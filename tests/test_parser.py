from code_tools.parsers.plantUML_parser import plantUML_parser

def test_parser() :
    puml_file_path = "./data/example.puml"

    puml_parser = plantUML_parser()
    puml_parser.parse_file(puml_file_path)

if __name__ == "__main__" :
    test_parser()