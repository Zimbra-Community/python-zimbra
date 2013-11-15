Python-Zimbra
=============

Python classes to access Zimbra SOAP backend with a few utilities. Handles
creating and sending Zimbra SOAP queries to the backend and adds a few
utilities such as a preauth generator.

Please refer to the [official SOAP documentation by Zimbra](http://wiki.zimbra.com/wiki/SOAP_API_Reference_Material_Beginning_with_ZCS_8.0)
on how to use the SOAP backend.

Used dictionary
---------------

All requests are built up using a certain dictionary format. This is heavily
influenced by the Zimbra json format being:

    {
        "RequestName": {
            "_content": "Content of the node"
            "attribute": "value",
            "subnode": {
                "_content": "Content of the subnode"
            }
        }
    }

in XML this would look like this:

    <RequestName attribute="value">
        <subnode>
            Content of the subnode
        </subnode>

        Content of the node
    </RequestName>

All requests should conform to this dictionary format and the responses are
also returned in this format.

Warning
-------

There are missing sanity checks on purpose. This is because the Zimbra API is
 due to heavy modifications and to keep up with the current API catalogue is
 quiet problematic.

So please be aware of this and use the library with caution. Don't expose the
 library to the public without doing sanity checks on your own.