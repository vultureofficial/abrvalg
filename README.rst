Abrvalg
=======

Abrvalg is a Python-like programming language interpreter and transpiler.

The project contains:

- Regular expression based lexer
- Top-down recursive descent parser
- AST-walking interpreter
- REPL
- CPP transpiler
- Static typing (Optional)

Abrvalg doesn't require any third-party libraries.

What the language looks like:

.. code-block::

    using io

    func main() -> int:
        let filePtr: file = io::openFile("testing2.txt", "r")
        //io::writeFile(filePtr, "This is a test!!!!")

        let contents: string = io::readFile(filePtr)

        io::println(contents)

        io::closeFile(filePtr)
        return 0


You can find more examples in ``tests`` directory.

How to try it:

.. code-block::
    
    git clone https://github.com/akrylysov/abrvalg.git
    cd abrvalg
    python -m abrvalg tests/factorial.abr
