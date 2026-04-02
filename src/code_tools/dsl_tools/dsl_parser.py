# Packages
from dataclasses import dataclass
from typing import List

# Local
from .token import Token, TokenType
from .ast import Visibility, DataType
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
    
    def parse(self, tokens_list: List[Token]) -> ParserStatus :
        """
        Parses lexer output and creates the AST representation of the DSL.

        Args:
            tokens_list (List[Token]): List of tokens output by the lexer
        """
        self._tokens_list = tokens_list
        self._index = 0

        while self._index < len(self._tokens_list):
            if self._peek(TokenType.TK_CLASS) :
                kw_parse_res = self._handle_class(self.tree)
            elif self._peek(TokenType.TK_FUNCT) :
                kw_parse_res = self._handle_function(self.tree)
            else :
                return ParserStatus(False, "Invalid token sequence")

            if not kw_parse_res.status :
                return kw_parse_res
            
        return ParserStatus(True, "Success")

    def _handle_class(self, parent: ASTNode) -> ParserStatus :
        """
        Parser function to handle class tokens.

        Args:
            parent (ASTNode): Parent AST node to which the parsed class AST node will become a child of.
        """
        # Empty Function AST node
        class_node = ClassNode()
        
        # Consume "class" keyword
        self._check_and_consume(TokenType.TK_CLASS)

        # Look for the class name identifier, consume if found, throw error if not found
        if (lexeme := self._check_and_consume(TokenType.TK_IDEN)) == None :
            return ParserStatus(False, "Missing class name identifier")
        class_node.name = lexeme

        # Look for the opening brace, consume if found, throw error if not found
        if self._check_and_consume(TokenType.TK_L_BRACE) == None :
            return ParserStatus(False, "Missing class L-Brace token")
        
        # Parse class fields and methods
        while True :
            if self._peek(TokenType.TK_VIS_CTRL) != None :
                if self._peek(TokenType.TK_COLON, 2) != None :
                    member_parse_res = self._handle_field(class_node)
                elif self._peek(TokenType.TK_L_PARAN, 2) != None :
                    member_parse_res = self._handle_method(class_node)
                else :
                    return ParserStatus(False, "Invalid class member syntax")
                
                if not member_parse_res.status :
                    return member_parse_res
            elif self._peek(TokenType.TK_R_BRACE) != None :
                break
            else :
                return ParserStatus(False, "Invalid class member syntax")
        
        # Look for the closing brace, consume if found
        self._check_and_consume(TokenType.TK_R_BRACE)
        
        # Add class_node to the children of parent
        parent.children.append(class_node)

        return ParserStatus(True, "Success")

    def _handle_field(self, parent: ASTNode) -> ParserStatus :
        """
        Parser function to handle class field tokens.

        Args:
            parent (ASTNode): Parent AST node to which the parsed class field AST node will become a child of.
        """
        # Empty Function AST node
        field_node = FieldNode()

        # Look for the visibility control token, consume if found
        field_node.vis_ctrl = self._visibility(self._check_and_consume(TokenType.TK_VIS_CTRL))

        # Look for the field name identifier
        if (lexeme := self._peek(TokenType.TK_IDEN)) == None :
            return ParserStatus(False, "Missing field name identifier")
        field_node.name = lexeme

        # Parse field data node
        data_parse_res = self._handle_data(field_node)
        if not data_parse_res.status :
            return data_parse_res
        
        # Add field_node to the children of parent
        parent.children.append(field_node)

        return ParserStatus(True, "Success")

    def _handle_method(self, parent: ASTNode) -> ParserStatus :
        """
        Parser function to handle class method tokens.

        Args:
            parent (ASTNode): Parent AST node to which the parsed class method AST node will become a child of.
        """
        # Empty Method AST node
        method_node = MethodNode()

        # Look for the visibility control token, consume if found
        method_node.vis_ctrl = self._visibility(self._check_and_consume(TokenType.TK_VIS_CTRL))

        # Look for the method name identifier, consume if found, throw error if not found
        if (lexeme := self._check_and_consume(TokenType.TK_IDEN)) == None :
            return ParserStatus(False, "Missing method name identifier")
        method_node.name = lexeme
        
        # Look for the opening parenthesis, consume if found, throw error if not found
        if self._check_and_consume(TokenType.TK_L_PARAN) == None :
            return ParserStatus(False, "Missing method L-Paran token")
        
        # Parse method parameters
        while True :
            if self._peek(TokenType.TK_IDEN) != None :
                param_parse_res = self._handle_data(method_node)
                if not param_parse_res.status :
                    return param_parse_res
            elif self._check_and_consume(TokenType.TK_COMMA) != None :
                if self._peek(TokenType.TK_IDEN) == None :
                    return ParserStatus(False, "Missing identifier after \",\" punctuator")
            elif self._peek(TokenType.TK_R_PARAN) :
                break
            else :
                print(self._tokens_list[self._index])
                return ParserStatus(False, "Invalid method signature")

        # Look for the closing parenthesis, consume if found
        self._check_and_consume(TokenType.TK_R_PARAN)

        # Look for the return type separator colon, consume if found, throw error if not found
        if self._check_and_consume(TokenType.TK_COLON) == None :
            return ParserStatus(False, "Missing method return type separator colon")

        # Look for the return type keyword, consume if found, throw error if not found
        if (lexeme := self._check_and_consume(TokenType.TK_VAR_TYPE)) == None :
            return ParserStatus(False, "Missing method return type keyword")
        method_node.rtype = lexeme

        # Add method_node to the children of parent
        parent.children.append(method_node)

        return ParserStatus(True, "Success")

    def _handle_function(self, parent: ASTNode) -> ParserStatus :
        """
        Parser function to handle function tokens.

        Args:
            parent (ASTNode): Parent AST node to which the parsed function AST node will become a child of.
        """
        # Empty Function AST node
        function_node = FunctionNode()
        
        # Consume "function" keyword
        self._check_and_consume(TokenType.TK_FUNCT)

        # Look for the function name identifier, consume if found, throw error if not found
        if (lexeme := self._check_and_consume(TokenType.TK_IDEN)) == None :
            return ParserStatus(False, "Missing function name identifier")
        function_node.name = lexeme

        # Look for the opening parenthesis, consume if found, throw error if not found
        if self._check_and_consume(TokenType.TK_L_PARAN) == None :
            return ParserStatus(False, "Missing function L-Paran token")

        # Parse function parameters
        while True :
            if self._peek(TokenType.TK_IDEN) != None :
                param_parse_res = self._handle_data(function_node)
                if not param_parse_res.status :
                    return param_parse_res
            elif self._check_and_consume(TokenType.TK_COMMA) != None :
                if self._peek(TokenType.TK_IDEN) == None :
                    return ParserStatus(False, "Missing identifier after \",\" punctuator")
            elif self._peek(TokenType.TK_R_PARAN) :
                break
            else :
                print(self._tokens_list[self._index])
                return ParserStatus(False, "Invalid function signature")

        # Look for the closing parenthesis, consume if found
        self._check_and_consume(TokenType.TK_R_PARAN)

        # Look for the return type separator colon, consume if found, throw error if not found
        if self._check_and_consume(TokenType.TK_COLON) == None :
            return ParserStatus(False, "Missing function return type separator colon")

        # Look for the return type keyword, consume if found, throw error if not found
        if (lexeme := self._check_and_consume(TokenType.TK_VAR_TYPE)) == None :
            return ParserStatus(False, "Missing function return type keyword")
        function_node.rtype = lexeme

        # Add function_node to the children of parent
        parent.children.append(function_node)

        return ParserStatus(True, "Success")
    
    def _handle_data(self, parent: ASTNode) -> ParserStatus :
        """
        Parser function to handle data tokens.

        Args:
            parent (ASTNode): Parent AST node to which the parsed data AST node will become a child of.
        """
        # Empty data AST node
        data_node = DataNode()

        # Look for data node's name identifier, consume if found, throw error if not found
        if (lexeme := self._check_and_consume(TokenType.TK_IDEN)) == None :
            return ParserStatus(False, "Missing variable/parameter name")
        data_node.name = lexeme

        # Look for the colon separator token, consume if found, throw error if not found
        if self._check_and_consume(TokenType.TK_COLON) == None :
            return ParserStatus(False, "Missing colon after variable/parameter name")

        # Look for the datatype keyword, consume if found, throw error if not found
        if (lexeme := self._check_and_consume(TokenType.TK_VAR_TYPE)) == None :
            return ParserStatus(False, "Missing variable/parameter datatype")
        data_node.dtype = self._datatype(lexeme)

        # Look for the assignment value token (optional)
        isValPresent = True
        if self._check_and_consume(TokenType.TK_EQUALS) == None :
            isValPresent = False
        
        # Look for the value literal (optional)
        if (isValPresent and 
            (lexeme := self._check_and_consume(TokenType.TK_LIT_BOOL)) == None and 
            (lexeme := self._check_and_consume(TokenType.TK_LIT_NUM)) == None and
            (lexeme := self._check_and_consume(TokenType.TK_LIT_STR)) == None
        ) :
            return ParserStatus(False, "Missing parameter literal value after \"=\"")
        data_node.value = lexeme

        # Add data_node to the children of parent
        parent.children.append(data_node)

        return ParserStatus(True, "Success")

    def _check_and_consume(self, token_type: TokenType) -> str :
        """
        Check the token type of the current token being parsed.
        Return the lexeme if the type matches. Return None if not. Token is consumed if the expected type matches.

        Args:
            token_type (TokenType): Expected type of the token 
        """
        if self._index < len(self._tokens_list) and self._tokens_list[self._index].tk_type == token_type :
            self._index += 1
            return self._tokens_list[self._index - 1].tk_lexeme
        return None
    
    def _peek(self, token_type: TokenType, offset: int = 0) -> str :
        """
        Check the token type of the current token being parsed without consuming the current token.
        Return the lexeme if the token type matches. Return None if not.

        Args:
            token_type (TokenType): Expected type of the token 
        """
        if self._index + offset < len(self._tokens_list) and self._tokens_list[self._index + offset].tk_type == token_type :
            return self._tokens_list[self._index + offset].tk_lexeme
        return None
    
    def _visibility(self, lexeme: str) -> Visibility :
        """
        Return the visibility control enum value corresponding to the lexeme.

        Args:
            lexeme (str): visibility control lexeme
        """
        match lexeme :
            case "+" :
                return Visibility.public
            case "#" :
                return Visibility.protected
            case "-" :
                return Visibility.private
    
    def _datatype(self, lexeme: str) -> DataType :
        """
        Return the datatype enum value corresponding to the lexeme.

        Args:
            lexeme (str): datatype lexeme
        """
        match lexeme :
            case "void" :
                return DataType.void
            case "int" :
                return DataType.int
            case "char" :
                return DataType.char
            case "bool" :
                return DataType.bool
            case "str" :
                return DataType.str
            case "float" :
                return DataType.float