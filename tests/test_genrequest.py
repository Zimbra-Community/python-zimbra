""" Test usage of communication.authenticate and communication.gen_request
"""
from unittest import TestCase
from pythonzimbra.exceptions.communication import UnknownRequestType
from pythonzimbra.request_json import RequestJson
from pythonzimbra.request_xml import RequestXml
from pythonzimbra.tools.auth import authenticate
from pythonzimbra.communication import Communication
from tests import get_config


class TestGenrequest(TestCase):

    def test_genrequest_default(self):

        """ Create a request only using the Communication-object
        """

        config = get_config()

        if config.getboolean("genrequest_test", "enabled"):

            # Run only if enabled

            comm = Communication(config.get("genrequest_test", "url"))

            token = authenticate(
                config.get("genrequest_test", "url"),
                config.get("genrequest_test", "account"),
                config.get("genrequest_test", "preauthkey")
            )

            self.assertNotEqual(
                token,
                None,
                "Cannot authenticate."
            )

            request = comm.gen_request(token=token)

            request.add_request(
                "NoOpRequest",
                {

                },
                "urn:zimbraMail"
            )

            response = comm.send_request(request)

            if response.is_fault():

                self.fail(
                    "Reponse failed: (%s) %s" % (
                        response.get_fault_code(),
                        response.get_fault_message()
                    )
                )

    def test_genrequest_fail(self):

        """ Create a request only using the Communication-object
        """

        config = get_config()

        if config.getboolean("genrequest_test", "enabled"):

            # Run only if enabled

            comm = Communication(config.get("genrequest_test", "url"))

            token = authenticate(
                config.get("genrequest_test", "url"),
                config.get("genrequest_test", "account"),
                config.get("genrequest_test", "preauthkey")
            )

            self.assertNotEqual(
                token,
                None,
                "Cannot authenticate."
            )

            self.assertRaises(
                UnknownRequestType,
                comm.gen_request,
                request_type="INVALID",
                token=token
            )

            request = comm.gen_request(token=token)

            request.add_request(
                "NoOpRequest",
                {

                },
                "urn:zimbraMail"
            )

            # Deliberately break the request

            request.request_type = "INVALID"

            self.assertRaises(
                UnknownRequestType,
                comm.send_request,
                request
            )

    def test_genrequest_xml(self):

        """ Create a request only using the Communication-object
        """

        config = get_config()

        if config.getboolean("genrequest_test", "enabled"):

            # Run only if enabled

            comm = Communication(config.get("genrequest_test", "url"))

            token = authenticate(
                config.get("genrequest_test", "url"),
                config.get("genrequest_test", "account"),
                config.get("genrequest_test", "preauthkey")
            )

            self.assertNotEqual(
                token,
                None,
                "Cannot authenticate."
            )

            request = comm.gen_request(request_type="xml", token=token)

            request.add_request(
                "NoOpRequest",
                {

                },
                "urn:zimbraMail"
            )

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

    def test_genrequest_batch(self):

        """ Create a batch-request only using the Communication-object
        """

        config = get_config()

        if config.getboolean("genrequest_test", "enabled"):

            # Run only if enabled

            comm = Communication(config.get("genrequest_test", "url"))

            token = authenticate(
                config.get("genrequest_test", "url"),
                config.get("genrequest_test", "account"),
                config.get("genrequest_test", "preauthkey")
            )

            self.assertNotEqual(
                token,
                None,
                "Cannot authenticate."
            )

            request = comm.gen_request(token=token, set_batch=True)

            self.assertEqual(
                type(request),
                RequestJson,
                "Generated request wasn't an json-request, which should be "
                "the default."
            )

            request.add_request(
                "NoOpRequest",
                {

                },
                "urn:zimbraMail"
            )

            request.add_request(
                "NoOpRequest",
                {

                },
                "urn:zimbraMail"
            )

            response = comm.send_request(request)

            if response.is_fault():

                self.fail(
                    "Reponse failed: (%s) %s" % (
                        response.get_fault_code(),
                        response.get_fault_message()
                    )
                )

            self.assertEqual(
                response.is_batch(),
                True,
                "Batch-request didn't return a Batch response."
            )

            expected_batch = {
                'nameToId': {
                    'NoOpResponse': [
                        '1',
                        '2'
                    ]
                },
                'hasFault': False,
                'idToName': {
                    '1': 'NoOpResponse',
                    '2': 'NoOpResponse'
                }
            }

            self.assertEqual(
                response.get_batch(),
                expected_batch,
                "Batch-dictionary wasn't expected"
            )

    def test_genrequest_batch_xml(self):

        """ Create a batch-request only using the Communication-object (
            xml-version)
        """

        config = get_config()

        if config.getboolean("genrequest_test", "enabled"):

            # Run only if enabled

            comm = Communication(config.get("genrequest_test", "url"))

            token = authenticate(
                config.get("genrequest_test", "url"),
                config.get("genrequest_test", "account"),
                config.get("genrequest_test", "preauthkey")
            )

            self.assertNotEqual(
                token,
                None,
                "Cannot authenticate."
            )

            request = comm.gen_request(
                request_type="xml",
                token=token,
                set_batch=True
            )

            self.assertEqual(
                type(request),
                RequestXml,
                "Generated request wasn't an xml-request"
            )

            request.add_request(
                "NoOpRequest",
                {

                },
                "urn:zimbraMail"
            )

            request.add_request(
                "NoOpRequest",
                {

                },
                "urn:zimbraMail"
            )

            response = comm.send_request(request)

            if response.is_fault():

                self.fail(
                    "Reponse failed: (%s) %s" % (
                        response.get_fault_code(),
                        response.get_fault_message()
                    )
                )

            self.assertEqual(
                response.is_batch(),
                True,
                "Batch-request didn't return a Batch response."
            )

            expected_batch = {
                'nameToId': {
                    'NoOpResponse': [
                        '1',
                        '2'
                    ]
                },
                'hasFault': False,
                'idToName': {
                    '1': 'NoOpResponse',
                    '2': 'NoOpResponse'
                }
            }

            self.assertEqual(
                response.get_batch(),
                expected_batch,
                "Batch-dictionary wasn't expected"
            )

    def test_genrequest_check_response(self):

        """ Create a request only using the Communication-object, send it and
            check the response
        """

        config = get_config()

        if config.getboolean("genrequest_test", "enabled"):

            # Run only if enabled

            comm = Communication(config.get("genrequest_test", "url"))

            token = authenticate(
                config.get("genrequest_test", "url"),
                config.get("genrequest_test", "account"),
                config.get("genrequest_test", "preauthkey")
            )

            self.assertNotEqual(
                token,
                None,
                "Cannot authenticate."
            )

            request = comm.gen_request(token=token)

            request.add_request(
                "GetInfoRequest",
                {
                },
                "urn:zimbraAccount"
            )

            response = comm.send_request(request)

            if response.is_fault():

                self.fail(
                    "Reponse failed: (%s) %s" % (
                        response.get_fault_code(),
                        response.get_fault_message()
                    )
                )

            self.assertEqual(
                response.get_response()["GetInfoResponse"]["name"],
                config.get("genrequest_test", "account"),
                "Request returned unexpected response"
            )

    def test_genrequest_check_response_batch(self):

        """ Create a batch-request only using the Communication-object
        """

        config = get_config()

        if config.getboolean("genrequest_test", "enabled"):

            # Run only if enabled

            comm = Communication(config.get("genrequest_test", "url"))

            token = authenticate(
                config.get("genrequest_test", "url"),
                config.get("genrequest_test", "account"),
                config.get("genrequest_test", "preauthkey")
            )

            self.assertNotEqual(
                token,
                None,
                "Cannot authenticate."
            )

            request = comm.gen_request(token=token, set_batch=True)

            self.assertEqual(
                type(request),
                RequestJson,
                "Generated request wasn't an json-request, which should be "
                "the default."
            )

            request.add_request(
                "NoOpRequest",
                {

                },
                "urn:zimbraMail"
            )

            request.add_request(
                "GetInfoRequest",
                {
                },
                "urn:zimbraAccount"
            )

            response = comm.send_request(request)

            if response.is_fault():

                self.fail(
                    "Reponse failed: (%s) %s" % (
                        response.get_fault_code(),
                        response.get_fault_message()
                    )
                )

            self.assertEqual(
                response.get_response(2)["GetInfoResponse"]["name"],
                config.get("genrequest_test", "account"),
                "Request returned unexpected response"
            )

    def test_genrequest_check_response_xml(self):

        """ Create a request only using the Communication-object, send it and
            check the response
        """

        config = get_config()

        if config.getboolean("genrequest_test", "enabled"):

            # Run only if enabled

            comm = Communication(config.get("genrequest_test", "url"))

            token = authenticate(
                config.get("genrequest_test", "url"),
                config.get("genrequest_test", "account"),
                config.get("genrequest_test", "preauthkey")
            )

            self.assertNotEqual(
                token,
                None,
                "Cannot authenticate."
            )

            request = comm.gen_request(request_type="xml", token=token)

            request.add_request(
                "GetInfoRequest",
                {
                },
                "urn:zimbraAccount"
            )

            response = comm.send_request(request)

            if response.is_fault():

                self.fail(
                    "Reponse failed: (%s) %s" % (
                        response.get_fault_code(),
                        response.get_fault_message()
                    )
                )

            self.assertEqual(
                response.get_response()["GetInfoResponse"]["name"],
                config.get("genrequest_test", "account"),
                "Request returned unexpected response"
            )

    def test_genrequest_check_response_batch_xml(self):

        """ Create a batch-request only using the Communication-object
        """

        config = get_config()

        if config.getboolean("genrequest_test", "enabled"):

            # Run only if enabled

            comm = Communication(config.get("genrequest_test", "url"))

            token = authenticate(
                config.get("genrequest_test", "url"),
                config.get("genrequest_test", "account"),
                config.get("genrequest_test", "preauthkey")
            )

            self.assertNotEqual(
                token,
                None,
                "Cannot authenticate."
            )

            request = comm.gen_request(
                request_type="xml",
                token=token,
                set_batch=True
            )

            self.assertEqual(
                type(request),
                RequestXml,
                "Generated request wasn't an json-request, which should be "
                "the default."
            )

            request.add_request(
                "NoOpRequest",
                {

                },
                "urn:zimbraMail"
            )

            request.add_request(
                "GetInfoRequest",
                {
                },
                "urn:zimbraAccount"
            )

            response = comm.send_request(request)

            if response.is_fault():

                self.fail(
                    "Reponse failed: (%s) %s" % (
                        response.get_fault_code(),
                        response.get_fault_message()
                    )
                )

            self.assertEqual(
                response.get_response(2)["GetInfoResponse"]["name"],
                config.get("genrequest_test", "account"),
                "Request returned unexpected response"
            )

    def test_genrequest_batch_invalid(self):

        """ Create a batchrequest only using the Communication-object,
            send it and request an invalid request id
        """

        config = get_config()

        if config.getboolean("genrequest_test", "enabled"):

            # Run only if enabled

            comm = Communication(config.get("genrequest_test", "url"))

            token = authenticate(
                config.get("genrequest_test", "url"),
                config.get("genrequest_test", "account"),
                config.get("genrequest_test", "preauthkey")
            )

            self.assertNotEqual(
                token,
                None,
                "Cannot authenticate."
            )

            request = comm.gen_request(token=token, set_batch=True)

            self.assertEqual(
                type(request),
                RequestJson,
                "Generated request wasn't an json-request, which should be "
                "the default."
            )

            request.add_request(
                "NoOpRequest",
                {

                },
                "urn:zimbraMail"
            )

            request.add_request(
                "NoOpRequest",
                {

                },
                "urn:zimbraMail"
            )

            response = comm.send_request(request)

            if response.is_fault():

                self.fail(
                    "Reponse failed: (%s) %s" % (
                        response.get_fault_code(),
                        response.get_fault_message()
                    )
                )

            self.assertIsNone(
                response.get_response(3),
                "Querying an invalid requestId didn't return None"
            )

    def test_genrequest_batch_invalid_xml(self):

        """ Create a batchrequest only using the Communication-object,
            send it and request an invalid request id (xml)
        """

        config = get_config()

        if config.getboolean("genrequest_test", "enabled"):

            # Run only if enabled

            comm = Communication(config.get("genrequest_test", "url"))

            token = authenticate(
                config.get("genrequest_test", "url"),
                config.get("genrequest_test", "account"),
                config.get("genrequest_test", "preauthkey")
            )

            self.assertNotEqual(
                token,
                None,
                "Cannot authenticate."
            )

            request = comm.gen_request(
                request_type="xml",
                token=token,
                set_batch=True
            )

            self.assertEqual(
                type(request),
                RequestXml,
                "Generated request wasn't an json-request, which should be "
                "the default."
            )

            request.add_request(
                "NoOpRequest",
                {

                },
                "urn:zimbraMail"
            )

            request.add_request(
                "NoOpRequest",
                {

                },
                "urn:zimbraMail"
            )

            response = comm.send_request(request)

            if response.is_fault():

                self.fail(
                    "Reponse failed: (%s) %s" % (
                        response.get_fault_code(),
                        response.get_fault_message()
                    )
                )

            self.assertIsNone(
                response.get_response(3),
                "Querying an invalid requestId didn't return None"
            )
