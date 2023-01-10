"""
Module for handling all REST related requests in the Netsuite API.
"""


import json
import requests

from .base_rest import Rest


class NetSuiteRest(Rest):
    """
    """

    def __init__(self, account_id, consumer_key, consumer_secret, token_key=None, token_secret=None) -> None:
        super().__init__(account_id, consumer_key, consumer_secret, token_key, token_secret)

    def patch(self, url: str, body: dict, headers=None):
        """
        Update a record in Netsuite.

        Wrapper function for all endpoints in the Netsuite API that accept the 
        PATCH http method.

        NOTE: To delete a value from a record, simply pass null as the value.

        Args:
        -----
        - url (str) -> The url from which to get data (actual url, not base string. see Examples section for example)
        - body (dict) -> The PATCH body containing fields to update and their new values as key-value pairs.
        - headers (dict) -> Optional dictionary of headers to override the defaults. (See README or NetsuiteOAuth.generate_headers for defaults)

        Returns:
        --------
        - response (obj) -> requests.response object from PATCH request. 

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

        response = requests.patch(
            url, headers=headers, data=json.dumps(body, default=str))

        return response
