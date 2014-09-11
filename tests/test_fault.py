""" Fault tests """

from unittest import TestCase
from tests import get_config
from pythonzimbra.tools import auth
from pythonzimbra.request_xml import RequestXml
from pythonzimbra.response_xml import ResponseXml
from pythonzimbra.request_json import RequestJson
from pythonzimbra.response_json import ResponseJson
from pythonzimbra.communication import Communication


class TestRequestFault(TestCase):
    """ Fault tests
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

    def test_fault_non_existing_folder_json(self):
        """ Request a non existing folder, so we get a fitting fault
        """

        config = get_config()

        if config.getboolean('fault_test', 'enabled'):

            comm = Communication(config.get('fault_test', 'url'))

            token = auth.authenticate(config.get('fault_test', 'url'),
                                      config.get('fault_test', 'account'),
                                      config.get('fault_test', 'preauthkey'),
                                      config.get('fault_test', 'account_by'))

            request = RequestJson()

            request.set_auth_token(token)

            request.add_request(
                "GetFolderRequest",
                {
                    "folder": {
                        "path": config.get('fault_test', 'folder')
                    }
                },
                "urn:zimbraMail"
            )

            response = ResponseJson()

            comm.send_request(request, response)

            self.checkResponse(
                response,
                response.get_response()["Fault"]["Detail"]["Error"]["Code"]
            )

    def test_fault_non_existing_folder_xml(self):
        """ Request a non existing folder, so we get a fitting fault
        """

        config = get_config()

        if config.getboolean('fault_test', 'enabled'):

            comm = Communication(config.get('fault_test', 'url'))

            token = auth.authenticate(config.get('fault_test', 'url'),
                                      config.get('fault_test', 'account'),
                                      config.get('fault_test', 'preauthkey'),
                                      config.get('fault_test', 'account_by'))

            request = RequestXml()

            request.set_auth_token(token)

            request.add_request(
                "GetFolderRequest",
                {
                    "folder": {
                        "path": config.get('fault_test', 'folder')
                    }
                },
                "urn:zimbraMail"
            )

            response = ResponseXml()

            comm.send_request(request, response)

            self.checkResponse(
                response,
                response.get_response()["Fault"]["Detail"]["Error"]["Code"][
                    "_content"]
            )

    def checkResponse(self, response, compare_value):

        # Should be a fault

        self.assertEqual(
            True,
            response.is_fault()
        )

        # Correct error should've been returned

        self.assertEqual(
            "mail.NO_SUCH_FOLDER",
            compare_value
        )

    def tearDown(self):
        self.request = None