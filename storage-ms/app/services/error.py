# Author: Nina Mislej
# Date created: 07.01.2025

class ErrorResponse:
    def __init__(self, message, code=400):
        self.message = message
        self.code = code