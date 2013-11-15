""" Request exceptions """

import exceptions


class RequestHeaderContextException(exceptions.BaseException):
    pass


class NoXMLNSGiven(exceptions.BaseException):
    pass