# define Python user-defined exceptions
class InvalidFileType(Exception):
    """Error: invalid file type"""

    pass


class CsvMissing(Exception):
    """Error: CSV file is missing"""

    pass


class JsonMissing(Exception):
    """Error: JSON file is missing"""

    pass
