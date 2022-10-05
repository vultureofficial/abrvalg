"""
Main
----

Command line interface.
"""
import argparse
import subprocess
from abrvalg import __version__ as version, interpreter


try:
    input = raw_input
except NameError:
    pass


def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-v', '--verbose', action='store_true')
    argparser.add_argument('-t', '--transpile', action='store_true')
    argparser.add_argument('file', nargs='?')
    argparser.add_argument('output', nargs='?')

    return argparser.parse_args()


def interpret_file(path, verbose=False, outPut=None, transpile=False):
    with open(path) as f:
        print("Reading : " + path)
        res = interpreter.evaluate(f.read(), verbose=verbose)
        

        if transpile:
            file = ""
            if outPut != None:
                file = outPut
            else:
                path = path.split('.')[0]
                file = path + ".cpp"

            print("Writing: " + file)
            with open(file, "w+") as fw:
                if res != None:
                    fw.write(res)
                fw.close()
        else:
            #TODO: compilation 
            exit(0)



def repl():
    print('Abrvalg {}. Press Ctrl+C to exit.'.format(version))
    env = interpreter.create_global_env()
    buf = ''
    try:
        while True:
            inp = input('>>> ' if not buf else '')
            if inp == '':
                print(interpreter.evaluate_env(buf, env))
                buf = ''
            else:
                buf += '\n' + inp
    except KeyboardInterrupt:
        pass


def main():
    args = parse_args()
    if args.file:
        interpret_file(args.file, args.verbose, args.output, args.transpile)
    else:
        repl()

if __name__ == '__main__':
    main()
