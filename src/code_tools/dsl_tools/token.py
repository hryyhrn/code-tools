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
    TK_VAR_TYPE = "var_type"
    
    # Identifiers
    TK_IDEN = "identifier"

    # Visibility controllers
    TK_VIS_CTRL = "vis_ctrl"
    
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