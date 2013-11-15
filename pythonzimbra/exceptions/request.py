""" Request exceptions """

import exceptions


class RequestHeaderContextException(exceptions.BaseException):

    """ Invalid context parameter specified

    """

    pass


class NoNamespaceGiven(exceptions.BaseException):

    """ No namespace specified, when it should be
    """

    pass