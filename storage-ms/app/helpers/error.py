# Author: Nina Mislej
# Date created: 07.01.2025

class ErrorResponse:
    """
    This class encapsulates an error message and an associated HTTP status code.
    Code defaults to `400`.
    """

    def __init__(self, message, code=400):
        self.message = message
        self.code = code