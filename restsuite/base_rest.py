"""
Base Class for SuiteTalk and RESTlet.
"""

import requests
import json

from requests_oauthlib import OAuth1


class Rest:
    def __init__(self, account_id, consumer_key, consumer_secret, token_key=None, token_secret=None) -> None:
        self.auth = OAuth1(
            realm=account_id,
            client_key=consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=token_key,
            resource_owner_secret=token_secret,
            signature_method="HMAC-SHA256"
        )

    def request(self, method: str, url: str, **kwargs):
        """
        NEW for version 1.

        Main request method inherited by each NetSuite interface. 
        Key-word arguments can be passed dependent upon the http 
        method desired. This allows for a single method to be called
        for every method desired. 

        Args:
            method (str) : HTTP method for request
            url (str) : url to send request to

        Kwargs:
            headers (dict) : desired request headers for the request
            body (dict) : body data for POST, PATCH, PUT type requests
            params (dict) : query parameters for request NOTE: query params 
                            can also be passed directly into the url.

        Returns 
            response (obj) : requests.Response instance object

        """
        headers = kwargs.get('headers')
        body = kwargs.get('body')
        params = kwargs.get('params')

        # type checking
        if headers and not isinstance(headers, dict):
            raise TypeError(
                "Expected type dict for headers | received type: {}".format(
                    type(headers))
            )

        if body and not isinstance(body, dict):
            raise TypeError(
                "Expected type dict for body | received type: {}".format(
                    type(headers))
            )
        # if no headers are provided, default to the following
        if not headers:
            headers = {
                "Prefer": "transient",
                "Content-Type": "application/json",
                "cache-control": "no-cache"
            }

        # request library raises ValueError if GET or HEAD requests contain a body
        if method.upper() in ("GET", "HEAD"):
            res = requests.request(method.upper(), url,
                                   headers=headers, auth=self.auth, params=params)
        # all other requests can have the body passed
        else:
            res = requests.request(method.upper(), url,
                                   headers=headers, auth=self.auth, params=params, data=json.dumps(body, default=str))

        return res
