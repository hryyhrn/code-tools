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
        self.dtype: DataType
        self.vis_ctrl: Visibility
        self.val: VarNode

class MethodNode(ASTNode) :
    """
    Method AST node
    """
    def __init__(self) :
        super().__init__()
        self.rtype: DataType
        self.vis_ctrl: Visibility
        self.param_list: List[VarNode]

class FunctionNode(ASTNode) :
    """
    Function AST node
    """
    def __init__(self) :
        super().__init__()
        self.rtype: DataType
        self.param_list: List[VarNode]

class VarNode(ASTNode) :
    """
    Parameter AST node
    """
    def __init__(self) :
        super().__init__()
        self.dtype: DataType
        self.value: str