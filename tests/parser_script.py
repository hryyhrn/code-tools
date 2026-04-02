from typing import List

from code_tools.dsl_tools import DslLexer
from code_tools.dsl_tools import DSLParser
from code_tools.dsl_tools.ast import ASTNode

def traverse_tree(tree_node: ASTNode, level: int) -> None :
    spaces = ""
    for i in range(level) :
        spaces += "    "
    print(f"{spaces}Node: {tree_node.name}, Level: {level}, type: {type(tree_node)}")

    for node in tree_node.children:
        traverse_tree(node, level + 1)

if __name__ == "__main__" :
    lexer = DslLexer()
    tokens_list = lexer.lex_DSL("./docs/example.dsl")

    parser = DSLParser()
    res = parser.parse(tokens_list)
    if not res.status :
        print(res.message)

    traverse_tree(parser.tree, 0)