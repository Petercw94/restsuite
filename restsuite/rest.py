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
