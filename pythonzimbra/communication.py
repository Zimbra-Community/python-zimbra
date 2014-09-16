""" Zimbra communication handler. """

import urllib2
from pythonzimbra.request_json import RequestJson
from pythonzimbra.request_xml import RequestXml
from pythonzimbra.response_xml import ResponseXml
from pythonzimbra.response_json import ResponseJson
from exceptions.communication import *


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

    def gen_request(self, request_type="json", token=None, set_batch=False,
        batch_onerror=None):

        """ Convenience method to quickly generate a token

        :param request_type: Type of request (defaults to json)
        :param token: Authentication token
        :param set_batch: Also set this request to batch mode?
        :param batch_onerror: Onerror-parameter for batch mode
        :return: The request
        """

        if request_type == "json":

            local_request = RequestJson()

        elif request_type == "xml":

            local_request = RequestXml()

        else:

            raise UnknownRequestType()

        if not token is None:
            local_request.set_auth_token(token)

        if set_batch:
            local_request.enable_batch(batch_onerror)

        return local_request

    def send_request(self, request, response=None):

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

        local_response = None

        if response is None:

            if request.request_type == "json":

                local_response = ResponseJson()

            elif request.request_type == "xml":

                local_response = ResponseXml()

            else:

                raise UnknownRequestType()

        try:

            server_request = urllib2.urlopen(
                self.url,
                request.get_request(),
                self.timeout
            )

            if response is None:

                local_response.set_response(server_request.read())

            else:

                response.set_response(server_request.read())

        except urllib2.HTTPError as e:

            if e.code == 500:

                # 500 codes normally returns a SoapFault, that we can use

                if response is None:

                    local_response.set_response(e.fp.read())

                else:

                    response.set_response(e.fp.read())

            else:

                raise e

        if response is None:
            return local_response