# Python-Zimbra

Python classes to access Zimbra SOAP backend with a few utilities. Handles
creating and sending Zimbra SOAP queries to the backend and adds a few
utilities such as a preauth generator.

Compatible with Python 2.7 and 3.x (cPython and PyPy)

This framework is not intended to supply user level access to Zimbra
functions. Zimbra tends to be too dynamic and complex for this to work. This
is actually a framework to reduce the implementation work if you want to
speak to the Zimbra SOAP API.

Please refer to the [official SOAP documentation by Zimbra](http://wiki.zimbra.com/wiki/SOAP_API_Reference_Material_Beginning_with_ZCS_8.0)
on how to use the SOAP backend.

For details refer to the [API-Documentation](http://zimbra-community.github.io/python-zimbra/docs/).

## Warning

There are missing sanity checks on purpose. This is because the Zimbra API is
 due to heavy modifications and to keep up with the current API catalogue is
 quiet problematic.

So please be aware of this and use the library with caution. Don't expose the
 library to the public without doing sanity checks on your own.

## Tutorial

This tutorial will explain you how to get information about a folder of a specific user.
this is how you do it in a few steps:
* [Installation](#installation)
* [Imports](#imports)
* [Communication and Token](#setup)
* [Creating your request](#request)
* [Fault handling](#fault)
* [Batch](#bacth)

### Installation

To install, either use :

`pip install python-zimbra`

or

`easy_install python-zimbra`

You may add `--pre` to download the pre-release

### Imports
First, import the needed libraries (You will learn about them later):
```python
import pythonzimbra.communication
from pythonzimbra.communication import Communication
import pythonzimbra.tools
from pythonzimbra.tools import auth
```
### Setup
Now, build up the communication object to send the future requests:
```python
# url to your zimbra server
url  = 'https://your-zimbra-server/service/soap'
comm = Communication(url)
```
Then, we will have to authenticate. Using [Zimbra preauth](https://wiki.zimbra.com/wiki/Preauth), we can do the following:
```python
usr_token = auth.authenticate(
    url,
    'myuser@mydomain.com',
    'secret-preauth-key'
)
```
This will return `None` on failure. If it is so, please check the parameters again.
Otherwise, you will get your authentication token for your Zimbra requests.

### Request
Time to create our request. This is how to get the content of a folder (located in `urn:zimbraMail-namespace`). 

Here is how initiating the request, adding a request then send it and gather its response.
```python
info_request = comm.gen_request(token=usr_token)
info_request.add_request(
    'GetFolderRequest',
    {
        'folder': {
            'path': '/inbox'
        }
    },
    'urn:zimbraMail'
)
info_response = comm.send_request(info_request)
```

Now, if the response was successful, we can print the result:
```python
if not info_response.is_fault():
    print (info_response.get_response()['GetFolderResponse']['folder']['n'])
```

### Fault
To verify if there is any fault in your response:
```python
response.is_fault()
```

If a result is fault, you can get specific information about it.
```python
response.get_fault_code()
response.get_fault_message()
```

* The fault_code is Zimbra's own fault message code (like mail.NO_SUCH_FOLDER).
* The message is a more elaborate message like (no such folder path: /...).
 
### Batch

Working with batch requests is also possible. To do that, set the
parameter "set_batch":
```python
batch_request = comm.gen_request(set_batch=True)
```
And can afterwards add multiple requests using add_request to it. You'll get 
the request id of the specific request as a return value. Use that id to 
retrieve the response later using get_response(id).


## Authentication against the administration console

Zimbra currently doesn't support the preauth-method for authentications against
the admin-console (URL `https://your-zimbra-server:7071/service/admin/soap`).

python-zimbra's auth tool can be used to authenticate to this url by specifying
the password instead of the preauth-key and setting the parameter admin_auth to
True. (see API docs for specifics)

## Used dictionary

All requests and responses are built up using a certain dictionary format.
This is heavily influenced by the Zimbra json format being:
```json
{
    "RequestName": {
        "_content": "Content of the node",
        "attribute": "value",
        "subnode": {
            "_content": "Content of the subnode"
        }
    }
}
```
in XML this would look like this:
```xml
<RequestName attribute="value">
    <subnode>
        Content of the subnode
    </subnode>
    Content of the node
</RequestName>
```
All requests should conform to this dictionary format and the responses are
also returned in this format. Subnodes can also contain lists of
dictionaries, which will create multiple subnodes with the same tag.

## Use a Custom SSL Context

In test environments sometimes SSL is not available and we want to disable SSL verification.

To achieve this we can use a [custom SSL context](https://docs.python.org/3/library/ssl.html#ssl-contexts):

Not yet released on pypi, so put in your `requirements.txt`:

    -e git+https://github.com/Zimbra-Community/python-zimbra.git#egg=python-zimbra

Example:

```python
import ssl

context = ssl.SSLContext()

...
comm = Communication(url, context=context)

usr_token = auth.authenticate(
    url=url,
    ...,
    context=context
)
```

## Testing

Python-Zimbra includes a testsuite with unittests, that test the supported
features.

To enable testing in your environment, copy the config.ini.dist to config.ini
in the tests module and configure it to match your environment.

You may need a Zimbra server with an admin and a user account to run all tests.
You have to specifically enable these tests. 

Test overview:
* `test_admin.py`
  * Authenticate as admin
  * Add a test account
  * Try logging in using that test account
  * Delete the test account
* `test_auth.py`
  * Authenticate as user
  * Authenticate as user with wrong preauth key
  * Authenticate as user with password
  * Authenticate as user with wrong password
* `test_autoresponse.py`
  * Authenticate as user
  * Send `NoOpRequest`
* `test_fault.py`
  * Authenticate as user
  * Query a non-existing folder using `GetFolderRequest`
  * Query a non-existing folder using `GetFolderRequest` inside a `BatchRequest`
* `test_genrequest.py`
  * Authenticate as user
  * Send a `NoOpRequest`
  * Send a `NoOpRequest` inside a `BatchRequest`
  * Send a GetInfoRequest
  * Send a `NoOpRequest` and a `GetInfoRequest` inside a `BatchRequest`

To run the test, enter the tests subdirectory and run
```bash
python -m unittest discover -s ..
```
We thankfully use [Travis](travis-ci.org) for continuous integration and
[Coveralls](https://coveralls.io) for code coverage.

The Zimbra server used in CI-testing is kindly hosted by [efm](http://www.efm.de/).

[ibs27]: https://img.shields.io/teamcity/http/ci.blueocean-net.de/s/ZimbraCommunity_PythonZimbra_TestPy27.png
[bs27]: http://ci.blueocean-net.de/viewType.html?buildTypeId=ZimbraCommunity_PythonZimbra_TestPy27
[icv27]: http://ci.blueocean-net.de/repository/download/ZimbraCommunity_PythonZimbra_TestPy27/.lastFinished/tests/coverage.png/coverage.png
[cv27]: http://ci.blueocean-net.de/repository/download/ZimbraCommunity_PythonZimbra_TestPy27/.lastFinished/tests/htmlcov/index.html 

[ibs32]: https://img.shields.io/teamcity/http/ci.blueocean-net.de/s/ZimbraCommunity_PythonZimbra_TestPy32.png
[bs32]: http://ci.blueocean-net.de/viewType.html?buildTypeId=ZimbraCommunity_PythonZimbra_TestPy32
[icv32]: http://ci.blueocean-net.de/repository/download/ZimbraCommunity_PythonZimbra_TestPy32/.lastFinished/tests/coverage.png/coverage.png
[cv32]: http://ci.blueocean-net.de/repository/download/ZimbraCommunity_PythonZimbra_TestPy32/.lastFinished/tests/htmlcov/index.html

[ibs336]: https://img.shields.io/teamcity/http/ci.blueocean-net.de/s/ZimbraCommunity_PythonZimbra_TestPy336.png
[bs336]: http://ci.blueocean-net.de/viewType.html?buildTypeId=ZimbraCommunity_PythonZimbra_TestPy336
[icv336]: http://ci.blueocean-net.de/repository/download/ZimbraCommunity_PythonZimbra_TestPy336/.lastFinished/tests/coverage.png/coverage.png
[cv336]: http://ci.blueocean-net.de/repository/download/ZimbraCommunity_PythonZimbra_TestPy336/.lastFinished/tests/htmlcov/index.html
 
[ibs343]: https://img.shields.io/teamcity/http/ci.blueocean-net.de/s/ZimbraCommunity_PythonZimbra_TestPy343.png
[bs343]: http://ci.blueocean-net.de/viewType.html?buildTypeId=ZimbraCommunity_PythonZimbra_TestPy343
[icv343]: http://ci.blueocean-net.de/repository/download/ZimbraCommunity_PythonZimbra_TestPy343/.lastFinished/tests/coverage.png/coverage.png
[cv343]: http://ci.blueocean-net.de/repository/download/ZimbraCommunity_PythonZimbra_TestPy343/.lastFinished/tests/htmlcov/index.html
 
[ibspy261]: https://img.shields.io/teamcity/http/ci.blueocean-net.de/s/ZimbraCommunity_PythonZimbra_TestPypy261.png
[bspy261]: http://ci.blueocean-net.de/viewType.html?buildTypeId=ZimbraCommunity_PythonZimbra_TestPypy261
[icvpy261]: http://ci.blueocean-net.de/repository/download/ZimbraCommunity_PythonZimbra_TestPypy261/.lastFinished/tests/coverage.png/coverage.png
[cvpy261]: http://ci.blueocean-net.de/repository/download/ZimbraCommunity_PythonZimbra_TestPypy261/.lastFinished/tests/htmlcov/index.html 

[ibspy3240]: https://img.shields.io/teamcity/http/ci.blueocean-net.de/s/ZimbraCommunity_PythonZimbra_TestPypy3240.png
[bspy3240]: http://ci.blueocean-net.de/viewType.html?buildTypeId=ZimbraCommunity_PythonZimbra_TestPypy3240
[icvpy3240]: http://ci.blueocean-net.de/repository/download/ZimbraCommunity_PythonZimbra_TestPypy3240/.lastFinished/tests/coverage.png/coverage.png
[cvpy3240]: http://ci.blueocean-net.de/repository/download/ZimbraCommunity_PythonZimbra_TestPypy3240/.lastFinished/tests/htmlcov/index.html
