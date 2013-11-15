""" XML-Response format. """

from xml.dom import minidom
from pythonzimbra.tools.xmlserializer import dom_to_dict
from response import Response


class ResponseXml(Response):

    response_doc = None

    """ The response document we're working on """

    def set_response(self, response_text):

        self.response_doc = minidom.parseString(response_text)

    def get_body(self):

        return dom_to_dict(self.response_doc.getElementsByTagNameNS(
            "*", "Body"
        ).item(0))

    def get_header(self):

        return dom_to_dict(self.response_doc.getElementsByTagNameNS(
            "*", "Header"
        ).item(0))

    def is_batch(self):

        if self.response_doc.getElementsByTagName("BatchResponse").length > 0:

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

        search_node = self.response_doc.getElementsByTagNameNS(
            "*", "BatchResponse"
        ).item(0)

        for child in search_node.childNodes:

            request_id = child.getAttribute("requestId")

            ret_dict['idToName'][request_id] = child.tagName

            if child.tagName not in ret_dict['nameToId'].keys():

                ret_dict['nameToId'][child.tagName] = []

            ret_dict['nameToId'][child.tagName].append(request_id)

            if child.tagName == 'Fault':

                has_fault = True

        ret_dict['hasFault'] = has_fault

        return ret_dict

    def get_response(self, request_id=0):

        if self.is_batch():

            search_node = self.response_doc.getElementsByTagNameNS(
                "*", "BatchResponse"
            ).item(0)

            for child in search_node.childNodes:

                if child.getAttribute("requestId") == request_id:

                    return self._filter_response(dom_to_dict(child))

            return None

        else:

            search_node = self.response_doc.getElementsByTagNameNS(
                "*", "Body"
            ).item(0)

            return self._filter_response(dom_to_dict(search_node.firstChild))