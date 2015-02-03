""" Test administrative requests """

import random

from unittest import TestCase
import sys
from pythonzimbra.request_json import RequestJson
from pythonzimbra.communication import Communication
from pythonzimbra.request_xml import RequestXml
from pythonzimbra.response_json import ResponseJson
from pythonzimbra.response_xml import ResponseXml
from pythonzimbra.tools.dict import get_value
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
                config.get("admin_request_test", "admin_url"),
                config.get("admin_request_test", "admin_account"),
                config.get("admin_request_test", "admin_password"),
                config.get("admin_request_test", "admin_account_by"),
                admin_auth=True,
                request_type=request_type
            )

            if token is None:

                self.fail("Authentication with the configured settings "
                          "was not successful")

            # Create an account

            comm = Communication(config.get("admin_request_test", "admin_url"))

            if request_type == "xml":

                request = RequestXml()

            else:

                request = RequestJson()

            request.set_auth_token(token)

            test_account = config.get("admin_request_test", "test_account")

            if "TEMP" in test_account:

                # Generate a random number and add it to the test account

                random.seed()
                temp_account = random.randint(1000000, 5000000)

                test_account = test_account.replace("TEMP", str(temp_account))

            test_displayname = config.get(
                "admin_request_test",
                "test_displayname"
            )

            if sys.version < '3':

                # Create unicode string for py2

                test_displayname = test_displayname.decode("utf-8")

            request.add_request(
                "CreateAccountRequest",
                {
                    "name": test_account,
                    "password": config.get(
                        "admin_request_test",
                        "test_password"
                    ),
                    "a": {
                        "n": "displayName",
                        "_content": test_displayname
                    }
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
                    "CreateAccount faulted. (%s) %s" % (
                        response.get_fault_code(),
                        response.get_fault_message()
                    )
                )

            account_id = response.get_response(
            )["CreateAccountResponse"]["account"]["id"]

            # Get account from database and compare display name to the setting

            request.clean()
            request.set_auth_token(token)
            response.clean()

            request.add_request(
                "GetAccountRequest",
                {
                    "account": {
                        "by": "name",
                        "_content": test_account
                    }
                },
                "urn:zimbraAdmin"
            )

            comm.send_request(request, response)

            if response.is_fault():

                self.fail(
                    "GetAccount faulted. (%s) %s" % (
                        response.get_fault_code(),
                        response.get_fault_message()
                    )
                )

            returned_name = get_value(
                response.get_response()["GetAccountResponse"]["account"]["a"],
                "displayName"
            )

            self.assertEqual(
                returned_name,
                test_displayname,
                "Zimbra didn't save the display name as requested."
            )

            # Try to log in as the new account

            user_token = authenticate(
                config.get("admin_request_test", "url"),
                test_account,
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
                    "Cannot remove test account: (%s) %s" % (
                        response.get_fault_code(),
                        response.get_fault_message()
                    )
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

        self.run_admin_test("json")
