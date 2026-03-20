def read_file(path: str) -> str :
    """
    Reads the contents of a file

    Args:
        path (str): Path to the file to be read
    """

    contents = ""
    with open(path, "r") as file :
        contents = file.read()

    return contents