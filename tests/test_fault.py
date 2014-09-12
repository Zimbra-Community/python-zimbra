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
                response
            )

    def test_fault_non_existing_folder_batch_json(self):

        """ Request a non existing folder multiple times to get multiple
        faults
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

            request.enable_batch()

            request.add_request(
                "GetFolderRequest",
                {
                    "folder": {
                        "path": config.get('fault_test', 'folder')
                    }
                },
                "urn:zimbraMail"
            )

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
                response
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
                response
            )

    def test_fault_non_existing_folder_batch_xml(self):

        """ Request a non existing folder multiple times to get multiple
        faults
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

            request.enable_batch()

            request.add_request(
                "GetFolderRequest",
                {
                    "folder": {
                        "path": config.get('fault_test', 'folder')
                    }
                },
                "urn:zimbraMail"
            )

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
                response
            )

    def checkResponse(self, response):

        # Should be a fault

        self.assertEqual(
            True,
            response.is_fault()
        )

        config = get_config()

        message = "no such folder path: %s" % config.get('fault_test', 'folder')

        if response.is_batch():

            # Correct error should've been returned

            for request_id, code in response.get_fault_code().iteritems():

                self.assertEqual(
                    "mail.NO_SUCH_FOLDER",
                    code
                )

            # Correct error message should've been returned

            for request_id, fault_message in response.get_fault_message().iteritems():

                self.assertEqual(
                    message,
                    fault_message
                )

        else:

            # Correct error should've been returned

            self.assertEqual(
                "mail.NO_SUCH_FOLDER",
                response.get_fault_code()
            )

            # Correct error message should've been returned

            self.assertEqual(
                message,
                response.get_fault_message()
            )

    def tearDown(self):
        self.request = None