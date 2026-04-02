# Packages
from typing import List

# Local
from .token import Token, TokenType

class DslLexer :
    """
    lex luth- Ahem. Da best lexer ever (My first attempt at a lexer)

    Attributes:
        contents (str): contents of the .dsl file read
        _index (int): index of the characters being lexically analysed
    """
    def __init__(self) :
        """
        Init

        Args:
            path (str): Path to the .dsl file
        """
        self.contents: str
        self._index: int
        self._line: int
        self._prev_lines: int

    def lex_DSL(self, path: str) -> List[Token] :
        """
        Load and lex a .dsl file

        Args:
            path (str): Path to the .dsl file
        Returns:
            List[Token]: A list of Token objects containing lexemes from the .dsl file
        """
        self._index = 0
        self._line = 1
        self._prev_lines = 0
        self._read_DSL(path)
        return self._lex()

    def _read_DSL(self, path: str) -> None :
        """
        Read file
        
        Args:
            path (str): Path to the .dsl file
        """
        with open(path, "r") as file :
            self.contents = file.read()

    def _lex(self) -> List[Token] :
        """
        Lexically analyse the contents of the .dsl file, (the algo).
        """
        token_list = []

        while(self._index < len(self.contents)) :
            if self.contents[self._index] == " " or self.contents[self._index] == "\n" :
                self._index += 1
                
                if self.contents[self._index - 1] == "\n" :
                    self._line += 1
                    self._prev_lines = self._index

            elif self._is_identifier() :
                token_list.append(self._handle_identifier())

            elif self._is_vis_controller() :
                token_list.append(self._handle_vis_controller())

            elif self._is_punctuator() :
                token_list.append(self._handle_punctuator())
            
            elif self._is_operator() :
                token_list.append(self._handle_operator())

            elif self._is_literal() :
                token_list.append(self._handle_literal())

            elif self._is_numeric() :
                token_list.append(self._handle_numeric())

            else :
                token_list.append(self._handle_undef())

        return token_list
    
    # ********************************************  Character classifying functions  ********************************************
    
    def _is_identifier(self) -> bool :
        """
        Detects keywords and identifiers
        """
        if self.contents[self._index].isalpha() or self.contents[self._index] == "_" :
            return True
        return False
    
    def _is_vis_controller(self) -> bool :
        """
        Detects visibility controller
        """
        match self.contents[self._index] :
            case "+" :
                return True
            case "#" :
                return True
            case "-" :
                return True
            case _ :
                return False

    def _is_punctuator(self) -> bool :
        """
        Detects punctuators
        """
        match self.contents[self._index] :
            case "{" :
                return True
            case "}" :
                return True
            case "(" :
                return True
            case ")" :
                return True
            case ":" :
                return True
            case "," :
                return True
            case _ :
                return False
            
    def _is_operator(self) -> bool :
        """
        Detects operators
        """
        match self.contents[self._index] :
            case "=" :
                return True
            case _ :
                return False
    
    def _is_numeric(self) -> bool :
        """
        Detects numeric literal start criteria
        """
        if self.contents[self._index].isdigit() or self.contents[self._index] == "." :
            return True
        return False
    
    def _is_literal(self) -> bool :
        """
        Detects string literal start criteria
        """
        if self.contents[self._index] == "\"" :
            return True
        return False
    
    # ********************************************  Category handling functions  ********************************************

    def _handle_identifier(self) -> Token :
        """
        Accumulates keywords and identifiers
        """
        # Create Token object
        token = Token(self._line, self._index - self._prev_lines + 1, "")

        # Accumulate till end of literal '"'
        while (
            self._index < len(self.contents) and (
                self.contents[self._index].isalpha() or
                self.contents[self._index].isdigit() or
                self.contents[self._index] == "_"
            )
        ) :
            token.tk_lexeme += self.contents[self._index]
            self._index += 1

        # Match token type
        match token.tk_lexeme :
            case "class" :
                token.tk_type = TokenType.TK_CLASS
            case "function" :
                token.tk_type = TokenType.TK_FUNCT
            case "void" :
                token.tk_type = TokenType.TK_VAR_TYPE
            case "int" :
                token.tk_type = TokenType.TK_VAR_TYPE
            case "char" :
                token.tk_type = TokenType.TK_VAR_TYPE
            case "bool" :
                token.tk_type = TokenType.TK_VAR_TYPE
            case "str" :
                token.tk_type = TokenType.TK_VAR_TYPE
            case "float" :
                token.tk_type = TokenType.TK_VAR_TYPE
            case "True" :
                token.tk_type = TokenType.TK_LIT_BOOL
            case "False" :
                token.tk_type = TokenType.TK_LIT_BOOL
            case _ :
                token.tk_type = TokenType.TK_IDEN
        
        return token
    
    def _handle_vis_controller(self) -> Token :
        """
        Returns visibility controller. (Pointless, done to keep everything similar)
        """
        # Create Token object
        token = Token(self._line, self._index - self._prev_lines + 1, self.contents[self._index], TokenType.TK_VIS_CTRL)
        
        self._index += 1

        return token

    def _handle_punctuator(self) -> Token :
        """
        Returns punctuator. (Pointless, done to keep everything similar)
        """
        # Create Token object
        token = Token(self._line, self._index - self._prev_lines + 1, self.contents[self._index])

        self._index += 1

        # Match token type
        match token.tk_lexeme :
            case "{" :
                token.tk_type = TokenType.TK_L_BRACE
            case "}" :
                token.tk_type = TokenType.TK_R_BRACE
            case "(" :
                token.tk_type = TokenType.TK_L_PARAN
            case ")" :
                token.tk_type = TokenType.TK_R_PARAN
            case "," :
                token.tk_type = TokenType.TK_COMMA
            case ":" :
                token.tk_type = TokenType.TK_COLON

        return token
    
    def _handle_operator(self) -> Token :
        """
        Returns operator. (Pointless, done to keep everything similar)
        """
        # Create Token object
        token = Token(self._line, self._index - self._prev_lines + 1, self.contents[self._index])

        self._index += 1

        # Match token type
        match token.tk_lexeme :
            case "=" :
                token.tk_type = TokenType.TK_EQUALS

        return token

    def _handle_numeric(self) -> Token :
        """
        Accumulates numeric literals
        """
        # Create Token object
        token = Token(self._line, self._index - self._prev_lines + 1, "", TokenType.TK_LIT_NUM)

        # Accumulate till character differs from 0-9 or '.'
        while self._index < len(self.contents) and (self.contents[self._index].isdigit() or self.contents[self._index] == ".") :
            token.tk_lexeme += self.contents[self._index]
            self._index += 1

        # Check if only one decimal point '.' exists
        if token.tk_lexeme.count(".") > 1 :
            token.tk_type = TokenType.TK_UNDEF

        return token

    def _handle_literal(self) -> Token :
        """
        Accumulates string literals
        """
        # Create Token object
        token = Token(self._line, self._index - self._prev_lines + 1, "", TokenType.TK_LIT_STR)

        # Accumulate till end of literal '"'
        while self._index < len(self.contents) :
            token.tk_lexeme += self.contents[self._index]
            self._index += 1

            if self.contents[self._index - 1] == "\"" and len(token.tk_lexeme) > 1 :
                break

        # Check if closing quote '"' exists
        if not token.tk_lexeme.endswith("\"") :
            token.tk_type = TokenType.TK_UNDEF
        
        return token
    
    def _handle_undef(self) -> Token :
        """
        Returns undefined tokens. (Pointless, done to keep everything similar)
        """
        # Create Token object
        token = Token(self._line, self._index - self._prev_lines + 1, self.contents[self._index], TokenType.TK_UNDEF)

        self._index += 1

        return token