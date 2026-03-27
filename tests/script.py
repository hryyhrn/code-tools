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
        self.content: str
        self._index: int
        
        if path :
            self.lexDSL(path)

    def lexDSL(self, path: str) -> None :
        self._index = 0
        self._readDSL(path)
        self._lex()

    def _readDSL(self, path: str) -> None :
        with open(path, "r") as file :
            self.content = file.read()

    def _lex(self) -> None :
        self._index = 0

        char = ""
        while(self._index < len(self.content)) :
            char = self.content[self._index]

            if char == " " or char == "\n" :
                self._index += 1

            elif self.isIdentifier() :
                print(self.handleIdentifier())

            elif self.isVisController() :
                print(self.handleVisController())

            elif self.isPunctuator() :
                print(self.handlePunctuator())
            
            elif self.isOperator() :
                print(self.handleOperator())

            elif self.isLiteral() :
                print(self.handleLiteral())

            elif self.isNumeric() :
                print(self.handleNumeric())

            else :
                self._index += 1

    # ********************************************  Character classifying functions  ********************************************
    
    def isIdentifier(self) -> bool :
        """
        Detects keywords and identifiers
        """

        if self.content[self._index].isalpha() or self.content[self._index] == "_" :
            return True
        return False
    
    def isVisController(self) -> bool :
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

    def isPunctuator(self) -> bool :
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
            
    def isOperator(self) -> bool :
        """
        Detects operators
        """

        match self.content[self._index] :
            case "=" :
                return True
            case _ :
                return False
    
    def isLiteral(self) -> bool :
        """
        Detects string literal start criteria
        """

        if self.content[self._index] == "\"" :
            return True
        return False
    
    def isNumeric(self) -> bool :
        """
        Detects numeric literal start criteria
        """

        if self.content[self._index].isdigit() or self.content[self._index] == "." :
            return True
        return False
    
    # ********************************************  Category handling functions  ********************************************

    def handleIdentifier(self) -> str :
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
    
    def handleVisController(self) -> str :
        """
        Returns visibility controller. (Pointless, done to keep everything similar)
        """
        
        self._index += 1
        return self.content[self._index - 1]

    def handlePunctuator(self) -> str :
        """
        Returns punctuator. (Pointless, done to keep everything similar)
        """
        
        self._index += 1
        return self.content[self._index - 1]
    
    def handleOperator(self) -> str :
        """
        Returns operator. (Pointless, done to keep everything similar)
        """
        
        self._index += 1
        return self.content[self._index - 1]

    def handleLiteral(self) -> str :
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
    
    def handleNumeric(self) -> str :
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