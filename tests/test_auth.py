""" Test the auth tool """

from unittest import TestCase
from tests import get_config
from pythonzimbra.tools.auth import authenticate


class TestAuth(TestCase):

    def test_auth_xml(self):

        """ Send a configured auth request in XML format and check a
        successfully returned token
        """

        config = get_config()

        if config.getboolean('auth_test', 'enabled'):

            # Run only if enabled

            try:

                timestamp = config.getint('auth_test', 'timestamp')

            except ValueError:

                # If timestamp is set to a none-integer, we'll just assume
                # that it's unset

                timestamp = None

            response = authenticate(
                config.get('auth_test', 'url'),
                config.get('auth_test', 'account'),
                config.get('auth_test', 'preauthkey'),
                config.get('auth_test', 'account_by'),
                config.getint('auth_test', 'expires'),
                timestamp
            )

            self.assertNotEqual(
                response,
                None,
                "Authentication with the configured settings "
                "was not successful"
            )

    def test_auth_failure_xml(self):

        """ Send a configured auth request with a wrong password in XML format
        and check the result
        """

        config = get_config()

        if config.getboolean('auth_test', 'enabled'):

            # Run only if enabled

            try:

                timestamp = config.getint('auth_test', 'timestamp')

            except ValueError:

                # If timestamp is set to a none-integer, we'll just assume
                # that it's unset

                timestamp = None

            response = authenticate(
                config.get('auth_test', 'url'),
                config.get('auth_test', 'account'),
                config.get('auth_test', 'preauthkey') + "1234",
                config.get('auth_test', 'account_by'),
                config.getint('auth_test', 'expires'),
                timestamp
            )

            self.assertEqual(
                response,
                None,
                "Authentication did not return 'None', but %s instead." % (
                    response
                )
            )

    def test_auth_json(self):

        """ Send a configured auth request in json format and check a
        successfully returned token
        """

        config = get_config()

        if config.getboolean('auth_test', 'enabled'):

            # Run only if enabled

            try:

                timestamp = config.getint('auth_test', 'timestamp')

            except ValueError:

                # If timestamp is set to a none-integer, we'll just assume
                # that it's unset

                timestamp = None

            response = authenticate(
                config.get('auth_test', 'url'),
                config.get('auth_test', 'account'),
                config.get('auth_test', 'preauthkey'),
                config.get('auth_test', 'account_by'),
                config.getint('auth_test', 'expires'),
                timestamp,
                request_type='json'
            )

            self.assertNotEqual(
                response,
                None,
                "Authentication with the configured settings "
                "was not successful"
            )

    def test_auth_failure_json(self):

        """ Send a configured auth request with a wrong password in json
        format and check the result
        """

        config = get_config()

        if config.getboolean('auth_test', 'enabled'):

            # Run only if enabled

            try:

                timestamp = config.getint('auth_test', 'timestamp')

            except ValueError:

                # If timestamp is set to a none-integer, we'll just assume
                # that it's unset

                timestamp = None

            response = authenticate(
                config.get('auth_test', 'url'),
                config.get('auth_test', 'account'),
                config.get('auth_test', 'preauthkey') + "1234",
                config.get('auth_test', 'account_by'),
                config.getint('auth_test', 'expires'),
                timestamp,
                request_type='json'
            )

            self.assertEqual(
                response,
                None,
                "Authentication did not return 'None', but %s instead." % (
                    response
                )
            )

    def test_password_auth_xml(self):

        """ Send a configured auth request in xml format using password
        based authentication and check a successfully returned token
        """

        config = get_config()

        if config.getboolean("auth_by_password_test", "enabled"):

            # Run only if enabled

            response = authenticate(
                config.get("auth_by_password_test", "url"),
                config.get("auth_by_password_test", "account"),
                config.get("auth_by_password_test", "password"),
                config.get("auth_by_password_test", "account_by"),
                use_password=True,
                request_type="xml"
            )

            self.assertNotEqual(
                response,
                None,
                "Authentication with the configured settings "
                "was not ssuccessful"
            )

    def test_password_auth_json(self):

        """ Send a configured auth request in json format using password
        based authentication and check a successfully returned token
        """

        config = get_config()

        if config.getboolean("auth_by_password_test", "enabled"):

            # Run only if enabled

            response = authenticate(
                config.get("auth_by_password_test", "url"),
                config.get("auth_by_password_test", "account"),
                config.get("auth_by_password_test", "password"),
                config.get("auth_by_password_test", "account_by"),
                use_password=True,
                request_type="json"
            )

            self.assertNotEqual(
                response,
                None,
                "Authentication with the configured settings "
                "was not ssuccessful"
            )

    def test_admin_auth_xml(self):

        """ Send a configured admin auth request in xml format using the
        admin auth-method and check a successfully returned token
        """

        config = get_config()

        if config.getboolean("admin_auth_test", "enabled"):

            # Run only if enabled

            response = authenticate(
                config.get("admin_auth_test", "admin_url"),
                config.get("admin_auth_test", "admin_account"),
                config.get("admin_auth_test", "admin_password"),
                config.get("admin_auth_test", "admin_account_by"),
                admin_auth=True,
                request_type="xml"
            )

            self.assertNotEqual(
                response,
                None,
                "Authentication with the configured settings "
                "was not successful"
            )

    def test_admin_auth_json(self):

        """ Send a configured admin auth request in json format using the
        admin auth-method and check a successfully returned token
        """

        config = get_config()

        if config.getboolean("admin_auth_test", "enabled"):

            # Run only if enabled

            response = authenticate(
                config.get("admin_auth_test", "admin_url"),
                config.get("admin_auth_test", "admin_account"),
                config.get("admin_auth_test", "admin_password"),
                config.get("admin_auth_test", "admin_account_by"),
                admin_auth=True,
                request_type="json"
            )

            self.assertNotEqual(
                response,
                None,
                "Authentication with the configured settings "
                "was not successful"
            )