""" Testing response class """

from unittest import TestCase
from pythonzimbra.response_json import ResponseJson


class TestResponseJson(TestCase):

    """ Response class tests
    """

    tested_server_result = '{ "Header": { "context": { "_jsns": "urn:zimbra" ' \
                           '} }, "Body": { "GetVersionInfoResponse": { ' \
                           '"info": { "type": "NETWORK", "version": "8.0' \
                           '.5_GA_5839.NETWORK", "release": "20130910124124",' \
                           ' "buildDate": "20130910-1244", ' \
                           '"host": "zre-ubuntu12-64", "platform": ' \
                           '"UBUNTU12_64", "majorversion": "8", ' \
                           '"minorversion": "0", "microversion": "5" }, ' \
                           '"_jsns": "urn:zimbraAdmin" } }, ' \
                           '"_jsns": "urn:zimbraSoap" }'

    """ The result we test against (coming from a GetVersionInfoRequest) """

    response = None

    """ Our response object """

    def setUp(self):

        """ Generate a Response object and set our tested server result string
        """

        self.response = ResponseJson()
        self.response.set_response(self.tested_server_result)

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
