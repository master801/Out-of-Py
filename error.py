
class Error(Exception):
    pass

class UnknownError(Error):

    def __init__(self, message):
        self.message = message
