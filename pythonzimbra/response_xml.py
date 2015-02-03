""" XML-Response format. """

from xml.dom import minidom
from pythonzimbra.tools.xmlserializer import dom_to_dict
from .response import Response


class ResponseXml(Response):

    response_doc = None

    """ The response document we're working on """

    response_type = "xml"

    def clean(self):
        super(ResponseXml, self).clean()
        self.response_doc = None

    def set_response(self, response_text):

        if not isinstance(response_text, str):

            response_text = response_text.encode("utf-8")

        self.response_doc = minidom.parseString(response_text)

    def get_body(self):

        return self._filter_response(
            dom_to_dict(
                self.response_doc.getElementsByTagNameNS(
                    "*", "Body"
                ).item(0).firstChild
            )
        )

    def get_header(self):

        return self._filter_response(
            dom_to_dict(
                self.response_doc.getElementsByTagNameNS(
                    "*", "Header"
                ).item(0).firstChild
            )
        )

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

            tag = child.tagName

            if ":" in tag:

                tag = tag.split(":")[1]

            if tag == 'Fault':

                has_fault = True
                continue

            request_id = child.getAttribute("requestId")

            ret_dict['idToName'][request_id] = tag

            if tag not in list(ret_dict['nameToId'].keys()):

                ret_dict['nameToId'][tag] = []

            ret_dict['nameToId'][tag].append(request_id)

        ret_dict['hasFault'] = has_fault

        return ret_dict

    def get_response(self, request_id=0):

        if self.is_batch():

            search_node = self.response_doc.getElementsByTagNameNS(
                "*", "BatchResponse"
            ).item(0)

            for child in search_node.childNodes:

                if int(child.getAttribute("requestId")) == request_id:

                    return self._filter_response(dom_to_dict(child))

            return None

        else:

            search_node = self.response_doc.getElementsByTagNameNS(
                "*", "Body"
            ).item(0)

            return self._filter_response(dom_to_dict(search_node.firstChild))

    def get_fault_code(self):

        if self.is_batch():

            ret_dict = {}

            search_node = self.response_doc.getElementsByTagNameNS(
                "*", "BatchResponse"
            ).item(0)

            for child in search_node.childNodes:

                ret_dict[child.getAttribute("requestId")] = self.get_response(
                    int(child.getAttribute("requestId"))
                )["Fault"]["Detail"]["Error"]["Code"]

            return ret_dict

        else:

            return self.get_response()["Fault"]["Detail"]["Error"][
                "Code"]

    def get_fault_message(self):

        if self.is_batch():

            ret_dict = {}

            search_node = self.response_doc.getElementsByTagNameNS(
                "*", "BatchResponse"
            ).item(0)

            for child in search_node.childNodes:

                ret_dict[child.getAttribute("requestId")] = self.get_response(
                    int(child.getAttribute("requestId"))
                )["Fault"]["Reason"]["Text"]

            return ret_dict

        else:

            return self.get_response()["Fault"]["Reason"]["Text"]
