# Lexical analyser (lexer) algorithm:

# 1. Open and read the file.
# 2. Read the next character. Skip whitespace, newlines, and comments. If EOF, stop.
# 3. Pass the character to the character classifier to determine its category.
# 4. Dispatch to the corresponding category handler. Each handler accumulates according to its own rules — single character tokens emit immediately, multi-character ones loop until termination.
# 5. Pass the accumulated lexeme to the pattern classifier. Determine the exact token type.
# 6. Attach metadata (type, lexeme, line, column) and store the token. Go to step 2.

class dslLexer :
    """
    lex luth- Ahem. Da best lexer ever (My first attempt at a lexer)

    Attributes:
        content (str): Content of the .dsl file read
        _index (int): index of the characters being lexically analysed
    """

    def __init__(self, path: str = None) :
        """
        Init

        Args:
            path (str): Path to the .dsl file
        """
        
        self.content: str
        self._index: int
        
        if path :
            self.lexDSL(path)

    def lexDSL(self, path: str) -> None :
        """
        Load and lex a .dsl file

        Args:
            path (str): Path to the .dsl file
        """
        
        self._index = 0
        self._readDSL(path)
        self._lex()

    def _readDSL(self, path: str) -> None :
        """
        Read file
        
        Args:
            path (str): Path to the .dsl file
        """

        with open(path, "r") as file :
            self.content = file.read()

    def _lex(self) -> None :
        """
        Lexically analyse the contents of the .dsl file, (the algo).
        """

        self._index = 0

        char = ""
        while(self._index < len(self.content)) :
            char = self.content[self._index]

            if char == " " or char == "\n" :
                self._index += 1

            elif self._isIdentifier() :
                print(self._handleIdentifier())

            elif self._isVisController() :
                print(self._handleVisController())

            elif self._isPunctuator() :
                print(self._handlePunctuator())
            
            elif self._isOperator() :
                print(self._handleOperator())

            elif self._isLiteral() :
                print(self._handleLiteral())

            elif self._isNumeric() :
                print(self._handleNumeric())

            else :
                self._index += 1

    # ********************************************  Character classifying functions  ********************************************
    
    def _isIdentifier(self) -> bool :
        """
        Detects keywords and identifiers
        """

        if self.content[self._index].isalpha() or self.content[self._index] == "_" :
            return True
        return False
    
    def _isVisController(self) -> bool :
        """
        Detects visibility controller
        """

        match self.content[self._index] :
            case "+" :
                return True
            case "#" :
                return True
            case "-" :
                return True
            case _ :
                return False

    def _isPunctuator(self) -> bool :
        """
        Detects punctuators
        """

        match self.content[self._index] :
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
            
    def _isOperator(self) -> bool :
        """
        Detects operators
        """

        match self.content[self._index] :
            case "=" :
                return True
            case _ :
                return False
    
    def _isLiteral(self) -> bool :
        """
        Detects string literal start criteria
        """

        if self.content[self._index] == "\"" :
            return True
        return False
    
    def _isNumeric(self) -> bool :
        """
        Detects numeric literal start criteria
        """

        if self.content[self._index].isdigit() or self.content[self._index] == "." :
            return True
        return False
    
    # ********************************************  Category handling functions  ********************************************

    def _handleIdentifier(self) -> str :
        """
        Accumulates keywords and identifiers
        """
        
        accumulatedStr = ""
        # Accumulate till end of literal '"'
        while (
            self._index < len(self.content) and (
                self.content[self._index].isalpha() or
                self.content[self._index].isdigit() or
                self.content[self._index] == "_"
            )
        ) :
            accumulatedStr += self.content[self._index]
            self._index += 1

        return accumulatedStr
    
    def _handleVisController(self) -> str :
        """
        Returns visibility controller. (Pointless, done to keep everything similar)
        """
        
        self._index += 1
        return self.content[self._index - 1]

    def _handlePunctuator(self) -> str :
        """
        Returns punctuator. (Pointless, done to keep everything similar)
        """
        
        self._index += 1
        return self.content[self._index - 1]
    
    def _handleOperator(self) -> str :
        """
        Returns operator. (Pointless, done to keep everything similar)
        """
        
        self._index += 1
        return self.content[self._index - 1]

    def _handleLiteral(self) -> str :
        """
        Accumulates string literals
        """

        accumulatedStr = ""
        # Accumulate till end of literal '"'
        while self._index < len(self.content) :
            accumulatedStr += self.content[self._index]
            self._index += 1

            if self.content[self._index - 1] == "\"" and len(accumulatedStr) > 1 :
                break

        return accumulatedStr
    
    def _handleNumeric(self) -> str :
        """
        Accumulates numeric literals
        """

        accumulatedStr = ""
        # Accumulate till character differs from 0-9 or '.'
        while self._index < len(self.content) and self.content[self._index].isdigit() or self.content[self._index] == "." :
            accumulatedStr += self.content[self._index]
            self._index += 1
        
        return accumulatedStr


if __name__ == "__main__" :
    lexer = dslLexer("./data/example.dsl")
    print(lexer.content)