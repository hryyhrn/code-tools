# Packages
from dataclasses import dataclass
from enum import Enum

class TokenType(Enum) :
    """
    Token type enum
    """
    
    TK_UNDEF = 0
    TK_KW = 1
    TK_IDEN = 2
    TK_VIS_CTRL = 3
    TK_PUNC = 4
    TK_OPER = 5
    TK_LIT = 6

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