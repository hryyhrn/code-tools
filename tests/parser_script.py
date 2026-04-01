from typing import List

from code_tools.dsl_tools import DslLexer
from code_tools.dsl_tools import DSLParser

if __name__ == "__main__" :
    lexer = DslLexer()
    tokens_list = lexer.lex_DSL("./docs/example.dsl")

    parser = DSLParser()
    parser.parse(tokens_list)

    for el in parser.tree.children :
        print(type(el), el.name)