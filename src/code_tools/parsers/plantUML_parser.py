# Local
from ..utils import read_file

# Packages
import re

class plantUML_parser :
    """
    plantUML parser class. Parses .puml files and extracts classes, fields, methods.

    Args:
        parsed_file (str): Holds the parsed .puml string
        parsed_classes (List[str]): Holds all the classes contained in the .puml string 
    """
    
    def __init__(self) :
        """
        init function to setup plantUML_parser object
        """

        self._file = None
        self._classes = None
    
    def parse_file(self, path) -> None :
        """
        Parse .puml file, extract classes, fields, methods

        Args:
            path (str): Path to .puml file
        """

        self._file = read_file(path)
        self._parse_classes()

    def _parse_classes(self) -> None :
        """
        Extract classes out of the .puml file's contents
        """

        pattern = "class.*?}"
        self._classes = re.findall(pattern, self._file, re.DOTALL)

    def _parse_methods() :
        pass

    def _parse_fields() :
        pass