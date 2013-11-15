""" Testing response class """

from unittest import TestCase
from pythonzimbra.response_xml import ResponseXml
import pickle


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

    response = None

    """ Our response object """

    def setUp(self):

        """ Generate a Response object and set our tested server result string
        """

        self.response = ResponseXml()
        self.response.set_response(self.tested_server_result)

    def test_get_body(self):

        """ Checks the body against a pickled expectation
        """

        expected_result = "(dp0\nVsoap:Body\np1\n(" \
                          "dp2\nVGetVersionInfoResponse\np3\n(" \
                          "dp4\nVinfo\np5\n(" \
                          "dp6\nVmajorversion\np7\nV8\np8\nsVminorversion\np9" \
                          "\nV0\np10\nsVmicroversion\np11\nV5\np12" \
                          "\nsVplatform\np13\nVUBUNTU12_64\np14\nsVhost\np15" \
                          "\nVzre-ubuntu12-64\np16\nsVversion\np17\nV8.0" \
                          ".5_GA_5839" \
                          ".NETWORK\np18\nsVrelease\np19\nV20130910124124" \
                          "\np20\nsVtype\np21\nVNETWORK\np22\nsVbuildDate" \
                          "\np23\nV20130910-1244\np24\nssS'xmlns'\np25\nVurn" \
                          ":zimbraAdmin\np26\nsss."

        self.assertEqual(
            expected_result,
            pickle.dumps(self.response.get_body())
        )

    def test_get_header(self):

        expected_result = "(dp0\nVsoap:Header\np1\n(dp2\nVcontext\np3\n(" \
                          "dp4\nS'xmlns'\np5\nVurn:zimbra\np6\nsss."

        self.assertEqual(
            expected_result,
            pickle.dumps(self.response.get_header())
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

        expected_result = "(dp0\nVGetVersionInfoResponse\np1\n(" \
                          "dp2\nVinfo\np3\n(" \
                          "dp4\nVmajorversion\np5\nV8\np6\nsVminorversion\np7" \
                          "\nV0\np8\nsVmicroversion\np9\nV5\np10\nsVplatform" \
                          "\np11\nVUBUNTU12_64\np12\nsVhost\np13\nVzre" \
                          "-ubuntu12-64\np14\nsVversion\np15\nV8.0.5_GA_5839" \
                          ".NETWORK\np16\nsVrelease\np17\nV20130910124124" \
                          "\np18\nsVtype\np19\nVNETWORK\np20\nsVbuildDate" \
                          "\np21\nV20130910-1244\np22\nssS'xmlns'\np23\nVurn" \
                          ":zimbraAdmin\np24\nss."

        self.assertEqual(
            expected_result,
            pickle.dumps(self.response.get_response())
        )