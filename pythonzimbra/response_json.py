""" JSON-Response format """

import json
from pythonzimbra.response import Response


class ResponseJson(Response):

    response_dict = None

    """ The dictionary we'll be working on """

    def set_response(self, response_text):

        self.response_dict = json.loads(response_text)

    def get_body(self):

        return self.response_dict['Body']

    def get_header(self):

        return self.response_dict['Header']

    def is_batch(self):

        if 'BatchResponse' in self.response_dict['Body']:

            return True

        return False

    def get_batch(self):

        if not self.is_batch():

            return None

        ret_dict = {

            'idToName': {},
            'nameToId': {}
        }

        has_fault = False

        for key, value in self.response_dict['Body']['BatchResponse']\
            .iteritems():

            request_id = value['requestId']

            ret_dict['idToName'][request_id] = key

            if key not in ret_dict['nameToId']:

                ret_dict['nameToId'][key] = []

            ret_dict['nameToId'][key].append(request_id)

            if key == 'Fault':

                has_fault = True

        ret_dict['hasFault'] = has_fault

        return ret_dict

    def get_response(self, request_id=0):

        if self.is_batch():

            for key, value in self.response_dict[
                'Body'
            ]['BatchResponse'].iteritems():

                if value['requestId'] == request_id:

                    return self._filter_response({
                        key: value
                    })

        else:

            key = self.response_dict['Body'].keys()[0]

            return self._filter_response({
                key: self.response_dict['Body'][key]
            })