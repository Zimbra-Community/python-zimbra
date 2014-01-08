""" Run an AuthRequest against the zimbra server and return the
authentication token """

from datetime import datetime
from urllib2 import HTTPError
from pythonzimbra.request_json import RequestJson

from pythonzimbra.request_xml import RequestXml
from pythonzimbra.communication import Communication
from pythonzimbra.response_json import ResponseJson
from pythonzimbra.response_xml import ResponseXml
from pythonzimbra.tools import preauth


def authenticate(url, account, key, by='name', expires=0, timestamp=None,
                 timeout=None, request_type="xml", admin_auth=False,
                 use_password=False):

    """ Authenticate to the Zimbra server

    :param url: URL of Zimbra SOAP service
    :param account: The account to be authenticated against
    :param key: The preauth key of the domain of the account or a password (if
      admin_auth or use_password is True)
    :param by: If the account is specified as a name, an ID or a
      ForeignPrincipal
    :param expires: When the token expires (or 0 for default expiration)
    :param timestamp: When the token was requested (None for "now")
    :param timeout: Timeout for the communication with the server. Defaults
      to the urllib2-default
    :param request_type: Which type of request to use ("xml" (default) or
      "json")
    :param admin_auth: This request should authenticate and generate an admin
      token. The "key"-parameter therefore holds the admin password (implies
      use_password)
    :param use_password: The "key"-parameter holds a password. Do a password-
      based user authentication.
    :return: The authentication token
    :rtype: str or None or unicode
    """

    if timestamp is None:
        timestamp = int(datetime.now().strftime("%s")) * 1000

    pak = ""
    if not admin_auth:
        pak = preauth.create_preauth(account, key, by, expires, timestamp)

    if request_type == 'xml':

        auth_request = RequestXml()

    else:

        auth_request = RequestJson()

    request_data = {
        'account': {
            'by': by,
            '_content': account
        }
    }

    ns = "urn:zimbraAccount"

    if admin_auth:

        ns = "urn:zimbraAdmin"

        request_data['password'] = key

    elif use_password:

        request_data['password'] = {
            "_content": key
        }

    else:

        request_data['preauth'] = {
            'timestamp': timestamp,
            'expires': expires,
            '_content': pak
        }

    auth_request.add_request(
        'AuthRequest',
        request_data,
        ns
    )

    server = Communication(url, timeout)

    if request_type == 'xml':

        response = ResponseXml()

    else:

        response = ResponseJson()

    try:

        server.send_request(auth_request, response)

    except HTTPError:

        # A HTTPError (which is an AuthError in most cases) occured. Simply
        # return nothing

        return None

    return response.get_response()['AuthResponse']['authToken']['_content']