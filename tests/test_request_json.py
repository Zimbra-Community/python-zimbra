""" Request tests """
import json

from unittest import TestCase
from pythonzimbra.request_json import RequestJson
from pythonzimbra.exceptions.request import \
    NoNamespaceGiven, RequestHeaderContextException


class TestRequestJson(TestCase):
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
        self.request = RequestJson()

    def test_empty_request(self):
        """ Create an empty request and check the created xml
        """

        expected_result = {
            "Body": {},
            "Header": {
                "context": {
                    "_jsns": "urn:zimbra",
                    "format": {
                        "type": "js"
                    }
                }
            }
        }

        self.assertEqual(
            expected_result,
            json.loads(self.request.get_request())
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

        expected_result = {
            "Body": {},
            "Header": {
                "context": {
                    "authToken": {
                        "_content": "1234567890abcdef"
                    },
                    "account": {
                        "by": "name",
                        "_content": "user@zimbra.com"
                    },
                    "via": {
                        "_content": "proxyserver.zimbra.com"
                    },
                    "targetServer": {
                        "_content": "mailboxserver.zimbra.com"
                    },
                    "format": {
                        "type": "js"
                    },
                    "_jsns": "urn:zimbra",
                    "session": {
                        "type": "admin",
                        "id": "1234567890abcdef",
                        "seq": "1234567890"
                    },
                    "authTokenControl": {
                        "voidOnExpired": "1"
                    },
                    "userAgent": {
                        "version": "1.0",
                        "name": "Mozilla"
                    },
                    "change": {
                        "token": "1234567890abcdef",
                        "type": "new"
                    }
                }
            }
        }

        self.assertEqual(
            expected_result,
            json.loads(self.request.get_request())
        )

        # Clean up after this test

        self.cleanUp()

    def test_enable_batch_default(self):

        """ Test enabling batch requests
        """

        # Check with default parameter

        self.request.enable_batch()

        expected_result = {
            "Body": {
                "BatchRequest": {
                    "onerror": "continue",
                    "_jsns": "urn:zimbra"
                }
            },
            "Header": {
                "context": {
                    "_jsns": "urn:zimbra",
                    "format": {
                        "type": "js"
                    }
                }
            }
        }

        self.assertEqual(
            expected_result,
            json.loads(self.request.get_request())
        )

        # Clean up

        self.cleanUp()

    def test_enable_batch_stop(self):

        """ Test enabling batch requests with additional parameter
        """

        self.request.enable_batch('stop')

        expected_result = {
            "Body": {
                "BatchRequest": {
                    "onerror": "stop",
                    "_jsns": "urn:zimbra"
                }
            },
            "Header": {
                "context": {
                    "_jsns": "urn:zimbra",
                    "format": {
                        "type": "js"
                    }
                }
            }
        }

        self.assertEqual(
            expected_result,
            json.loads(self.request.get_request())
        )

        # Clean up

        self.cleanUp()

    def test_batch_add_request(self):

        """ Test adding multiple request to a batch request
        """

        self.request.enable_batch()

        request_id = self.request.add_request(
            'GetInfoRequest',
            {
                'sections': 'mbox,prefs'
            },
            "urn_zimbra"
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

        expected_result = {
            "Body": {
                "BatchRequest": {
                    "onerror": "continue",
                    "_jsns": "urn:zimbra",
                    "GetInfoRequest": {
                        "_jsns": "urn_zimbra",
                        "sections": "mbox,prefs",
                        "requestId": 1
                    }
                }
            },
            "Header": {
                "context": {
                    "_jsns": "urn:zimbra",
                    "format": {
                        "type": "js"
                    }
                }
            }
        }

        self.assertEqual(
            expected_result,
            json.loads(self.request.get_request())
        )

        request_id = self.request.add_request(
            'GetInfoRequest',
            {
                'sections': 'zimlets'
            },
            "urn:zimbra"
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

        expected_result = {
            "Body": {
                "BatchRequest": {
                    "onerror": "continue",
                    "_jsns": "urn:zimbra",
                    "GetInfoRequest": [
                        {
                            "_jsns": "urn_zimbra",
                            "sections": "mbox,prefs",
                            "requestId": 1
                        },
                        {
                            "_jsns": "urn:zimbra",
                            "sections": "zimlets",
                            "requestId": 2
                        }
                    ]
                }
            },
            "Header": {
                "context": {
                    "_jsns": "urn:zimbra",
                    "format": {
                        "type": "js"
                    }
                }
            }
        }

        self.assertEqual(
            expected_result,
            json.loads(self.request.get_request())
        )

        # Clean up

        self.setUp()

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

        expected_result = {
            "Body": {
                "GetInfoRequest": {
                    "_jsns": "urn:zimbra",
                    "sections": "mbox,prefs"
                }
            },
            "Header": {
                "context": {
                    "_jsns": "urn:zimbra",
                    "format": {
                        "type": "js"
                    }
                }
            }
        }

        self.assertEqual(
            expected_result,
            json.loads(self.request.get_request())
        )

        # Clean up

        self.setUp()

    def tearDown(self):
        self.request = None
