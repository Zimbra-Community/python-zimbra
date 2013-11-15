""" Zimbra request handling (JSON) """
import json

from request import Request


class RequestJson(Request):

    request_dict = None

    """ Dictionary we're working on here """

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

    def set_context_params(self, params):

        # Call parent method

        super(RequestJson, self).set_context_params(params)

        for key, value in params.iteritems():

            self.request_dict['Header']['context'][key] = value

    def _create_batch_node(self, namespace, onerror):

        self.request_dict['Body'] = {
            'BatchRequest': {
                '_jsns': namespace,
                'onerror': onerror
            }
        }

    def add_request(self, request_name, request_dict, namespace=None):

        super(RequestJson, self).add_request(
            request_name,
            request_dict,
            namespace
        )

        request_node = self.request_dict['Body']

        if self.batch_request:

            request_id = self.batch_request_id

            request_dict['requestId'] = request_id

            self.batch_request_id += 1

            return request_id

        else:

            request_dict['_jsns'] = namespace

        request_node[request_name] = request_dict

    def get_request(self):

        return json.dumps(self.request_dict)




