""" Testing response class """

from unittest import TestCase
from pythonzimbra.response_xml import ResponseXml


class TestResponseXml(TestCase):

    """ Response class tests
    """

    tested_server_result = '<soap:Envelope xmlns:soap="http://www.w3' \
                           '.org/2003/05/soap-envelope"><soap:Header><context' \
                           ' xmlns="urn:zimbra"/></soap:Header><soap:Body' \
                           '><GetVersionInfoResponse ' \
                           'xmlns="urn:zimbraAdmin"><info ' \
                           'platform="UBUNTU12_64" host="zre-ubuntu12-64" ' \
                           'minorversion="0" microversion="5" ' \
                           'buildDate="20130910-1244" type="NETWORK" ' \
                           'majorversion="8" release="20130910124124" ' \
                           'version="8.0.5_GA_5839' \
                           '.NETWORK"/></GetVersionInfoResponse></soap:Body' \
                           '></soap:Envelope>'

    """ The result we test against (coming from a GetVersionInfoRequest by
    running zmsoap -z --json -t admin GetVersionInfoRequest -vv) """

    tested_server_result_multi_value = \
        '<soap:Envelope xmlns:soap="http://www.w3' \
        '.org/2003/05/soap-envelope"><soap:Header><context' \
        ' xmlns="urn:zimbra"/></soap:Header><soap:Body' \
        '><GetAllDomainsResponse> ' \
        '<domain id="b37d6b9" name="client1.unbound.example.fr"></domain>' \
        '<domain id="444d6b9" name="client1.unbound.example.fr"></domain>' \
        '</GetAllDomainsResponse></soap:Body' \
        '></soap:Envelope>'\

    """ This one is a stripped version of a GetAlDomains """

    response = None

    """ Our response object """

    def setUp(self):

        """ Generate a Response object and set our tested server result string
        """

        self.response = ResponseXml()
        self.response.set_response(self.tested_server_result)

        self.response_multi = ResponseXml()
        self.response_multi.set_response(self.tested_server_result_multi_value)

    def test_get_body(self):

        """ Checks the body against a pickled expectation
        """

        expected_result = {
            "GetVersionInfoResponse": {
                "info": {
                    "majorversion": "8",
                    "buildDate": "20130910-1244",
                    "microversion": "5",
                    "platform": "UBUNTU12_64",
                    "host": "zre-ubuntu12-64",
                    "version": "8.0.5_GA_5839.NETWORK",
                    "release": "20130910124124",
                    "type": "NETWORK",
                    "minorversion": "0"
                }
            }
        }

        self.assertEqual(
            expected_result,
            self.response.get_body()
        )

    def test_get_header(self):

        expected_result = {
            "context": {
            }
        }

        self.assertEqual(
            expected_result,
            self.response.get_header()
        )

    def test_is_batch(self):

        self.assertFalse(
            self.response.is_batch(),
            "Is_Batch hasn't returned False, rather than %s" % (
                str(self.response.is_batch())
            )
        )

    def test_get_batch(self):

        self.assertIsNone(
            self.response.get_batch(),
            "get_batch hasn't returned None"
        )

    def test_get_response(self):

        expected_result = {
            "GetVersionInfoResponse": {
                "info": {
                    "majorversion": "8",
                    "buildDate": "20130910-1244",
                    "microversion": "5",
                    "platform": "UBUNTU12_64",
                    "host": "zre-ubuntu12-64",
                    "version": "8.0.5_GA_5839.NETWORK",
                    "release": "20130910124124",
                    "type": "NETWORK",
                    "minorversion": "0"
                }
            }
        }

        self.assertEqual(
            expected_result,
            self.response.get_response()
        )

    def test_get_response_multi(self):
        """ For cases where we have several tags with the same name.

        In that case, for a given tag name as a key, we want a list of dicts
        containing the content of each tag, instead of a single dict.
        """

        resp = self.response_multi.get_response()
        gad_resp = resp['GetAllDomainsResponse']

        self.assertTrue('domain' in gad_resp)
        self.assertTrue(gad_resp['domain'])
        self.assertIsInstance(gad_resp['domain'], list)
        self.assertEqual(len(gad_resp['domain']), 2)
