""" Zimbra communication handler. """

from __future__ import unicode_literals

import sys

# Py2-Compatibility

if sys.version < '3':
    import urllib2 as ur  # pragma: no cover py3
    import urllib2 as ue  # pragma: no cover py3
else:
    import urllib.request as ur  # pragma: no cover py2
    import urllib.error as ue  # pragma: no cover py2

from pythonzimbra.request_json import RequestJson
from pythonzimbra.request_xml import RequestXml
from pythonzimbra.response_xml import ResponseXml
from pythonzimbra.response_json import ResponseJson
from .exceptions.communication import *


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

        if sys.version < '3' and self.url.startswith("https"):

            # Force tlsv1 on https-requests in Python 2

            import tools.urllib2_tls  # pragma: no cover py3

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

        if token is not None:
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

            server_request = ur.urlopen(
                self.url,
                request.get_request().encode("utf-8"),
                self.timeout
            )

            server_response = server_request.read()

            if isinstance(server_response, bytes):

                server_response = server_response.decode("utf-8")

            if response is None:

                local_response.set_response(
                    server_response
                )

            else:

                response.set_response(server_response)

        except ue.HTTPError as e:

            if e.code == 500:

                # 500 codes normally returns a SoapFault, that we can use

                server_response = e.fp.read()

                if isinstance(server_response, bytes):

                    server_response = server_response.decode("utf-8")

                if response is None:

                    local_response.set_response(server_response)

                else:

                    response.set_response(server_response)

            else:

                raise e

        if response is None:
            return local_response
