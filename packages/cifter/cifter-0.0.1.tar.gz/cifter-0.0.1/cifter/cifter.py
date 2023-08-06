from .errors import CIFParseError
from .parser import parse_itterable


def parse_file(filename):
    try:
        with open(filename) as f:
            return parse_itterable(f)
    except IOError as e:
        raise CIFParseError(f"Failed to open file '{filename}': {str(e)}")
