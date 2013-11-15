""" Run an AuthRequest against the zimbra server and return the
authentication token """

from datetime import datetime
from urllib2 import HTTPError

from pythonzimbra.request_xml import RequestXml
from pythonzimbra.communication import Communication
from pythonzimbra.response_xml import ResponseXml
from pythonzimbra.tools import preauth


def authenticate(url, byval, key, by='name', expires=0, timestamp=None,
                 timeout=None):

    if timestamp is None:
        timestamp = int(datetime.now().strftime("%s")) * 1000

    pak = preauth.create_preauth(byval, key, by, expires, timestamp)

    auth_request = RequestXml()

    auth_request.add_request(
        'AuthRequest',
        {
            'account': {
                'by': by,
                '_content': byval
            },
            'preauth': {
                'timestamp': timestamp,
                'expires': expires,
                '_content': pak
            }
        },
        'urn:zimbraAccount'
    )

    server = Communication(url, timeout)

    response = ResponseXml()

    try:

        server.send_request(auth_request, response)

    except HTTPError:

        # A HTTPError (which is an AuthError in most cases) occured. Simply
        # return nothing

        return None

    return response.get_response()['AuthResponse']['authToken']['_content']