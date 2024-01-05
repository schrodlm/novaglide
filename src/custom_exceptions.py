"""Module containing custom exceptions for the game.
"""

class OutOfBoundsError(Exception):
    """
    Custom exception class for handling cases where values exceed 
    expected range.

    Parameters
    ----------
    message : str, optional
        Custom error message, by default:
        "Coordinates are outside the window size".
    """

    def __init__(self, message="Coordinates are outside the window size"):
        self.message = message
        super().__init__(self.message)
        
class InvalidColorString(Exception):
    """Custom class for handling cases when invalid color string is passed.

    Parameters
    ----------
    message : str, optional
        Custom error message, by default:
        "Color is not valid string representation in pygame".
    """

    def __init__(self, 
                message="Color is not valid string representation in pygame"):
        self.message = message
        super().__init__(self.message)

class InvalidClientException(Exception):
    def __init__(self, message="Incorrect client"):
        self.message = message
        super().__init__(self.message)