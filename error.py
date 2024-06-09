#!/usr/bin/env python3

class Error(Exception):
    pass


class UnknownError(Error):

    def __init__(self, message):
        self.message = message
