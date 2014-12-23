""" A tool to convert from Zimbra dicts to Python dicts

"Zimbra dicts" means lists in the following form::

    [
        {
            "n": "key",
            "_content": "value"
        }
    ]

"""


def zimbra_to_python(zimbra_dict, key_attribute="n",
                     content_attribute="_content"):

    """
    Converts single level Zimbra dicts to a standard python dict

    :param zimbra_dict: The dictionary in Zimbra-Format
    :return: A native python dict
    """

    local_dict = {}

    for item in zimbra_dict:

        local_dict[item[key_attribute]] = item[content_attribute]

    return local_dict


def get_value(haystack, needle, key_attribute="n",
              content_attribute="_content"):

    """ Fetch a value from a zimbra-like json dict (keys are "n", values are
    "_content"

    This function may be slightly faster than zimbra_to_python(haystack)[
    needle], because it doesn't necessarily iterate over the complete list.

    :param haystack: The list in zimbra-dict format
    :param needle: the key to search for
    :return: the value or None, if the key is not found
    """

    for value in haystack:

        if value[key_attribute] == needle:

            return value[content_attribute]

    return None
