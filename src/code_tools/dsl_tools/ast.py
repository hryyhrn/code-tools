# Packages
from typing import List

class ASTNode :
    """
    Base AST Node class

    Attributes:
        name (str): Name of the AST node
        children (List[ASTNode]): List of references to the children of the AST node
    """

    def __init__(self) :
        self.name: str = ""
        self.children: List[ASTNode] = None
        
class ClassNode(ASTNode) :
    """
    Class AST node
    """
    
    def __init__(self) :
        super().__init__()

class FieldNode(ASTNode) :
    """
    Field AST node
    """
    
    def __init__(self) :
        super().__init__()

class MethodNode(ASTNode) :
    """
    Method AST node
    """
    
    def __init__(self) :
        super().__init__()

class FunctionNode(ASTNode) :
    """
    Function AST node
    """
    
    def __init__(self) :
        super().__init__()