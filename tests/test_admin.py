""" Test administrative requests """

from unittest import TestCase
from pythonzimbra.request_json import RequestJson
from pythonzimbra.communication import Communication
from pythonzimbra.request_xml import RequestXml
from pythonzimbra.response_json import ResponseJson
from pythonzimbra.response_xml import ResponseXml
from tests import get_config
from pythonzimbra.tools.auth import authenticate


class TestAdmin(TestCase):

    def run_admin_test(self, request_type):

        """ Actually do the work
        """

        config = get_config()

        if config.getboolean("admin_request_test", "enabled"):

            # Run only if enabled

            token = authenticate(
                config.get("admin_request_test", "url"),
                config.get("admin_request_test", "account"),
                config.get("admin_request_test", "password"),
                config.get("admin_request_test", "account_by"),
                admin_auth=True,
                request_type=request_type
            )

            if token is None:

                self.fail("Authentication with the configured settings "
                          "was not successful")

            # Create an account

            comm = Communication(config.get("admin_request_test", "url"))

            if request_type == "xml":

                request = RequestXml()

            else:

                request = RequestJson()

            request.set_auth_token(token)

            request.add_request(
                "CreateAccountRequest",
                {
                    "name": config.get("admin_request_test", "test_account"),
                    "password": config.get(
                        "admin_request_test",
                        "test_password"
                    )
                },
                "urn:zimbraAdmin"
            )

            if request_type == "xml":

                response = ResponseXml()

            else:

                response = ResponseJson()

            comm.send_request(request, response)

            if response.is_fault():

                self.fail(
                    "CreateAccount faulted. %s" % (response.get_response())
                )

            account_id = response.get_response(
            )["CreateAccountResponse"]["account"]["id"]

            # Try to log in as the new account

            user_token = authenticate(
                config.get("admin_request_test", "user_url"),
                config.get("admin_request_test", "test_account"),
                config.get("admin_request_test", "test_password"),
                "name",
                request_type=request_type,
                use_password=True
            )

            if user_token is None:

                self.fail("Cannot log in as the test user.")

            # Remove account

            request.clean()
            response.clean()
            request.set_auth_token(token)

            request.add_request(
                "DeleteAccountRequest",
                {
                    "id": account_id
                },
                "urn:zimbraAdmin"
            )

            comm.send_request(request, response)

            if response.is_fault():

                self.fail(
                    "Cannot remove test account. %s" % response.get_response()
                )

    def test_admin_xml(self):

        """ Creates a new account, authenticates as this account and deletes
        it afterwards. Assumes, that this works correctly (in xml format)
        """

        self.run_admin_test("xml")

    def test_admin_json(self):

        """ Creates a new account, authenticates as this account and deletes
        it afterwards. Assumes, that this works correctly (in json format)
        """

        self.run_admin_test("xml")