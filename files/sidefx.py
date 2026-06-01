# Implemented by SideFX
# source: https://www.sidefx.com/docs/api/_downloads/2bed669482c8cadf176add6254a2ee7c/sidefx.py
# requires python3.9 compatibility due to rhel9 systems

from __future__ import print_function, absolute_import
import time
import json
import base64
import io
import html
from typing import Optional

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class _APIFunction(object):
    def __init__(self, function_name: str, service) -> None:
        self.function_name: str = function_name
        self.service: str = service

    def __getattr__(self, attr_name: str) -> "_APIFunction":
        # This isn't actually an API function, but a family of them.  Append
        # the requested function name to our name.
        return _APIFunction(
            f"{self.function_name}.{attr_name}", self.service)

    def __call__(self, *args, **kwargs):
        return call_api_with_access_token(
            self.service.endpoint_url, self.service.access_token,
            self.function_name, args, kwargs,
            timeout=self.service.timeout)


class _Service(object):
    def __init__(
            self,
            endpoint_url: str,
            access_token: str,
            access_token_expiry_time: str,
            timeout: str) -> None:
        self.endpoint_url: str = endpoint_url
        self.access_token: str = access_token
        self.access_token_expiry_time: str = access_token_expiry_time
        self.timeout: str = timeout

    def __getattr__(self, attr_name: str) -> _APIFunction:
        return _APIFunction(attr_name, self)


class File(object):
    """Pass parameters of this type to API functions as a way of uploading
    large files.  Note that these File parameters must be specified by keyword
    arguments when calling the functions.
    """

    def __init__(self, filename: str) -> None:
        self.filename: str = filename


class ResponseFile(object):
    """This object is returned from API functions that stream binary content.
    Call the API function from a `with` statement, and call the read method
    on the object to read the data in chunks.
    """
    def __init__(self, response):
        self.response = response

    def __enter__(self):
        return self.response.raw

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.response.close()


def service(
        client_id: str, client_secret_key: str,
        access_token_url: str = "https://www.sidefx.com/oauth2/application_token",
        endpoint_url: str ="https://www.sidefx.com/api/",
        access_token: Optional[str] = None,
        access_token_expiry_time: Optional[float] = None,
        timeout: Optional[str] = None) -> _Service:

    if (access_token is None or
            access_token_expiry_time is None or
            access_token_expiry_time < time.time()):
        access_token, access_token_expiry_time = (
            get_access_token_and_expiry_time(
                access_token_url, client_id, client_secret_key,
                timeout=timeout))

    return _Service(
        endpoint_url, access_token, access_token_expiry_time, timeout=timeout)


#------------------------------------------------------------------------------
# Code that implements authentication and raw calls into the API:

def get_access_token_and_expiry_time(
        access_token_url, client_id, client_secret_key, timeout=None):
    """Given an API client (id and secret key) that is allowed to make API
    calls, return an access token that can be used to make calls.
    """
    # If they're trying to use the /token URL directly then assume this is a
    # client-credentials application.
    post_data = {}
    if (access_token_url.endswith("/token") or
            access_token_url.endswith("/token/")):
        post_data["grant_type"] = "client_credentials"

    response = requests.post(
        access_token_url,
        headers={
            "Authorization": u"Basic {0}".format(
                base64.b64encode(
                    "{0}:{1}".format(
                        client_id, client_secret_key
                    ).encode()
                ).decode('utf-8')
            ),
        },
        data=post_data,
        timeout=timeout)
    if response.status_code != 200:
        raise AuthorizationError(
            response.status_code,
            "{0}: {1}".format(
                response.status_code,
                _extract_traceback_from_response(response)))

    response_json = response.json()
    access_token_expiry_time = time.time() - 2 + response_json["expires_in"]
    return response_json["access_token"], access_token_expiry_time


class AuthorizationError(Exception):
    """Raised from the client if the server generated an error while generating
    an access token.
    """
    def __init__(self, http_code, message):
        super(AuthorizationError, self).__init__(message)
        self.http_code = http_code


def call_api_with_access_token(
        endpoint_url, access_token, function_name, args, kwargs,
        timeout=None):
    """Call into the API using an access token that was returned by
    get_access_token.
    """
    file_data = {}
    for arg_name, arg_value in kwargs.items():
        if isinstance(arg_value, (bytearray, File)):
            if isinstance(arg_value, File):
                file_data[arg_name] = (
                    arg_value.filename, open(arg_value.filename, "rb"),
                    "application/octet-stream")
            else:
                file_data[arg_name] = (
                    "unnamed.bin", io.BytesIO(arg_value),
                    "application/octet-stream")
    for arg_name in file_data:
        del kwargs[arg_name]

    post_data = dict(json=json.dumps([function_name, args, kwargs]))

    # urllib3 renamed the method_whitelist argument to allowed_methods, so
    # handle different versions of urllib3.
    retry_kwargs = dict(
        total=3,
        status_forcelist=[429],
        allowed_methods=["GET", "POST"],
        backoff_factor=1,
    )
    try:
        retry_strategy = Retry(**retry_kwargs)
    except TypeError:
        retry_kwargs["method_whitelist"] = retry_kwargs["allowed_methods"]
        del retry_kwargs["allowed_methods"]
        retry_strategy = Retry(**retry_kwargs)

    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    response = http.post(
        endpoint_url,
        headers={"Authorization": "Bearer " + access_token},
        data=post_data,
        timeout=timeout,
        files=file_data,
        stream=True)
    if response.status_code == 200:
        if response.headers.get("Content-Type") == "application/octet-stream":
            return ResponseFile(response)
        return response.json()

    raise APIError(
        response.status_code,
        _extract_traceback_from_response(response))


class APIError(Exception):
    """Raised from the client if the server generated an error while calling
    into the API.
    """
    def __init__(self, http_code, message):
        super(APIError, self).__init__(message)
        self.http_code = http_code

    def __str__(self):
        return "%s %s" % (self.http_code, self.args[0])


def _extract_traceback_from_response(response):
    """Helper function to extract a traceback from the web server response
    if an API call generated a server-side exception and the server is running
    in debug mode.  In production mode, the server will send back just the
    stack trace without the need to parse any html.
    """
    error_message = response.text
    if response.status_code != 500:
        return error_message

    traceback = ""
    for line in error_message.split("\n"):
        if traceback and line == "</textarea>":
            break
        if line == "Traceback:" or traceback:
            traceback += line + "\n"

    if traceback:
        traceback = error_message

    return html.unescape(traceback)
