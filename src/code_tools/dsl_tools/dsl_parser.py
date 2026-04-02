# Packages
from dataclasses import dataclass
from typing import List

# Local
from .token import Token, TokenType
from .ast import ASTNode, ClassNode, FieldNode, MethodNode, FunctionNode, DataNode, DataType

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
        self._tokens_list = tokens_list
        self._index = 0

        while self._index < len(self._tokens_list) :
            if self._peek(TokenType.TK_CLASS) :
                res = self._handle_class(self.tree)
                if not res.status :
                    print(res.message)
            if self._peek(TokenType.TK_FUNCT) :
                res = self._handle_function(self.tree)
                if not res.status :
                    print(res.message)
            else :
                print("Invalid token sequence")
                self._index += 1

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
        if (lexeme := self._check_and_consume(TokenType.TK_IDEN)) is None :
            return ParserStatus(False, "Missing class name identifier")
        class_node.name = lexeme

        # Look for the opening brace, consume if found, throw error if not found
        if self._check_and_consume(TokenType.TK_L_BRACE) is None :
            return ParserStatus(False, "Missing class L-Brace token")
        
        # Parse class fields and methods
        members_parse_res = self._handle_class_members(class_node)
        if not members_parse_res.status :
            return members_parse_res
        
        # Look for the closing brace, consume if found, throw error if not found
        if self._check_and_consume(TokenType.TK_R_BRACE) is None :
            return ParserStatus(False, "Missing class R-Brace token")
        
        # Add class_node to the children of parent
        parent.children.append(class_node)

        return ParserStatus(True, "Success")

    def _handle_class_members(self, parent: ASTNode) -> ParserStatus :
        """
        Parser function to handle class member tokens.

        Args:
            parent (ASTNode): Parent AST node to which the parsed class member AST nodes will become children of.
        """
        if self._peek(TokenType.TK_R_BRACE) :
            return ParserStatus(True, "Success")
        
        # Look for the visibility controller token, consume if found, throw error if not found
        if (
            (vis_ctrl := self._check_and_consume(TokenType.TK_VIS_PUB)) is None and
            (vis_ctrl := self._check_and_consume(TokenType.TK_VIS_PROT)) is None and
            (vis_ctrl := self._check_and_consume(TokenType.TK_VIS_PRIV)) is None
        ) :
            return ParserStatus(False, "Missing visibility control token")
        
        # Look for the member name identifier, consume if found, throw error if not found
        if (member_name := self._check_and_consume(TokenType.TK_IDEN)) is None :
            return ParserStatus(False, "Missing class member name identifier")
        
        # Identify if the member is a field or a method and pass control to the appropriate handler
        if self._peek(TokenType.TK_COLON) :
            field_parse_res = self._handle_field(member_name, vis_ctrl, parent)
            if not field_parse_res.status :
                return field_parse_res
        elif self._peek(TokenType.TK_L_PARAN) :
            method_parse_res = self._handle_method(member_name, vis_ctrl, parent)
            if not method_parse_res.status :
                return method_parse_res
        
        # Recursively call the handle class members function to extract the other members
        return self._handle_class_members(parent)

    def _handle_field(self, vis_ctrl: str, member_name: str, parent: ASTNode) -> ParserStatus :
        """
        Parser function to handle class field tokens.

        Args:
            member_name (str): Name of the field.
            vis_ctrl (str): Visibility of the field.
            parent (ASTNode): Parent AST node to which the parsed class field AST node will become a child of.
        """
        # Empty Function AST node
        field_node = FieldNode()
        field_node.name = member_name
        field_node.vis_ctrl = vis_ctrl

        # Look for the colon separator token
        if self._check_and_consume(TokenType.TK_COLON) is None :
            return ParserStatus(False, "Missing colon separator after field name")
        
        # Empty Data AST node
        data_node = DataNode()

        # Look for the datatype keyword
        if (lexeme := self._check_and_consume(TokenType.TK_VAR_TYPE)) is None :
            return ParserStatus(False, "Missing field datatype")
        data_node.dtype = self._datatype(lexeme)

        # Look for the assignment value token (optional)
        isValPresent = True
        if self._check_and_consume(TokenType.TK_EQUALS) is None :
            isValPresent = False
        
        # Look for the value literal (optional)
        if (isValPresent and 
            (lexeme := self._check_and_consume(TokenType.TK_LIT_BOOL)) is None and 
            (lexeme := self._check_and_consume(TokenType.TK_LIT_NUM)) is None and
            (lexeme := self._check_and_consume(TokenType.TK_LIT_STR)) is None
        ) :
            return ParserStatus(False, "Missing field literal value after \"=\"")
        data_node.value = lexeme
        
        # Add data_node to the children of field_node
        field_node.children.append(data_node)
        # Add field_node to the children of parent
        parent.children.append(field_node)

        return ParserStatus(True, "Success")

    def _handle_method(self, vis_ctrl: str, member_name: str, parent: ASTNode) -> ParserStatus :
        """
        Parser function to handle class method tokens.

        Args:
            member_name (str): Name of the method.
            vis_ctrl (str): Visibility of the method.
            parent (ASTNode): Parent AST node to which the parsed class method AST node will become a child of.
        """
        # Empty Method AST node
        method_node = MethodNode()
        method_node.name = member_name
        method_node.vis_ctrl = vis_ctrl

        # Look for the opening parenthesis, consume if found, throw error if not found
        if self._check_and_consume(TokenType.TK_L_PARAN) is None :
            return ParserStatus(False, "Missing method L-Paran token")
        
        # Parse method parameters
        param_parse_res = self._handle_params(method_node)
        if not param_parse_res.status :
            return param_parse_res
        
        # Look for the closing parenthesis, consume if found, throw error if not found
        if self._check_and_consume(TokenType.TK_R_PARAN) is None :
            return ParserStatus(False, "Missing function R-Paran token")

        # Look for the return type separator colon, consume if found, throw error if not found
        if self._check_and_consume(TokenType.TK_COLON) is None :
            return ParserStatus(False, "Missing function return type separator colon")

        # Look for the return type keyword, consume if found, throw error if not found
        if (lexeme := self._check_and_consume(TokenType.TK_VAR_TYPE)) is None :
            return ParserStatus(False, "Missing function return type keyword")
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
        if (lexeme := self._check_and_consume(TokenType.TK_IDEN)) is None :
            return ParserStatus(False, "Missing function name identifier")
        function_node.name = lexeme

        # Look for the opening parenthesis, consume if found, throw error if not found
        if self._check_and_consume(TokenType.TK_L_PARAN) is None :
            return ParserStatus(False, "Missing function L-Paran token")

        # Parse function parameters
        param_parse_res = self._handle_params(function_node)
        if not param_parse_res.status :
            return param_parse_res

        # Look for the closing parenthesis, consume if found, throw error if not found
        if self._check_and_consume(TokenType.TK_R_PARAN) is None :
            return ParserStatus(False, "Missing function R-Paran token")

        # Look for the return type separator colon, consume if found, throw error if not found
        if self._check_and_consume(TokenType.TK_COLON) is None :
            return ParserStatus(False, "Missing function return type separator colon")

        # Look for the return type keyword, consume if found, throw error if not found
        if (lexeme := self._check_and_consume(TokenType.TK_VAR_TYPE)) is None :
            return ParserStatus(False, "Missing function return type keyword")
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

        # Look for the datatype keyword
        if (lexeme := self._check_and_consume(TokenType.TK_VAR_TYPE)) is None :
            return ParserStatus(False, "Missing parameter return type")
        parameter_node.dtype = self._datatype(lexeme)

        # Look for the assignment value token (optional)
        isValPresent = True
        if self._check_and_consume(TokenType.TK_EQUALS) is None :
            isValPresent = False
        
        # Look for the value literal (optional)
        if (isValPresent and 
            (lexeme := self._check_and_consume(TokenType.TK_LIT_BOOL)) is None and 
            (lexeme := self._check_and_consume(TokenType.TK_LIT_NUM)) is None and
            (lexeme := self._check_and_consume(TokenType.TK_LIT_STR)) is None
        ) :
            return ParserStatus(False, "Missing parameter literal value after \"=\"")
        parameter_node.value = lexeme

        # Look for the comma separator token
        if self._check_and_consume(TokenType.TK_COMMA) is None :
            if not self._peek(TokenType.TK_R_PARAN) :
                return ParserStatus(False, "Missing punctuator \",\" in between parameter declarations")
        else :
            if not self._peek(TokenType.TK_IDEN) :
                return ParserStatus(False, "Invalid punctuator \",\"")

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
        return self._tokens_list[self._index - 1].tk_lexeme
    
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
    
    def _datatype(self, lexeme: str) -> DataType :
        """
        Return the datatype enum corresponding to the datatype lexeme.

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