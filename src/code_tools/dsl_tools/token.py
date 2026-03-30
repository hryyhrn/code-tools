# Packages
from dataclasses import dataclass
from enum import Enum

class TokenType(Enum) :
    """
    Token type enum
    """
    TK_UNDEF = "undefined"

    # Keywords
    TK_CLASS = "class"
    TK_FUNCT = "function"
    TK_VOID = "void"
    TK_INT = "int"
    TK_CHAR = "char"
    TK_BOOL = "bool"
    TK_STR = "str"
    TK_FLOAT = "float"
    
    # Identifiers
    TK_IDEN = "identifier"

    # Visibility controllers
    TK_VIS_PUB = "+"
    TK_VIS_PROT = "#"
    TK_VIS_PRIV = "-"
    
    # Punctuators
    TK_L_BRACE = "{"
    TK_R_BRACE = "}"
    TK_L_PARAN = "("
    TK_R_PARAN = ")"
    TK_COMMA = ","
    TK_COLON = ":"

    # Operators
    TK_EQUALS = "="

    # Literals
    TK_LIT_NUM = "numeric_lit"
    TK_LIT_STR = "string_lit"
    TK_LIT_BOOL = "boolean_lit"

@dataclass
class Token :
    """
    A dataclass to hold each token
    
    Attributes:
        line (int): Line number of the .dsl file where the token was found
        column (int): Line number of the .dsl file where the token was found
        tk_lexeme (str): The actual token lexed
        tk_type (TokenType): Type of the token
    """
    line: int
    column: int
    tk_lexeme: str
    tk_type: TokenType = TokenType.TK_UNDEF