""" Tests of the dict tool """

from unittest import TestCase
from pythonzimbra.tools import dict


class TestDict(TestCase):

    zimbra_dict = [
        {
            "n": "key1",
            "_content": "value1"
        },
        {
            "n": "key2",
            "_content": "value2"
        }
    ]

    def test_zimbra_to_python(self):

        """ Turn a zimbra-style dictionary into a python-style
        """

        python_dict = {
            "key1": "value1",
            "key2": "value2"
        }

        self.assertEqual(
            dict.zimbra_to_python(self.zimbra_dict),
            python_dict,
            "Invalid converted dictionary"
        )

    def test_get_value(self):

        """ Fetch a single value from a zimbra style dictionary
        """

        self.assertEqual(
            dict.get_value(self.zimbra_dict, "key2"),
            "value2",
            "Unexpected value returned"
        )

    def test_get_value_fault(self):

        """ Try to fetch a value, when the key doesn't exist.
        """

        self.assertIsNone(
            dict.get_value(self.zimbra_dict, "key3"),
            "Unexpected value returned"
        )
