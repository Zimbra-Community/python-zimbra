""" Request handling and generation. """

from pythonzimbra.exceptions.request import RequestHeaderContextException, NoNamespaceGiven


class Request(object):

    """ Zimbra SOAP request generation and handling.

    """

    valid_context_params = ['authToken', 'authTokenControl', 'session',
                            'account', 'change', 'targetServer', 'userAgent',
                            'via']

    """ Valid parameter name for Soap context """

    batch_request = False

    """ Are we doing batch requests? """

    batch_request_id = None

    """ If so, keep the current request id """

    def set_context_params(self, params):

        """ Set header context parameters. Refer to the top of <Zimbra
        Server-Root>/docs/soap.txt about specifics.

        The <format>-Parameter cannot be changed, because it is set by the
        implementing class.

        Should be called by implementing method to check for valid context
        params.

        :param params: A Dict containing context parameters.
        """

        for key, value in params.iteritems():

            if key not in self.valid_context_params:

                raise RequestHeaderContextException(
                    "%s is not a valid context parameter." % key
                )

    def set_auth_token(self, token):

        """ Convenience function to inject the auth token into the header.

        :param token: Auth token
        """

        self.set_context_params(
            {
                'authToken': {
                    '_content': token
                }
            }
        )

    def enable_batch(self, namespace, onerror="continue"):

        """ Enables batch request gathering.

        Do this first and then consecutively call "add_request" to add more
        requests. All requests have to be the same namespace, so specify the
        xml namespace (i.e. "urn:zimbra") here.

        :param namespace: The XML namespace of the requests to come
        :param onerror: "continue" (default) if one request fails (and
          response with soap Faults for the request) or "stop" processing.
        """

        self.batch_request = True
        self.batch_request_id = 1

        self._create_batch_node(namespace, onerror)

    def _create_batch_node(self, namespace, onerror):

        """Prepare the request structure to support batch mode

        The params are like in enable_batch
        """

        pass

    def add_request(self, request_name, request_dict, namespace=None):

        """ Add a request.

        This adds a request to the body or to the batchrequest-node if batch
        requesting is enabled. Has to update the self.batch_request_id after
        adding a batch request!

        Implementing classes should call this first for checks.

        :param request_name: The name of the request
        :param request_dict: The request parameters as a serializable dict.
          Check out xmlserializer documentation about this.
        :param namespace: The XML namespace of the request. (Please don't use
          the request_dict to specify it, use this parameter)
        :returns: The current request id (if batch processing) or None
        :rtype: int or None
        """

        if not self.batch_request:

            if not namespace:
                raise NoNamespaceGiven(
                    'You have added a request without specifying a XML '
                    'namespace, but you are not in batch request mode.'
                )

    def get_request(self):

        """ Return the request in the native form.
        """

        pass

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.get_request()
