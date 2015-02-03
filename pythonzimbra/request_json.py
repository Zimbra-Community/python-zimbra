""" Zimbra request handling (JSON) """
import json

from .request import Request


class RequestJson(Request):

    request_dict = None

    """ Dictionary we're working on here """

    request_type = "json"

    def __init__(self):

        """ Generate dictionary for json output
        """

        self.request_dict = {
            'Header': {
                'context': {
                    '_jsns': 'urn:zimbra',
                    'format': {
                        'type': 'js'
                    }
                }
            },
            'Body': {}
        }

    def clean(self):
        super(RequestJson, self).clean()

        self.__init__()

    def set_context_params(self, params):

        # Call parent method

        super(RequestJson, self).set_context_params(params)

        for key, value in params.items():

            self.request_dict['Header']['context'][key] = value

    def _create_batch_node(self, onerror):

        self.request_dict['Body'] = {
            'BatchRequest': {
                '_jsns': "urn:zimbra",
                'onerror': onerror
            }
        }

    def add_request(self, request_name, request_dict, namespace):

        super(RequestJson, self).add_request(
            request_name,
            request_dict,
            namespace
        )

        request_node = self.request_dict['Body']
        request_dict['_jsns'] = namespace

        if self.batch_request:

            request_id = self.batch_request_id

            request_dict['requestId'] = request_id

            self.batch_request_id += 1

            if request_name in request_node["BatchRequest"]:

                tmp = request_node["BatchRequest"][request_name]

                request_node["BatchRequest"][request_name] = [
                    tmp,
                    request_dict
                ]

            else:

                request_node["BatchRequest"][request_name] = request_dict

            return request_id

        request_node[request_name] = request_dict

    def get_request(self):

        return json.dumps(self.request_dict)




