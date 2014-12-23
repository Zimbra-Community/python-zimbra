""" Request exceptions """


class RequestHeaderContextException(Exception):

    """ Invalid context parameter specified

    """

    pass  # pragma: no cover


class NoNamespaceGiven(Exception):

    """ No namespace specified, when it should be
    """

    pass  # pragma: no cover
