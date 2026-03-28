from code_tools.dsl_tools import DslLexer

if __name__ == "__main__" :
    lexer = DslLexer()
    tokens_list = lexer.lex_DSL("./docs/example.dsl")
    # print(lexer.content)
    for token in tokens_list :
        print(token)