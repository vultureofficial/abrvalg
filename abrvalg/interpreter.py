"""
Interpreter
-----------

AST-walking interpreter.
"""
from __future__ import print_function
from cgitb import reset
import operator
from collections import namedtuple
from pydoc import classname
import re
from textwrap import indent
from abrvalg import ast
from abrvalg.lexer import Lexer, TokenStream
from abrvalg.parser import Parser
from abrvalg.errors import AbrvalgSyntaxError, report_syntax_error
from abrvalg.utils import print_ast, print_tokens, print_env
from abrvalg.ops import add, sub, div, mul, mod,gt,ge,lt,le,eq,ne



buffer = "#include <data_types.h>\n#include <vector>\n#include <range.h>\n\n"

BuiltinFunction = namedtuple('BuiltinFunction', ['params', 'body'])
object_list = []

class Break(Exception):
    pass


class Continue(Exception):
    pass


class Return(Exception):
    def __init__(self, value):
        self.value = value


class Environment(object):

    def __init__(self, parent=None, args=None):
        self._parent = parent
        self._values = {}
        if args is not None:
            self._from_dict(args)

    def _from_dict(self, args):
        for key, value in args.items():
            self.set(key, value)

    def set(self, key, val):
        self._values[key] = val

    def get(self, key):
        val = self._values.get(key, None)
        if val is None and self._parent is not None:
            return self._parent.get(key)
        else:
            return val

    def asdict(self):
        return self._values

    def __repr__(self):
        return 'Environment({})'.format(str(self._values))


def eval_type(eval, tps):
    
    for tp in tps:
        if type(eval) == tp:
            return tp(eval)
    
def eval_binary_operator(node, env):
    simple_operations = {
        '+': add,
        '-': sub,
        '*': mul,
        '/': div,
        '%': mod,
        '>': gt,
        '>=': ge,
        '<': lt,
        '<=': le,
        '==': eq,
        '!=': ne,
        '..': lambda start, end: ast.BinaryOperator('..', start, end),
        '...': lambda start, end: range(start, end + 1),
    }
    lazy_operations = {
        '&&': lambda lnode, lenv: eval_expression(lnode.left, lenv) + " && "+  eval_expression(lnode.right, lenv),
        '||': lambda lnode, lenv: eval_expression(lnode.left, lenv) + " || "+  eval_expression(lnode.right, lenv)
    }
    if node.operator in simple_operations:
        return simple_operations[node.operator](eval_expression(node.left, env), eval_expression(node.right, env))
    elif node.operator in lazy_operations:
        return lazy_operations[node.operator](node, env)
    else:
        raise Exception('Invalid operator {}'.format(node.operator))


def eval_unary_operator(node, env):
    operations = {
        '-': operator.neg,
        '!': operator.not_,
    }
    return operations[node.operator](eval_expression(node.right, env))


def eval_assignment(node, env):
    if isinstance(node.left, ast.SubscriptOperator):
        return eval_setitem(node, env)
    
    elif isinstance(node.left, ast.ClassAccess):
        name = node.left.left.value 
        access_name = node.left.right.value

        ret = eval_expression(node.right, env)
        if env.get(access_name) != None:
            return name + "." + access_name + " = " + ret + ";"
        env.set(access_name, ret)
        return "auto " + name + " = " + access_name + "()." + ret   
    
    else:
        
        val = str(eval_expression(node.right, env))
        if env.get(node.left.value) != None:
            return node.left.value + " = " + val + ";"
        env.set(node.left.value, val)
        return "auto " + node.left.value + " = " + val + ";"


def eval_condition(node, env):
    cond  = eval_expression(node.test, env)

    ret_str = " if (" + cond + ") {"
    _if_body = eval_statements(node.if_body, env) 
    ret_str = ret_str + _if_body + "\n}"

    for cond in node.elifs:
        cnd = eval_expression(cond.test, env)
        ret_str = ret_str + " else if (" + cnd + ") {"
        else_if_body = eval_statements(cond.body, env)
        ret_str = ret_str + else_if_body + "\n}"

    if node.else_body is not None:
        ret_str = ret_str + " else {"
        val = eval_statements(node.else_body, env)
        ret_str = ret_str + val + "\n}"

    return ret_str


def eval_match(node, env):
    test = eval_expression(node.test, env)
    ret_str = "switch (" + test + ") {\n"
    for pattern in node.patterns:
        #if eval_expression(pattern.pattern, env) == test:
        #    return eval_statements(pattern.body, env)
        body = eval_statements(pattern.body, env)
        match = eval_expression(pattern.pattern, env)
        ret_str = ret_str + "case " + match + ":\n{" + body + "\nbreak;\n}\n"
    if node.else_body is not None:
        default = eval_statements(node.else_body, env)
        ret_str = ret_str + " default:\n{" + default + "\n}\n"
    ret_str = ret_str + "}\n"

    return ret_str


def eval_while_loop(node, env):
    cond = eval_expression(node.test, env)
    body = eval_statements(node.body, env)

    ret_str = 'while (' + cond + ') {'
    ret_str = ret_str + body + '\n}\n'
    return ret_str


def eval_for_loop(node, env):
    var_name = node.var_name
    env.set(var_name,0)
    collection = eval_expression(node.collection, env)

    ret_str = 'for '

    if type(collection) == ast.BinaryOperator:
        if collection.operator == '..':
            left= collection.left, 
            right = collection.right
            left = str(left[0])
            right = str(right)

            ret_str = ret_str + '( auto ' + var_name + ': range::range(' + left + "," + right + ')) {' #+ " + 1"
            #ret_str = ret_str + '; ' + var_name 
            body = eval_statements(node.body, env) 
            ret_str = ret_str + body + "\n}"
        else:
            print("Syntax error: Invalid loop operator "+ collection.operator)
            exit()

    return ret_str


def eval_function_declaration(node, env):
    env.set(node.name, node)

    func = node.ret[1] 
    params = node.params
    if node.name == "main":
        params = node.params + [ast.TypedParam("argc", "i32"), ast.TypedParam("argv", "i8**")]
    func = func + " " + node.name + "(" 
    call_env = Environment(env, None)

    for i in range(0, len(params)):
        param = params[i]
        if type(param) == ast.TypedParam:
            func = func + param.data_type + " " + param.name  
            call_env.set(param.name, 0)
        else:
            call_env.set(param, 0)
            func = func + "auto " + param 


        if i != len(params) -1:
            func = func + ", "

    func = func + ") {"
    res = None
    try:
        res = eval_statements(node.body, call_env)
        func = func + str(res) + "\n}\n" 
    except Return as ret:
        return ret.value
    
    return func

def eval_group(node, env):
    ret = "(" + eval_expression(node.left, env) + ")"
    return ret


def eval_classaccess(node, env):
    ret_str = ""
    class_name= node.left.value
    res = ""
    if type(node.right) == ast.Call:
        res = eval_call(node.right, env)
    elif type(node.right) == ast.Identifier :
        res = eval_expression(node.right, env)
    elif type(node.right) == ast.BinaryOperator:
        res = eval_expression(node.right, env)
        #TODO: fix codegen for obj::
        
    if env.get(class_name) != None:
        ret_str = ret_str + class_name +'.'
    else:
        ret_str = ret_str + class_name +'().'

    ret_str = ret_str + res

    return ret_str
def eval_classdef(node, env):
    ret_str = 'class ' + node.name[1]
    object_list.append(node.name[0])
    for i in range(0,len(node.parents)):
        parent = node.parents[i] 
        if i == 0:
            ret_str = ret_str + ": public " + parent 
        elif i < len(node.parents) - 1:
            ret_str = ret_str + ", public " + parent
        else:
            ret_str = ret_str + parent 

    ret_str = ret_str + "{\npublic:\n"
    ret_str = ret_str + node.name[1] + "() {}\n"
    ret_str = ret_str + "~" +node.name[1] + "() {}"

    body = eval_statements(node.body, env) 
    ret_str = ret_str + body + "\n};\n"

    return ret_str

def eval_include(node, env):
    module = node.module
    #env.set(module, 0)
    return "#include <" + module + ".h>" 


def eval_typed_var(node, env):
    ret_str = node.type[1] + " " + node.name[1] 
    env.set(node.name[1], 0)
    val = ""
    if node.value != None:
        val = " = " + str(eval_expression(node.value, env))
    ret_str = ret_str + val + ";"
    return ret_str

def eval_call(node, env):
    function = env.get(node.left)
    ret_str = node.left.value + " ("
    n_actual_args = len(node.arguments)

    for i in range(0, n_actual_args):
        param = node.arguments[i]

        val = ""
        
        if type(param) == ast.BinaryOperator:
            val = str(eval_expression(param, env))
        elif type(param) == ast.ClassAccess:
            val = "(" + str(eval_classaccess(param, env)) + ")"
        elif type(param) == ast.String:
            val = '"' + param.value + '"'
        elif type(param) == ast.Call:
            val = str(eval_expression(param, env))
        elif type(param) == ast.SubscriptOperator:
            val = str(eval_expression(param, env))
        else:
            val = str(param.value)

        if i != n_actual_args -1:
            ret_str = ret_str + val + " , "
        else:
            ret_str = ret_str + val 
        
    if node.tagged ==None:
        return ret_str + ");"
    else:
        return ret_str + ") "

def eval_identifier(node, env):
    name = node.value
    val = env.get(name)
    if val is None:
        raise NameError('Name "{}" is not defined'.format(name))
    return name


def eval_getitem(node, env):
    collection = eval_expression(node.left, env)
    key = eval_expression(node.key, env)
    return collection + '[' + key + ']'


def eval_setitem(node, env):
    collection = eval_expression(node.left.left, env)
    key = eval_expression(node.left.key, env)
    val = eval_expression(node.right, env)

    return collection + '.at(' + key + ') = ' + val + ';'


def eval_array(node, env):
    ret_str = "std::vector {"
    for i  in range(0, len(node.items)):
        item = node.items[i]
        val = eval_expression(item, env) 
        if i < len(node.items) -1:
            ret_str = ret_str + val + ","
        else:
            ret_str = ret_str + val 

    return ret_str + '};'


def eval_dict(node, env):
    return {eval_expression(key, env): eval_expression(value, env) for key, value in node.items}


def eval_return(node, env):
    return "return " + str(eval_expression(node.value, env)) + ";" if node.value is not None else "return ;"


evaluators = {
    ast.Number: lambda node, env: str(node.value),
    ast.String: lambda node, env: '"' + str(node.value) + '"',
    ast.Array: eval_array,
    ast.Dictionary: eval_dict,
    ast.Identifier: eval_identifier,
    ast.BinaryOperator: eval_binary_operator,
    ast.UnaryOperator: eval_unary_operator,
    ast.SubscriptOperator: eval_getitem,
    ast.Assignment: eval_assignment,
    ast.Condition: eval_condition,
    ast.Match: eval_match,
    ast.WhileLoop: eval_while_loop,
    ast.ForLoop: eval_for_loop,
    ast.Function: eval_function_declaration,
    ast.Call: eval_call,
    ast.Return: eval_return,
    ast.TypedName: eval_typed_var, 
    ast.UsingNode: eval_include, 
    ast.ClassDefinition: eval_classdef,
    ast.ClassAccess: eval_classaccess, 
    ast.GroupExpression: eval_group
}


def eval_node(node, env):
    tp = type(node)
    if tp in evaluators:
        return evaluators[tp](node, env)
    else:
        raise Exception('Unknown node {} {}'.format(tp.__name__, node))


def eval_expression(node, env):
    return eval_node(node, env)


def eval_statement(node, env):
    return eval_node(node, env)


def eval_statements(statements, env):
    ret = None
    str_res = ""
    for statement in statements:
        if isinstance(statement, ast.Break):
            str_res = str_res + '\nbreak;'
            continue
        elif isinstance(statement, ast.Continue):
            str_res = str_res + '\ncontinue;'
            continue
        else:
            ret = eval_statement(statement, env)
            str_res =  str_res + "\n" + str(ret) 


    return str_res


def add_builtins(env):
    builtins = {
        "null":"null", 
        "true":"true",
        "false": "false"
    }

    for key in builtins.keys():
        env.set(key, 0)


def create_global_env():
    env = Environment()
    add_builtins(env)
    return env


def evaluate_env(s, env, verbose=False):
    lexer = Lexer()
    try:
        tokens = lexer.tokenize(s)
    except AbrvalgSyntaxError as err:
        report_syntax_error(lexer, err)
        if verbose:
            raise
        else:
            return

    if verbose:
        print('Tokens')
        print_tokens(tokens)
        print()

    token_stream = TokenStream(tokens)

    try:
        program = Parser().parse(token_stream)
    except AbrvalgSyntaxError as err:
        report_syntax_error(lexer, err)
        if verbose:
            raise
        else:
            return

    if verbose:
        print('AST')
        print_ast(program.body)
        print()

    ret = eval_statements(program.body, env)

    if verbose:
        print('Environment')
        print_env(env)
        print()

    return buffer + ret


def evaluate(s, verbose=False):
    return evaluate_env(s, create_global_env(), verbose)
