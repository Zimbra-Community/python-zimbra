""" Test the auth tool """

from unittest import TestCase
from tests import get_config
from pythonzimbra.tools.auth import authenticate


class TestAuth(TestCase):

        def test_auth(self):

            """ Send a configured auth request and check a successfully
            returned token
            """

            config = get_config()

            if config.get('auth_test', 'enabled'):

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

                if response is None:

                    self.fail("Authentication with the configured settings "
                              "was not successful")