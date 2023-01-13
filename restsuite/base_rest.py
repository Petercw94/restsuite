"""
Base Class for SuiteTalk and RESTlet.
"""

import requests
import json

from .auth import NetsuiteOAuth


class Rest:
    def __init__(self, account_id, consumer_key, consumer_secret, token_key=None, token_secret=None) -> None:
        self.auth = NetsuiteOAuth(
            account_id, consumer_key, consumer_secret, token_key, token_secret)

    def get(self, url: str, headers=None):
        """
        Retrieve data from netsuite. 

        Wrapper function for all endpoints in the Netsuite API that accept the
        GET http method. 

        Args:
        -----
        - url (str) -> The url from which to get data (actual url, not base string. see Examples section for example)
        - headers (dict) -> Optional dictionary of headers to override the defaults. (See README or NetsuiteOAuth.generate_headers for defaults)

        Returns:
        --------
        - response (obj) -> requests.response object from GET request. 

        Examples:
        ---------
        URL: https://{{ NETSUITE ACCOUNT ID }}.suitetalk.api.netsuite.com/services/rest/record/v1/job/ 

        HEADERS: {"Prefer": "respond-async", "limit": 100, "offset": 2}
            NOTE: The get method would take the above headers parameter and add the Authorization 
            header to it, in order to properly sign the request. All other default headers will be dropped.

        """

        # type checking
        if headers and not isinstance(headers, dict):
            raise TypeError(
                "Expected dictionary for headers parameter. Received: {}".format(type(headers)))

        # generate default auth headers:
        default_headers = self.auth.generate_auth_header("GET", url)

        # override headers if necessary
        if headers:
            headers["Authorization"] = default_headers["Authorization"]
        else:
            headers = default_headers

        response = requests.get(url, headers=headers)

        return response

    def post(self, url: str, body: dict, headers=None):
        """
        Create a record in Netsuite.

        Wrapper function for all endpoints in the Netsuite API that accept the 
        PATCH http method.

        Args:
        -----
        - url (str) -> The url from which to get data (actual url, not base string. see Examples section for example)
        - body (dict) -> The POST body containing fields to update and their new values as key-value pairs.
        - headers (dict) -> Optional dictionary of headers to override the defaults. (See README or NetsuiteOAuth.generate_headers for defaults)

        Returns:
        --------
        - response (obj) -> requests.response object from GET request. 

        Examples:
        ---------
        URL: https://{{ NETSUITE ACCOUNT ID }}.suitetalk.api.netsuite.com/services/rest/record/v1/job/12345

        BODY: {"entityid": "Updated Customer"} <- update customer 12345's entity id to "Updated Customer"

        HEADERS: {"Prefer": "respond-async", "limit": 100, "offset": 2}
            NOTE: The get method would take the above headers parameter and add the Authorization 
            header to it, in order to properly sign the request. All other default headers will be dropped.
        """

        # type checking
        if headers and not isinstance(headers, dict):
            raise TypeError(
                "Expected dictionary for headers parameter. Received: {}".format(type(headers)))

        if not isinstance(body, dict):
            raise TypeError(
                "Expected dictionary for headers parameter. Received: {}".format(type(body)))

        # generate default auth headers:
        default_headers = self.auth.generate_auth_header("PATCH", url)

        # override headers if necessary
        if headers:
            headers["Authorization"] = default_headers["Authorization"]
        else:
            headers = default_headers

        response = requests.post(url, headers=headers,
                                 data=json.dumps(body, default=str))

        return response

    def put(self, url: str, body: dict, headers=None):
        """
        Upsert a record in Netsuite.

        Wrapper function for all endpoints in the Netsuite API that accept the 
        PUT http method.

        "The upsert operation enables you to either create a record, or update an existing record. You 
        can only use the upsert operation when you use an external ID in the request URL and when 
        you use the PUT HTTP method." - Netsuite Documentation

        Args:
        -----
        - url (str) -> The url from which to get data (actual url, not base string. see Examples section for example)
        - body (dict) -> The PUT body containing fields to update and their new values as key-value pairs.
        - headers (dict) -> Optional dictionary of headers to override the defaults. (See README or NetsuiteOAuth.generate_headers for defaults)

        Returns:
        --------
        - response (obj) -> requests.response object from PUT request. 

        Examples:
        ---------
        URL: https://{{ NETSUITE ACCOUNT ID }}.suitetalk.api.netsuite.com/services/rest/record/v1/job/eid:54321

        BODY: {"entityid": "Updated Customer"} <- update customer 12345's entity id to "Updated Customer"

        HEADERS: {"Prefer": "respond-async", "limit": 100, "offset": 2}
            NOTE: The get method would take the above headers parameter and add the Authorization 
            header to it, in order to properly sign the request. All other default headers will be dropped.
        """

        # type checking
        if headers and not isinstance(headers, dict):
            raise TypeError(
                "Expected dictionary for headers parameter. Received: {}".format(type(headers)))

        if not isinstance(body, dict):
            raise TypeError(
                "Expected dictionary for headers parameter. Received: {}".format(type(body)))

        # generate default auth headers:
        default_headers = self.auth.generate_auth_header("PATCH", url)

        # override headers if necessary
        if headers:
            headers["Authorization"] = default_headers["Authorization"]
        else:
            headers = default_headers

        response = requests.put(
            url, headers=headers, data=json.dumps(body, default=str))

        return response

    def delete(self, url: str, headers=None):
        """
        Delete a record in Netsuite.

        Wrapper function for all endpoints in Netsuite API that accept the DELETE http method. 

        Args:
        -----
        - url (str) -> The url from which to get data (actual url, not base string. see Examples section for example)
        - headers (dict) -> Optional dictionary of headers to override the defaults. (See README or NetsuiteOAuth.generate_headers for defaults)

        Returns:
        --------
        - response (obj) -> requests.response object from DELETE request. 

        Examples:
        ---------
        URL: https://{{ NETSUITE ACCOUNT ID }}.suitetalk.api.netsuite.com/services/rest/record/v1/job/ 

        HEADERS: {"Prefer": "respond-async", "limit": 100, "offset": 2}
            NOTE: The get method would take the above headers parameter and add the Authorization 
            header to it, in order to properly sign the request. All other default headers will be dropped.
        """

        # type checking
        if headers and not isinstance(headers, dict):
            raise TypeError(
                "Expected dictionary for headers parameter. Received: {}".format(type(headers)))

        # generate default auth headers:
        default_headers = self.auth.generate_auth_header("GET", url)

        # override headers if necessary
        if headers:
            headers["Authorization"] = default_headers["Authorization"]
        else:
            headers = default_headers

        response = requests.delete(url, headers=headers)

        return response
