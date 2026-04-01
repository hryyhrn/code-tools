# Packages
from dataclasses import dataclass
from typing import List

# Local
from .token import Token, TokenType
from .ast import ASTNode, ClassNode, FieldNode, MethodNode, FunctionNode, DataNode

@dataclass
class ParserStatus :
    """
    Parser status object. Contains status, error messages, token data.
    
    Attributes:
        status (bool): Status of the last parsing action. True if successful, False incase of a failure.
        message (str): Debug message
    """
    status: bool
    message: str = ""

class DSLParser :
    def __init__(self) :
        self._tokens_list: List[Token]
        self._index: int
        self.tree: ASTNode = ASTNode("root")
    
    def parse(self, tokens_list: List[Token]) -> None :
        # TODO: Completely rework this
        self._tokens_list = tokens_list
        self._index = 0

        while self._index < len(self._tokens_list) :
            if self._tokens_list[self._index].tk_type == TokenType.TK_CLASS :
                class_node = self._handle_class()
                if class_node != None :
                    self.tree.children.append(class_node)
            elif self._tokens_list[self._index].tk_type == TokenType.TK_FUNCT :
                function_node = self._handle_function()
                if function_node != None :
                    self.tree.children.append(function_node)
            else :
                # print("Invalid token sequence")
                self._index += 1
                return

    def _handle_function(self, parent: ASTNode) -> ParserStatus :
        """
        Parser function to handle function tokens.

        Args:
            parent (ASTNode): Parent AST node to which the parsed function AST node will become a child of.
        """
        # Empty Function AST node
        function_node = FunctionNode()
        
        # Consume "function" keyword
        self._index += 1

        # Look for the function name identifier, consume if found, throw error if not found
        if (lexeme := self._check_and_consume(TokenType.TK_IDEN)) is None :
            return ParserStatus(False, "Missing function name identifier")
        function_node.name = lexeme

        # Look for the opening parenthesis, consume if found, throw error if not found
        if self._check_and_consume(TokenType.TK_L_PARAN) is None :
            return ParserStatus(False, "Missing function L-Paran token")

        # Parse function parameters
        self._handle_params(function_node)

        # Look for the closing parenthesis, consume if found, throw error if not found
        if self._check_and_consume(TokenType.TK_R_PARAN) is None :
            return ParserStatus(False, "Missing function R-Paran token")

        # Look for the return type separator colon, consume if found, throw error if not found
        if self._check_and_consume(TokenType.TK_COLON) is None :
            return ParserStatus(False, "Missing function return type separator colon")

        # Look for the return type keyword, consume if found, throw error if not found
        if (lexeme := self._check_and_consume(TokenType.TK_VAR_TYPE)) is None :
            return (False, "Missing function return type keyword")
        function_node.rtype = lexeme

        # Add function_node to the children of parent
        parent.children.append(function_node)

        return ParserStatus(True, "Success")
    
    def _handle_params(self, parent: ASTNode) -> ParserStatus :
        """
        Parser function to handle function parameters.

        Args:
            parent (ASTNode): Parent AST node to which the parsed parameter AST nodes will become children of.
        """
        if self._peek(TokenType.TK_R_PARAN) :
            return ParserStatus(True, "Success")
        
        # Empty parameter AST node
        parameter_node = DataNode()

        # Look for parameter name identifier
        if (lexeme := self._check_and_consume(TokenType.TK_IDEN)) is None :
            return ParserStatus(False, "Missing parameter name")
        parameter_node.name = lexeme

        # Look for the colon separator token
        if self._check_and_consume(TokenType.TK_COLON) is None :
            return ParserStatus(False, "Missing colon separator after function parameter name")

        # Look for the return type keyword
        if self._check_and_consume(TokenType.TK_VAR_TYPE) is None :
            return ParserStatus(False, "Missing parameter return type")
        
        # Look for the assignment value token (optional)
        isValPresent = True
        if self._check_and_consume(TokenType.TK_EQUALS) is None :
            isValPresent = False
        
        # Look for the value literal (optional)
        if (isValPresent and 
            (lexeme := self._check_and_consume(TokenType.TK_LIT_BOOL)) is None and 
            (lexeme := self._check_and_consume(TokenType.TK_LIT_NUM)) is None and
            (lexeme := self._check_and_consume(TokenType.TK_LIT_STR)) is None
        ):
            return ParserStatus(False, "Missing parameter literal value after \"=\"")
        parameter_node.value = lexeme

        # Look for the comma separator token
        self._check_and_consume(TokenType.TK_COMMA)

        # Add parameter_node to the children of parent
        parent.children.append(parameter_node)
        
        # Recursively call the handle params function to extract the other parameters
        return self._handle_params(parent) 

    def _check_and_consume(self, token_type: TokenType) -> str :
        """
        Check for the token type of the current token being parsed.
        Return the lexeme if the type matches. Return empty if not.

        Args:
            token_type (TokenType): Expected type of the token 
        """
        if self._index >= len(self._tokens_list) or self._tokens_list[self._index].tk_type != token_type :
            return None
        
        self._index += 1
        return self._tokens_list[self._index].tk_lexeme
    
    def _peek(self, token_type: TokenType) -> str :
        """
        Check for the token type of the current token being parsed without consuming the current token.
        Return True if the token type matches. Return False if not.

        Args:
            token_type (TokenType): Expected type of the token 
        """
        if self._index < len(self._tokens_list) and self._tokens_list[self._index].tk_type == token_type :
            return True
        return False