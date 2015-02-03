""" Tests of XML Serializer tools """

from unittest import TestCase
from pythonzimbra.tools import xmlserializer
from xml.dom import minidom
from pythonzimbra.tools.xmlserializer import dom_to_dict


class TestXmlSerializer(TestCase):

    def test_dict_to_dom(self):

        """ Test xml serialization using dict_to_dom method.
        """

        test_doc = minidom.Document()
        test_node = test_doc.createElement("test")
        test_dict = {
            'attr1': 'value1',
            'attr2': 'value2',
            'subnode1': {
                '_content': 'testcontent'
            },
            'subnode2': {
                'subnode2attr1': 'value1',
                'subnode2attr2': 'value2',
                '_content': 'testcontent2'
            },
            'subnode3': {
                'subnode3attr1': 'value1',
                'subnode3attr2': 'value2',
                'subnode31': {
                    '_content': 'testcontent3'
                }
            },
            'listsubnode': [
                {
                    "_content": "value1"
                },
                {
                    "_content": "value2"
                },
                {
                    "_content": "value3"
                }
            ]
        }

        xmlserializer.dict_to_dom(test_node, test_dict)

        self.assertEqual(
            xmlserializer.dom_to_dict(test_node),
            {
                "test": test_dict
            }
        )

    def test_dict_to_dom_unicode(self):

        """ Test xml serialization using dict_to_dom method.
        """

        test_doc = minidom.Document()
        test_node = test_doc.createElement("test")
        test_dict = {
            'attr1': 'value1',
            'attr2': 'value2',
            'subnode1': {
                '_content': 'testcontent'
            },
            'subnode2': {
                'subnode2attr1': 'value1',
                'subnode2attr2': 'value2',
                '_content': 'testcontent2'
            },
            'subnode3': {
                'subnode3attr1': 'value1',
                'subnode3attr2': 'value2\xf6',
                'subnode31': {
                    '_content': 'testcontent3\xf6'
                }
            },
            'listsubnode': [
                {
                    "_content": "value1"
                },
                {
                    "_content": "value2"
                },
                {
                    "_content": "value3"
                }
            ]
        }

        xmlserializer.dict_to_dom(test_node, test_dict)

        self.assertEqual(
            xmlserializer.dom_to_dict(test_node),
            {
                "test": test_dict
            }
        )

    def test_dom_to_dict(self):

        """ Test xml->dict serialization

        Creates a node, generates the dict using dict_to_dom and compares a
        pickled result
        """

        test_doc = minidom.Document()

        test_node = test_doc.createElement("test")

        test_node.setAttribute("testattribute", "value")

        test_subnode = test_doc.createElement("subtest")

        test_subnode.appendChild(test_doc.createTextNode("testcontent"))

        test_node.appendChild(test_subnode)

        test_doc.appendChild(test_node)

        test_dict = dom_to_dict(test_node)

        expected_result = {
            "test": {
                "testattribute": "value",
                "subtest": {
                    "_content": "testcontent"
                }
            }
        }

        self.assertEqual(
            expected_result,
            test_dict
        )
