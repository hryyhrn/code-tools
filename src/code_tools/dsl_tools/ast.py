# Packages
from enum import Enum
from typing import List

class Visibility(Enum) :
    """
    Visibility controllers
    """
    public = "+"
    protected = "#"
    private = "-"

class DataType(Enum) :
    """
    Datatypes
    """
    void = "void"
    int = "int"
    char = "char"
    bool = "bool"
    str = "str"
    float = "float"

class ASTNode :
    """
    Base AST Node class

    Attributes:
        name (str): Name of the AST node
        children (List[ASTNode]): List of references to the children of the AST node
    """
    def __init__(self, name = "") :
        self.name: str = name
        self.children: List[ASTNode] = []
        
class ClassNode(ASTNode) :
    """
    Class AST node
    """
    def __init__(self) :
        super().__init__()

class FieldNode(ASTNode) :
    """
    Field AST node. The value of the field is stored as Data AST nodes in the "children" attribute of the base AST class.

    Attributes:
        vis_ctrl (Visibility): Public, protected or private attribute visibility.
    """
    def __init__(self) :
        super().__init__()
        self.vis_ctrl: Visibility

class MethodNode(ASTNode) :
    """
    Method AST node. The parameters of the method are stored as Data AST nodes in the "children" attribute of the base AST class.
    
    Attributes:
        vis_ctrl (Visibility): Public, protected or private attribute visibility.
        rtype (DataType): Datatype of the method's return value.
    """
    def __init__(self) :
        super().__init__()
        self.vis_ctrl: Visibility
        self.rtype: DataType

class FunctionNode(ASTNode) :
    """
    Function AST node. The parameters of the function are stored as Data AST nodes in the "children" attribute of the base AST class.
    
    Attributes:
        rtype (DataType): Datatype of the function's return value.
    """
    def __init__(self) :
        super().__init__()
        self.rtype: DataType
        
class DataNode(ASTNode) :
    """
    Data carrying AST node
    """
    def __init__(self) :
        super().__init__()
        self.dtype: DataType
        self.value: str