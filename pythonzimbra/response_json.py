""" JSON-Response format """

import json
from pythonzimbra.response import Response


class ResponseJson(Response):

    response_dict = None

    """ The dictionary we'll be working on """

    response_type = "json"

    def clean(self):
        super(ResponseJson, self).clean()
        self.response_dict = None

    def set_response(self, response_text):

        self.response_dict = json.loads(response_text)

    def get_body(self):

        return self._filter_response(self.response_dict['Body'])

    def get_header(self):

        return self._filter_response(self.response_dict['Header'])

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

        for key, value in self.response_dict['Body']['BatchResponse'].items():

            if key == "_jsns":
                # Skip Namespace attribute

                continue

            if key == 'Fault':

                has_fault = True
                continue

            if not isinstance(value, list):

                # This is a cornerstone

                value = [value]  # pragma: no cover

            for item in value:

                request_id = item['requestId']

                ret_dict['idToName'][request_id] = key

                if key not in ret_dict['nameToId']:

                    ret_dict['nameToId'][key] = []

                ret_dict['nameToId'][key].append(request_id)

        ret_dict['hasFault'] = has_fault

        return ret_dict

    def get_response(self, request_id=0):

        if self.is_batch():

            for key in self.response_dict[
                'Body'
            ]['BatchResponse'].keys():

                if key == "_jsns":
                    continue  # pragma: no cover

                value = self.response_dict['Body']['BatchResponse'][key]

                if int(value[0]['requestId']) == request_id:

                    return self._filter_response({
                        key: value
                    })

        else:

            key = list(self.response_dict['Body'].keys())[0]

            return self._filter_response({
                key: self.response_dict['Body'][key]
            })

    def get_fault_code(self):

        if self.is_batch():

            ret_dict = {}

            for response in self.response_dict['Body'][
                    'BatchResponse']["Fault"]:

                request_id = response["requestId"]

                ret_dict[request_id] = response["Detail"]["Error"]["Code"]

            return ret_dict

        else:

            return self.get_response()["Fault"]["Detail"]["Error"]["Code"]

    def get_fault_message(self):

        if self.is_batch():

            ret_dict = {}

            for response in self.response_dict['Body'][
                    'BatchResponse']["Fault"]:

                request_id = response["requestId"]

                ret_dict[request_id] = response["Reason"]["Text"]

            return ret_dict

        else:

            return self.get_response()["Fault"]["Reason"]["Text"]


