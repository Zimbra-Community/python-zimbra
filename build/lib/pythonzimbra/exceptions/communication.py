""" Communication Exceptions """

import exceptions


class UnknownRequestType(exceptions.BaseException):

    """ The type of the request is neither json nor xml
    """

    pass
