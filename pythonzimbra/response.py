""" Zimbra response access. """


class Response(object):

    """ Unified access to Zimbra responses.

    """

    def set_response(self, response_text):

        """ Interpret the response object.

        Creates the internal response object by converting the given text
        from the HTTP communication into a managed object
        """

        pass

    def get_header(self):

        """ Return the header of the response.

        :returns: The response header in the documented dictionary format
        :rtype: dict
        """

        pass

    def get_body(self):

        """ Return the body of the response.

        :returns: The response body in the documented dictionary format
        :rtype: dict
        """

        pass

    def is_batch(self):

        """ Returns whether we have a BatchResponse.

        :returns: Whether we have a BatchResponse
        :rtype: bool
        """

        pass

    def get_batch(self):

        """ Returns an informative dictionary about a batch response.

        Returns a dictionary containing the following information::

            {
                "hasFault": <bool wether the batch has at least one SoapFault
                "idToName": {
                    <A dictionary mapping a response id to the corresponding
                    response name or Fault>
                }
                "nameToId": {
                    <A dictionary mapping response names (or Fault) to the
                    corresponding response id(s)
                }
            }

        If the method is called with no batch response existing, returns None

        :returns: Informative dictionary
        :rtype: dict or None
        """

        pass

    def get_response(self, request_id=0):

        """ Returns the response with the given request_id.

        Returns the specific response. If "request_id" isn't provided or 0,
        the first (or only one in a non-batch) response is returned.
        """

        pass

    def is_fault(self):

        """ Checks, wether this response has at least one fault response (
        supports both batch and single responses)
        """

        if self.is_batch():

            info = self.get_batch()

            return info['hasFault']

        else:

            my_response = self.get_response()

            if my_response.keys()[0] == 'Fault':

                return True

        return False