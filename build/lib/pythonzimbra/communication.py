""" Zimbra communication handler. """

import urllib2


class Communication(object):

    """ Zimbra communication handler.

    Sends requests to the zimbra SOAP server and returns the responses in a
    dictionary.

    """

    url = None

    """ URL to the zimbra soap interface """

    timeout = None

    """ Timeout of the request """

    def __init__(self, url, timeout=None):

        """ Initialize the communication handler.
        """

        self.url = url
        self.timeout = timeout

    def send_request(self, request, response):

        """ Send the request.

        Sends the request and retrieves the results, formats them and returns
         them in a dict or a list (when it's a batchresponse). If something
         goes wrong, raises a SoapFailure or a HTTPError on system-side
         failures. Note: AuthRequest raises an HTTPError on failed
         authentications!

        :param request: The request to send
        :type request: pythonzimbra.request.Request
        :param response: A prebuilt response object
        :type response: pythonzimbra.response.Response
        :raises: pythonzimbra.exceptions.communication.SoapFailure or
                urllib2.HTTPError
        """

        try:

            server_request = urllib2.urlopen(
                self.url,
                request.get_request(),
                self.timeout
            )

            response.set_response(server_request.read())

        except urllib2.HTTPError as e:

            if e.code == 500:

                # 500 codes normally returns a SoapFault, that we can use

                response.set_response(e.fp.read())

            else:

                raise e