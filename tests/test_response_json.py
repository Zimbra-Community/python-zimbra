""" Testing response class """

from unittest import TestCase
from pythonzimbra.response_json import ResponseJson
import pickle


class TestResponseJson(TestCase):

    """ Response class tests
    """

    tested_server_result = '{ "Header": { "context": { "_jsns": "urn:zimbra" ' \
                           '} }, "Body": { "GetVersionInfoResponse": { ' \
                           '"info": [{ "type": "NETWORK", "version": "8.0' \
                           '.5_GA_5839.NETWORK", "release": "20130910124124",' \
                           ' "buildDate": "20130910-1244", ' \
                           '"host": "zre-ubuntu12-64", "platform": ' \
                           '"UBUNTU12_64", "majorversion": "8", ' \
                           '"minorversion": "0", "microversion": "5" }], ' \
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

        expected_result = '(dp0\nVGetVersionInfoResponse\np1\n(' \
                          'dp2\nVinfo\np3\n(lp4\n(' \
                          'dp5\nVmajorversion\np6\nV8\np7\nsVbuildDate\np8' \
                          '\nV20130910-1244\np9\nsVmicroversion\np10\nV5\np11' \
                          '\nsVplatform\np12\nVUBUNTU12_64\np13\nsVhost\np14' \
                          '\nVzre-ubuntu12-64\np15\nsVversion\np16\nV8.0' \
                          '.5_GA_5839' \
                          '.NETWORK\np17\nsVrelease\np18\nV20130910124124' \
                          '\np19\nsVtype\np20\nVNETWORK\np21\nsVminorversion' \
                          '\np22\nV0\np23\nsasV_jsns\np24\nVurn:zimbraAdmin' \
                          '\np25\nss.'

        self.assertEqual(
            expected_result,
            pickle.dumps(self.response.get_body())
        )

    def test_get_header(self):

        expected_result = '(dp0\nVcontext\np1\n(' \
                          'dp2\nV_jsns\np3\nVurn:zimbra\np4\nss.'

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

        expected_result = '(dp0\nVGetVersionInfoResponse\np1\n(' \
                          'dp2\nVinfo\np3\n(' \
                          'dp4\nVmajorversion\np5\nV8\np6\nsVbuildDate\np7' \
                          '\nV20130910-1244\np8\nsVmicroversion\np9\nV5\np10' \
                          '\nsVplatform\np11\nVUBUNTU12_64\np12\nsVhost\np13' \
                          '\nVzre-ubuntu12-64\np14\nsVversion\np15\nV8.0' \
                          '.5_GA_5839' \
                          '.NETWORK\np16\nsVrelease\np17\nV20130910124124' \
                          '\np18\nsVtype\np19\nVNETWORK\np20\nsVminorversion' \
                          '\np21\nV0\np22\nsss.'

        self.assertEqual(
            expected_result,
            pickle.dumps(self.response.get_response())
        )