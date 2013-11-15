""" Request tests """

from unittest import TestCase
from pythonzimbra.request_xml import RequestXml
from pythonzimbra.exceptions.request import \
    NoNamespaceGiven, RequestHeaderContextException


class TestRequest(TestCase):
    """ Request tests
    """

    request = None

    """ The request to be tested against """

    def cleanUp(self):
        """ Clean up after one step to leave a dedicated result for the other
         test cases.
        """
        self.setUp()

    def setUp(self):
        self.request = RequestXml()

    def test_empty_request(self):
        """ Create an empty request and check the created xml
        """

        expected_result = '<?xml version="1.0" ?><soap:Envelope ' \
                          'xmlns:soap="http://www.w3' \
                          '.org/2003/05/soap-envelope"><soap:Header><context' \
                          ' xmlns="urn:zimbra"><format ' \
                          'type="xml"/></context></soap:Header><soap:Body' \
                          '/></soap:Envelope>'

        self.assertEqual(
            expected_result,
            self.request.get_request(),
            "Empty request not as expected. Expected: %s. Got: %s" % (
                expected_result,
                self.request.get_request()
            )
        )

    def test_set_context_params_failtype(self):
        """ Add context parameters to the request and expect the method to
        send an exception
        """

        self.assertRaises(
            RequestHeaderContextException,
            self.request.set_context_params,
            {
                'invalidParam': {
                    'invalidAttribute': 'invalidValue'
                }
            }
        )

    def test_set_context_params(self):
        """ Add all currently accepted params and check the result
        """

        self.request.set_context_params(
            {
                'authToken': {
                    '_content': '1234567890abcdef'
                },
                'authTokenControl': {
                    'voidOnExpired': '1'
                },
                'session': {
                    'id': '1234567890abcdef',
                    'seq': '1234567890',
                    'type': 'admin'
                },
                'account': {
                    'by': 'name',
                    '_content': 'user@zimbra.com'
                },
                'change': {
                    'token': '1234567890abcdef',
                    'type': 'new'
                },
                'targetServer': {
                    '_content': 'mailboxserver.zimbra.com'
                },
                'userAgent': {
                    'name': 'Mozilla',
                    'version': '1.0'
                },
                'via': {
                    '_content': 'proxyserver.zimbra.com'
                }
            }
        )

        expected_result = '<?xml version="1.0" ?><soap:Envelope ' \
                          'xmlns:soap="http://www.w3' \
                          '.org/2003/05/soap-envelope"><soap:Header><context ' \
                          'xmlns="urn:zimbra"><format ' \
                          'type="xml"/><authToken>1234567890abcdef</authToken' \
                          '><account by="name">user@zimbra' \
                          '.com</account><session id="1234567890abcdef" ' \
                          'seq="1234567890" type="admin"/><authTokenControl ' \
                          'voidOnExpired="1"/><targetServer>mailboxserver' \
                          '.zimbra.com</targetServer><via>proxyserver.zimbra' \
                          '.com</via><userAgent name="Mozilla" version="1' \
                          '.0"/><change token="1234567890abcdef" ' \
                          'type="new"/></context></soap:Header><soap:Body' \
                          '/></soap:Envelope>'

        self.assertEqual(
            expected_result,
            self.request.get_request(),
            'Unexpected result. Expected: %s. Got: %s' % (
                expected_result,
                self.request.get_request()
            )
        )

        # Clean up after this test

        self.cleanUp()

    def test_enable_batch_default(self):

        """ Test enabling batch requests
        """

        # Check with default parameter

        self.request.enable_batch('urn:zimbra')

        expected_result = '<?xml version="1.0" ?><soap:Envelope ' \
                          'xmlns:soap="http://www.w3' \
                          '.org/2003/05/soap-envelope"><soap:Header><context ' \
                          'xmlns="urn:zimbra"><format ' \
                          'type="xml"/></context></soap:Header><soap:Body' \
                          '><BatchRequest onerror="continue" ' \
                          'xmlns="urn:zimbra"/></soap:Body></soap:Envelope>'

        self.assertEqual(
            expected_result,
            self.request.get_request(),
            'Unexpected result with default parameter (continue): Expected %s'
            '. Got %s' % (
                expected_result,
                self.request.get_request()
            )
        )

        # Clean up

        self.cleanUp()

    def test_enable_batch_stop(self):

        """ Test enabling batch requests with additional parameter
        """

        self.request.enable_batch('urn:zimbra', 'stop')

        expected_result = '<?xml version="1.0" ?><soap:Envelope ' \
                          'xmlns:soap="http://www.w3' \
                          '.org/2003/05/soap-envelope"><soap:Header><context ' \
                          'xmlns="urn:zimbra"><format ' \
                          'type="xml"/></context></soap:Header><soap:Body' \
                          '><BatchRequest onerror="stop" ' \
                          'xmlns="urn:zimbra"/></soap:Body></soap:Envelope>'

        self.assertEqual(
            expected_result,
            self.request.get_request(),
            'Unexpected result with parameter "stop": Expected %s'
            '. Got %s' % (
                expected_result,
                self.request.get_request()
            )
        )

        # Clean up

        self.cleanUp()

    def test_batch_add_request(self):

        """ Test adding multiple request to a batch request
        """

        self.request.enable_batch('urn:zimbra')

        request_id = self.request.add_request(
            'GetInfoRequest',
            {
                'sections': 'mbox,prefs'
            }
        )

        self.assertIsInstance(
            request_id,
            int,
            msg="Returned request_id for request 1 is not of type int, "
                "but of type %s" % (
                type(request_id)
            )
        )

        self.assertEqual(
            1,
            request_id,
            msg="Returned request_id for request 1 is not 1, but %s" % (
                str(request_id)
            )
        )

        expected_result = '<?xml version="1.0" ?><soap:Envelope ' \
                          'xmlns:soap="http://www.w3' \
                          '.org/2003/05/soap-envelope"><soap:Header><context ' \
                          'xmlns="urn:zimbra"><format ' \
                          'type="xml"/></context></soap:Header><soap:Body' \
                          '><BatchRequest onerror="continue" ' \
                          'xmlns="urn:zimbra"><GetInfoRequest requestId="1" ' \
                          'sections="mbox,' \
                          'prefs"/></BatchRequest></soap:Body></soap:Envelope>'

        self.assertEqual(
            expected_result,
            self.request.get_request(),
            "Got unexpected result after adding request 1. Expected: %s, "
            "Got: %s" % (
                expected_result,
                self.request.get_request(),
            )
        )

        request_id = self.request.add_request(
            'GetInfoRequest',
            {
                'sections': 'zimlets'
            }
        )

        self.assertIsInstance(
            request_id,
            int,
            msg="Returned request_id for request 2 is not of type int, "
                "but of type %s" % (
                type(request_id)
            )
        )

        self.assertEqual(
            2,
            request_id,
            msg="Returned request_id for request 2 is not 2, but %s" % (
                str(request_id)
            )
        )

        expected_result = '<?xml version="1.0" ?><soap:Envelope ' \
                          'xmlns:soap="http://www.w3' \
                          '.org/2003/05/soap-envelope"><soap:Header><context ' \
                          'xmlns="urn:zimbra"><format ' \
                          'type="xml"/></context></soap:Header><soap:Body' \
                          '><BatchRequest onerror="continue" ' \
                          'xmlns="urn:zimbra"><GetInfoRequest requestId="1" ' \
                          'sections="mbox,prefs"/><GetInfoRequest ' \
                          'requestId="2" ' \
                          'sections="zimlets"/></BatchRequest></soap:Body' \
                          '></soap:Envelope>'

        self.assertEqual(
            expected_result,
            self.request.get_request(),
            "Got unexpected result after adding request 2. Expected: %s, "
            "Got: %s" % (
                expected_result,
                self.request.get_request(),
            )
        )

        # Clean up

        self.setUp()

    def test_add_request_missing_xmlns(self):

        """ Test adding a request without specifying a XML namespace
        """

        self.assertRaises(
            NoNamespaceGiven,
            self.request.add_request,
            'GetInfoRequest',
            {
                'sections': 'mbox,prefs'
            }
        )

    def test_add_request(self):

        """ Test adding a request
        """

        request_id = self.request.add_request(
            'GetInfoRequest',
            {
                'sections': 'mbox,prefs'
            },
            'urn:zimbra'
        )

        self.assertIsNone(
            request_id,
            msg="Returned request_id for request 1 is not none, "
                "but %s" % (
                    str(request_id)
                )
        )

        expected_result = '<?xml version="1.0" ?><soap:Envelope ' \
                          'xmlns:soap="http://www.w3' \
                          '.org/2003/05/soap-envelope"><soap:Header><context ' \
                          'xmlns="urn:zimbra"><format ' \
                          'type="xml"/></context></soap:Header><soap:Body' \
                          '><GetInfoRequest sections="mbox,' \
                          'prefs" ' \
                          'xmlns="urn:zimbra"/></soap:Body></soap:Envelope>'

        self.assertEqual(
            expected_result,
            self.request.get_request(),
            "Got unexpected result after adding request. Expected: %s, "
            "Got: %s" % (
                expected_result,
                self.request.get_request(),
            )
        )

        # Clean up

        self.setUp()

    def tearDown(self):
        self.request = None