import logging
import urllib3
try:
    from urllib import parse
except ImportError:  # above is available in py3+, below is py2.7
    import urlparse as parse
from selenium.webdriver.remote.errorhandler import ErrorCode
from selenium.webdriver.remote import utils
import selenium.webdriver.remote.remote_connection as remote_connection

LOGGER = logging.getLogger(__name__)

def _request(self, method, url, body=None):
    """
    Send an HTTP request to the remote server.

    :Args:
     - method - A string for the HTTP method to send the request with.
     - url - A string for the URL to send the request to.
     - body - A string for request body. Ignored unless method is POST or PUT.

    :Returns:
      A dictionary with the server's parsed JSON response.
    """
    LOGGER.debug('%s %s %s' % (method, url, body))

    parsed_url = parse.urlparse(url)
    headers = self.get_remote_connection_headers(parsed_url, self.keep_alive)
    resp = None
    if body and method != 'POST' and method != 'PUT':
        body = None

    if self.keep_alive:
        resp = self._conn.request(method, url, body=body, headers=headers)

        statuscode = resp.status
    else:
        #http = urllib3.PoolManager(timeout=self._timeout)
        #HERE THE PATCH!!
        with urllib3.PoolManager(timeout=self._timeout) as http:
            resp = http.request(method, url, body=body, headers=headers)

        statuscode = resp.status
        if not hasattr(resp, 'getheader'):
            if hasattr(resp.headers, 'getheader'):
                resp.getheader = lambda x: resp.headers.getheader(x)
            elif hasattr(resp.headers, 'get'):
                resp.getheader = lambda x: resp.headers.get(x)

    data = resp.data.decode('UTF-8')
    try:
        if 300 <= statuscode < 304:
            return self._request('GET', resp.getheader('location'))
        if 399 < statuscode <= 500:
            return {'status': statuscode, 'value': data}
        content_type = []
        if resp.getheader('Content-Type') is not None:
            content_type = resp.getheader('Content-Type').split(';')
        if not any([x.startswith('image/png') for x in content_type]):

            try:
                data = utils.load_json(data.strip())
            except ValueError:
                if 199 < statuscode < 300:
                    status = ErrorCode.SUCCESS
                else:
                    status = ErrorCode.UNKNOWN_ERROR
                return {'status': status, 'value': data.strip()}

            # Some of the drivers incorrectly return a response
            # with no 'value' field when they should return null.
            if 'value' not in data:
                data['value'] = None
            return data
        else:
            data = {'status': 0, 'value': data}
            return data
    finally:
        LOGGER.debug("Finished Request")
        resp.close()



def remote_connection_warnings_patch():
    '''
    Due to bad request handling we get lots of warnings
    Although this is fixed in webdriver's code, it is still not released
    https://github.com/SeleniumHQ/selenium/issues/6878
    https://github.com/jimevans/selenium/commit/88ecc549edc5731b8cbc3210a5e4e242e1e5807c
    DELETEME WHEN FIXED IN WEBDRIVER/SELENIUM
    '''
    remote_connection.RemoteConnection._request = _request
