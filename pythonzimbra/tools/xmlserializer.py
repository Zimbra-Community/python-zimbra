""" Tools to easily serialize XML from other input forms """
import sys


def convert_to_str(input_string):

    """ Returns a string of the input compatible between py2 and py3
    :param input_string:
    :return:
    """

    if sys.version < '3':

        if isinstance(input_string, str) \
                or isinstance(input_string, unicode):  # pragma: no cover py3

            return input_string  # pragma: no cover py3

    else:

        if isinstance(input_string, str):  # pragma: no cover py3

            return input_string  # pragma: no cover py3

    return str(input_string)


def dict_to_dom(root_node, xml_dict):
    """ Create a DOM node and optionally several subnodes from a dictionary.

    :param root_node: DOM-Node set the dictionary is applied upon
    :type root_node: xml.dom.Element
    :param xml_dict: The dictionary containing the nodes to process
    :type xml_dict: dict
    """

    if '_content' in list(xml_dict.keys()):

        root_node.appendChild(
            root_node.ownerDocument.createTextNode(
                convert_to_str(xml_dict['_content'])
            )
        )

    for key, value in xml_dict.items():

        if key == '_content':
            continue

        if type(value) == dict:

            # Root node

            tmp_node = root_node.ownerDocument.createElement(key)

            dict_to_dom(tmp_node, value)

            root_node.appendChild(tmp_node)

        elif type(value) == list:

            for multinode in value:

                tmp_node = root_node.ownerDocument.createElement(key)

                dict_to_dom(tmp_node, multinode)

                root_node.appendChild(tmp_node)

        else:

            # Attributes

            root_node.setAttribute(
                key,
                convert_to_str(value)
            )


def dom_to_dict(root_node):

    """ Serializes the given node to the dictionary

    Serializes the given node to the documented dictionary format.

    :param root_node: Node to serialize
    :returns: The dictionary
    :rtype: dict
    """

    # Remove namespaces from tagname

    tag = root_node.tagName

    if ":" in tag:

        tag = tag.split(":")[1]

    root_dict = {
        tag: {}
    }

    node_dict = root_dict[tag]

    # Set attributes

    if root_node.hasAttributes():

        for key in list(root_node.attributes.keys()):

            node_dict[key] = root_node.getAttribute(key)

    # Check out child nodes

    for child in root_node.childNodes:

        if child.nodeType == root_node.TEXT_NODE:

            # This is the content

            node_dict['_content'] = child.data

        else:

            subnode_dict = dom_to_dict(child)

            child_tag = child.tagName

            if ":" in child_tag:

                child_tag = child_tag.split(":")[1]

            new_val = subnode_dict[child_tag]

            # If we have several child with same name, put them in a list.

            if child_tag in node_dict:
                prev_val = node_dict[child_tag]

                if type(prev_val) != list:
                    node_dict[child_tag] = [prev_val]

                node_dict[child_tag].append(new_val)

            else:
                node_dict[child_tag] = new_val

    return root_dict



