# Lexical analyser (lexer) algorithm:

# 1. Open and read the file.
# 2. Read the next character. Skip whitespace, newlines, and comments. If EOF, stop.
# 3. Pass the character to the character classifier to determine its category.
# 4. Dispatch to the corresponding category handler. Each handler accumulates according to its own rules — single character tokens emit immediately, multi-character ones loop until termination.
# 5. Pass the accumulated lexeme to the pattern classifier. Determine the exact token type.
# 6. Attach metadata (type, lexeme, line, column) and store the token. Go to step 2.

# 1. Open and read the file.
content = None
with open("./data/example.dsl", "r") as file :
    content = file.read()

print(content)

# Character check functioins
def isAlpha(char: str) :
    if char.isalpha() or char == "_" :
        return True
    return False

def isNumeric(char: str) :
    if char.isdigit() or char == "." :
        return True
    return False

def isStringLiteral(char: str) :
    if char == "\"" :
        return True
    return False

def isVisibilityModifier(char: str) :
    if char == "+" or char == "#" or char == "-" :
        return True 
    return False

# Category handler functions
def handleAlpha() :
    pass

# 2. Read the next character. Skip whitespace, newlines, and comments. If EOF, stop.
i = 0
while(i < len(content)) :
    if content[i] == " " or content[i] == "\n" :
        i += 1
        continue
    
    elif isAlpha(content[i]) :
        pass

    elif isNumeric(content[i]) :
        print(content[i])

    elif isSymbol(content[i]) :
        pass

    i += 1