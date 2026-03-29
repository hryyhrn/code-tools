# Packages
import pytest

# Local
from code_tools.dsl_tools import DslLexer
from code_tools.dsl_tools import Token, TokenType

# ******************************************** Fixtures ********************************************

@pytest.fixture
def default_lexer() :
    """
    Default lexer to be used by all the tests
    """
    
    return DslLexer()

# ******************************************** Tests ********************************************

@pytest.mark.parametrize(
    "input, expected", [
        ("class", [Token(1, 1, "class", TokenType.TK_CLASS)]),
        ("foo", [Token(1, 1, "foo", TokenType.TK_IDEN)]),
        ("3.14", [Token(1, 1, "3.14", TokenType.TK_LIT_NUM)]),
        ("+", [Token(1, 1, "+", TokenType.TK_VIS_PUB)])
    ]
)
def test_tokens(default_lexer, input, expected) :
    """
    Test to check individual tokens
    TODO Add more tests to cover all tokens
    """
    
    # Lexer setup
    test_lexer = default_lexer
    test_lexer.contents = input
    test_lexer._index = 0
    test_lexer._line = 1
    test_lexer._prev_lines = 0
    
    assert test_lexer._lex() == expected

input_paths = ["./docs/example.dsl"]
expected_results = [
    [
        Token(1, 1, "class", TokenType.TK_CLASS),
        Token(1, 7, "foo", TokenType.TK_IDEN),
        Token(1, 11, "{", TokenType.TK_L_BRACE),
        Token(2, 5, "+", TokenType.TK_VIS_PUB),
        Token(2, 7, "publicField", TokenType.TK_IDEN),
        Token(2, 18, ":", TokenType.TK_COLON),
        Token(2, 20, "bool", TokenType.TK_BOOL),
        Token(2, 25, "=", TokenType.TK_EQUALS),
        Token(2, 27, "True", TokenType.TK_LIT_BOOL),
        Token(3, 5, "#", TokenType.TK_VIS_PROT),
        Token(3, 7, "protectedField", TokenType.TK_IDEN),
        Token(3, 21, ":", TokenType.TK_COLON),
        Token(3, 23, "str", TokenType.TK_STR),
        Token(3, 27, "=", TokenType.TK_EQUALS),
        Token(3, 29, "\"default\"", TokenType.TK_LIT_STR),
        Token(4, 5, "-", TokenType.TK_VIS_PRIV),
        Token(4, 7, "privateField", TokenType.TK_IDEN),
        Token(4, 19, ":", TokenType.TK_COLON),
        Token(4, 21, "float", TokenType.TK_FLOAT),
        Token(4, 27, "=", TokenType.TK_EQUALS),
        Token(4, 29, "3.14", TokenType.TK_LIT_NUM),
        Token(6, 5, "+", TokenType.TK_VIS_PUB),
        Token(6, 7, "publicMethod", TokenType.TK_IDEN),
        Token(6, 19, "(", TokenType.TK_L_PARAN),
        Token(6, 20, "param1", TokenType.TK_IDEN),
        Token(6, 26, ":", TokenType.TK_COLON),
        Token(6, 28, "str", TokenType.TK_STR),
        Token(6, 31, ")", TokenType.TK_R_PARAN),
        Token(6, 32, ":", TokenType.TK_COLON),
        Token(6, 34, "int", TokenType.TK_INT),
        Token(7, 5, "#", TokenType.TK_VIS_PROT),
        Token(7, 7, "protectedMethod", TokenType.TK_IDEN),
        Token(7, 22, "(", TokenType.TK_L_PARAN),
        Token(7, 23, "param2", TokenType.TK_IDEN),
        Token(7, 29, ":", TokenType.TK_COLON),
        Token(7, 31, "char", TokenType.TK_CHAR),
        Token(7, 35, ")", TokenType.TK_R_PARAN),
        Token(7, 36, ":", TokenType.TK_COLON),
        Token(7, 38, "float", TokenType.TK_FLOAT),
        Token(8, 5, "-", TokenType.TK_VIS_PRIV),
        Token(8, 7, "privateMethod", TokenType.TK_IDEN),
        Token(8, 20, "(", TokenType.TK_L_PARAN),
        Token(8, 21, "param3", TokenType.TK_IDEN),
        Token(8, 27, ":", TokenType.TK_COLON),
        Token(8, 29, "str", TokenType.TK_STR),
        Token(8, 32, ",", TokenType.TK_COMMA),
        Token(8, 34, "param4", TokenType.TK_IDEN),
        Token(8, 40, ":", TokenType.TK_COLON),
        Token(8, 42, "bool", TokenType.TK_BOOL),
        Token(8, 47, "=", TokenType.TK_EQUALS),
        Token(8, 49, "False", TokenType.TK_LIT_BOOL),
        Token(8, 54, ")", TokenType.TK_R_PARAN),
        Token(8, 55, ":", TokenType.TK_COLON),
        Token(8, 57, "void", TokenType.TK_VOID),
        Token(9, 1, "}", TokenType.TK_R_BRACE),
        Token(11, 1, "function", TokenType.TK_FUNCT),
        Token(11, 10, "functfoo", TokenType.TK_IDEN),
        Token(11, 18, "(", TokenType.TK_L_PARAN),
        Token(11, 19, "param5", TokenType.TK_IDEN),
        Token(11, 25, ":", TokenType.TK_COLON),
        Token(11, 27, "float", TokenType.TK_FLOAT),
        Token(11, 32, ",", TokenType.TK_COMMA),
        Token(11, 34, "param6", TokenType.TK_IDEN),
        Token(11, 40, ":", TokenType.TK_COLON),
        Token(11, 42, "int", TokenType.TK_INT),
        Token(11, 45, ")", TokenType.TK_R_PARAN),
        Token(11, 46, ":", TokenType.TK_COLON),
        Token(11, 48, "void", TokenType.TK_VOID),
    ]
]

@pytest.mark.parametrize(
    "path, expected", [
        (input_paths[0], expected_results[0])
    ]
)
def test_file(default_lexer, path, expected) :
    """
    Test to check file's lexed output
    """

    # Lexer setup
    test_lexer = default_lexer

    assert test_lexer.lex_DSL(path) == expected