sentry-opsgenie
================

A plugin for sentry that enables sending events on to a OpsGenie instance.

Install
-------

Install the package with ``pip``::

    pip install git+git://github.com/whommel/sentry-opsgenie.git


Configuration
-------------

Go to your project's configuration page (Projects -> [Project]) and click on "Manage Plugins".
Switch on OpsGenie by ticking "Enabled" in the appropriate column. Click "Save Changes". 
Then select the "OpsGenie" tab and enter the OpsGenie api-key, your sentry service-key and the domain name of your OpsGenie instance.


Time out issues
---------------

You might experience issues with raven client's default timeout beeing to short for OpsGenie to respond in time. In that case you need to adjust the timeout accordingly.
This proves challenging since providing a timeout query with the DSN is currently beeing disabled (https://github.com/getsentry/raven-python/issues/253) as is passing a timeout value 
during client instance creation (https://github.com/getsentry/raven-python/issues/183).

A temporarily solution which does not include changing 3rd party code would be to manually configure the client with a custom transport class e.g.::

    from urlparse import urlparse
    from raven import Client
    from raven.transport.base import HTTPTransport

    # instantiate client as usual
    client = Client('http://<public_key>:<secret_key>@0.0.0.0:9000/2')

    # create transport with custom timeout and register it with your sentry instance 
    transport = HTTPTransport(urlparse("http://0.0.0.0:9000/api/store/"), timeout=30)
    client._registry._transports["http://0.0.0.0:9000/api/store/"] = transport

    # use client at your convenience
    client.captureMessage('hello world')
