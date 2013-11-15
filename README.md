Python-Zimbra
=============

Python classes to access Zimbra SOAP backend with a few utilities. Handles
creating and sending Zimbra SOAP queries to the backend and adds a few
utilities such as a preauth generator.

This framework is not intended to supply user level access to Zimbra
functions. Zimbra tends to be too dynamic and complex for this to work. This
is actually a framework to reduce the implementation work if you want to
speak to the Zimbra SOAP API.

Please refer to the [official SOAP documentation by Zimbra](http://wiki.zimbra.com/wiki/SOAP_API_Reference_Material_Beginning_with_ZCS_8.0)
on how to use the SOAP backend.

Tutorial
--------

If you'd like to get the current version information from your zimbra admin,
this is how you do it:

First, import the needed libraries (You will learn about them later):

    from pythonzimbra.tools import auth
    from pythonzimbra.request_xml import RequestXml
    from pythonzimbra.response_xml import ResponseXml
    from pythonzimbra.communication import Communication

Let's assume you have a variable called "url" which holds the URL to your
Zimbra server. For our example this has to be an administrative url,
so it's something like "https://<yourzimbraserver>:7071/service/admin/soap"

Now, build up the communication object:

    comm = Communication(url)

This will be used to send the request later on. But first,
we have to authenticate using Zimbra preauth. We can do this by using the
auth-helper:

    token = auth.authenticate(
        url,
        'myadminuser@mydomain.com',
        'fkiwfki2ri32fiqepnfpwenufpsecretpreauthkey'
    )

This should return the authentication token to be used in Zimbra requests. If
 it returns None, the authentication is somehow failed (maybe wrong username,
  URL or preauthentication-key)

Now, we create our request (we use the XML mode in this example),

    info_request = RequestXml()

inject the authentication token into it,

    info_request.set_auth_token(token)

and add our (very simple) GetVersionInfo request,
which is in the urn:zimbraAdmin-namespace:

    info_request.add_request('GetVersionInfoRequest', {}, 'urn:zimbraAdmin')

Now, we prepare a response object for the transport (this has to use the same
 method (xml or json) as the request object):

    info_response = ResponseXml()

And finally, we sent the request:

    comm.send_request(info_request, info_response)

Our info_response-variable now holds the response information of the object.

Now, if the response was successful and has now Fault-object:

    if not info_response.is_fault():

Print the version info:

    print info_response.get_response()['GetVersionInfoResponse']['info']['version']

The framework also supports Zimbra batch requests. Please refer to the class
docs for more information.

Used dictionary
---------------

All requests and responses are built up using a certain dictionary format.
This is heavily influenced by the Zimbra json format being:

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