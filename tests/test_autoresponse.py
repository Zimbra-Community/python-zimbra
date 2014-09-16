""" Test, wether send_request can create a request automatically on its own
"""
from unittest import TestCase
from pythonzimbra.request_json import RequestJson
from pythonzimbra.request_xml import RequestXml
from pythonzimbra.tools.auth import authenticate
from pythonzimbra.communication import Communication
from tests import get_config


class TestAutoresponse(TestCase):

    def test_autoresponse_json(self):

        """ Create a JSON-request and pass this to send_request expection a
        json response.
        """

        config = get_config()

        if config.getboolean("autoresponse_test", "enabled"):

            # Run only if enabled

            token = authenticate(
                config.get("autoresponse_test", "url"),
                config.get("autoresponse_test", "account"),
                config.get("autoresponse_test", "preauthkey")
            )

            self.assertNotEqual(
                token,
                None,
                "Cannot authenticate."
            )

            request = RequestJson()
            request.set_auth_token(token)
            request.add_request(
                "NoOpRequest",
                {

                },
                "urn:zimbraMail"
            )

            comm = Communication(config.get("autoresponse_test", "url"))

            response = comm.send_request(request)

            if response.is_fault():

                self.fail(
                    "Reponse failed: (%s) %s" % (
                        response.get_fault_code(),
                        response.get_fault_message()
                    )
                )

            self.assertEqual(
                response.response_type,
                "json",
                "Invalid response type %s" % response.response_type
            )

    def test_autoresponse_xml(self):

        """ Create an XML-request and pass this to send_request expection a
        xml response.
        """

        config = get_config()

        if config.getboolean("autoresponse_test", "enabled"):

            # Run only if enabled

            token = authenticate(
                config.get("autoresponse_test", "url"),
                config.get("autoresponse_test", "account"),
                config.get("autoresponse_test", "preauthkey")
            )

            self.assertNotEqual(
                token,
                None,
                "Cannot authenticate."
            )

            request = RequestXml()
            request.set_auth_token(token)
            request.add_request(
                "NoOpRequest",
                {

                },
                "urn:zimbraMail"
            )

            comm = Communication(config.get("autoresponse_test", "url"))

            response = comm.send_request(request)

            if response.is_fault():

                self.fail(
                    "Reponse failed: (%s) %s" % (
                        response.get_fault_code(),
                        response.get_fault_message()
                    )
                )

            self.assertEqual(
                response.response_type,
                "xml",
                "Invalid response type %s" % response.response_type
            )