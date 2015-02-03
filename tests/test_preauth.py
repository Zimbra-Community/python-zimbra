""" Test Preauth tool """
from unittest import TestCase
from pythonzimbra.tools import preauth


class TestPreauth(TestCase):

    def test_create_preauth(self):

        """ Test creating a preauth

        This is mostly bogus, as the return value cannot be tested against
        something senseful. It's just tested if the method can be called and
        it returns a str.
        """

        # Test with default parameters

        pak = preauth.create_preauth('user@company.com', '1234567890abcdef')

        self.assertIsInstance(
            pak,
            str,
            'Returned preauth 1 is not of type str but of type %s' % (
                type(pak)
            )
        )

        # Test with full (bogus) parameters

        pak = preauth.create_preauth(
            'user@company.com',
            '1234567890abcdef',
            999,
            12345
        )

        self.assertIsInstance(
            pak,
            str,
            'Returned preauth 2 is not of type str but of type %s' % (
                type(pak)
            )
        )
