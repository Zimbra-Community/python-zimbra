""" Tools to easily serialize XML from other input forms """


def dict_to_dom(root_node, xml_dict):
    """ Create a DOM node and optionally several subnodes from a dictionary.

    :param root_node: DOM-Node set the dictionary is applied upon
    :type root_node: xml.dom.Node
    :param xml_dict: The dictionary containding the nodes to process. This
    dictionary is expected in this format:
      {
        '_content' : <The raw content of the tag>
        'subtag': {...} <A subtag with other nodes. Is also a dictionary in the
                   same format>
        'attrib': 'value' <An attribute with its value
      }
    :type xml_dict: dict
    """

    if '_content' in xml_dict.keys():

        root_node.appendChild(
            root_node.ownerDocument.createTextNode(str(xml_dict['_content']))
        )

    for key, value in xml_dict.iteritems():

        if key == '_content':
            continue

        if type(value) == dict:

            # Root node

            tmp_node = root_node.ownerDocument.createElement(key)

            dict_to_dom(tmp_node, value)

            root_node.appendChild(tmp_node)

        else:

            # Attributes

            root_node.setAttribute(
                key,
                str(value)
            )


def dom_to_dict(root_node):

    """ Serializes the given node to the dictionary

    Serializes the given node to the documented dictionary format.

    :param root_node: Node to serialize
    :returns: The dictionary
    :rtype: dict
    """

    root_dict = {
        root_node.tagName: {}
    }

    node_dict = root_dict[root_node.tagName]

    # Set attributes

    if root_node.hasAttributes():

        for key in root_node.attributes.keys():

            node_dict[key] = root_node.getAttribute(key)

    # Check out child nodes

    for child in root_node.childNodes:

        if child.nodeType == root_node.TEXT_NODE:

            # This is the content

            node_dict['_content'] = child.data

        else:

            subnode_dict = dom_to_dict(child)

            node_dict[child.tagName] = subnode_dict[child.tagName]

    return root_dict



