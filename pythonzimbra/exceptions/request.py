""" Request exceptions """


class RequestHeaderContextException(Exception):

    """ Invalid context parameter specified

    """

    pass


class NoNamespaceGiven(Exception):

    """ No namespace specified, when it should be
    """

    pass
