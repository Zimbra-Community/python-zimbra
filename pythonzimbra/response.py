""" Zimbra response access. """


class Response(object):

    """ Unified access to Zimbra responses.

    """

    response_type = None

    """ The actual response will set its response type (xml, json) here """

    def clean(self):

        """ Clean up the response, so it can be used again
        """

        pass  # pragma: no cover

    def set_response(self, response_text):

        """ Interpret the response object.

        Creates the internal response object by converting the given text
        from the HTTP communication into a managed object
        """

        pass  # pragma: no cover

    def get_header(self):

        """ Return the header of the response.

        :returns: The response header in the documented dictionary format
        :rtype: dict
        """

        pass  # pragma: no cover

    def get_body(self):

        """ Return the body of the response.

        :returns: The response body in the documented dictionary format
        :rtype: dict
        """

        pass  # pragma: no cover

    def is_batch(self):

        """ Returns whether we have a BatchResponse.

        :returns: Whether we have a BatchResponse
        :rtype: bool
        """

        pass  # pragma: no cover

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

        pass  # pragma: no cover

    def get_response(self, request_id=0):

        """ Returns the response with the given request_id.

        Returns the specific response. If "request_id" isn't provided or 0,
        the first (or only one in a non-batch) response is returned.
        """

        pass  # pragma: no cover

    def get_fault_code(self):

        """
        Returns the fault error code of this response (overridden)

        We provide this additional method because of zimbra bug
         https://bugzilla.zimbra.com/show_bug.cgi?id=95490

        For batch responses, we return a dict of fault codes. The key is
        the request_id.

        :return: Fault code string
        """

        pass  # pragma: no cover

    def get_fault_message(self):

        """
        Returns the fault error message of this response (overridden)

        We provide this additional method because of zimbra bug
         https://bugzilla.zimbra.com/show_bug.cgi?id=95490

        For batch responses, we return a dict of fault messages. The key is
        the request_id.

        :return: Fault code error message
        """

        pass  # pragma: no cover

    def is_fault(self):

        """ Checks, wether this response has at least one fault response (
        supports both batch and single responses)
        """

        if self.is_batch():

            info = self.get_batch()

            return info['hasFault']

        else:

            my_response = self.get_response()

            if list(my_response.keys())[0] == "Fault":

                return True

        return False

    def _filter_response(self, response_dict):

        """ Add additional filters to the response dictionary

        Currently the response dictionary is filtered like this:

          * If a list only has one item, the list is replaced by that item
          * Namespace-Keys (_jsns and xmlns) are removed

        :param response_dict: the pregenerated, but unfiltered response dict
        :type response_dict: dict
        :return: The filtered dictionary
        :rtype: dict
        """

        filtered_dict = {}

        for key, value in response_dict.items():

            if key == "_jsns":

                continue

            if key == "xmlns":

                continue

            if type(value) == list and len(value) == 1:

                filtered_dict[key] = value[0]

            elif type(value) == dict and len(value.keys()) == 1 and "_content" \
                    in value.keys():

                filtered_dict[key] = value["_content"]

            elif type(value) == dict:

                tmp_dict = self._filter_response(value)

                filtered_dict[key] = tmp_dict

            else:

                filtered_dict[key] = value

        return filtered_dict
