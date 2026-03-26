# Local
from ..utils import read_file

# Packages
import re

class plantUML_parser :
    """
    plantUML parser class. Parses .puml files and extracts classes, fields, methods.

    Args:
        _file (str): Holds the parsed .puml string
        _class_members (List[str]): Holds all the classes contained in the .puml string 
    """
    
    def __init__(self) :
        """
        init function to setup plantUML_parser object
        """

        self._file = None
        self._classes = None
        self._class_members = None
    
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

        class_pattern = r"class.*?}"
        _classes = re.findall(class_pattern, self._file, re.DOTALL)

        public_pattern = r"\+.*?\n"
        protected_pattern = r"#.*?\n"
        private_pattern = r"-.*?\n"

        # Extract public, protected, private attributes of each class
        for cl in _classes :
            # Extract class name
            items_to_remove = ["class", " ", "{"]
            pattern = '|'.join(map(re.escape, items_to_remove))
            class_name = re.sub(pattern, "", re.findall(r"class.*?\{", cl, re.DOTALL)[0])
            print(class_name)

            _attrs = []
            _attrs.append(re.findall(public_pattern, cl))
            _attrs.append(re.findall(protected_pattern, cl))
            _attrs.append(re.findall(private_pattern, cl))

            # Extract fields and methods from each type of attrs
            for attr_type in _attrs :
                for attr in attr_type :
                    if re.search(r"\(.*?\)", attr, re.DOTALL) :
                        print(f"Method: {attr}")
                    else :
                        print(f"Field: {attr}")