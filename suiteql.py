"""
Module for making SuiteQL queries
"""

from .auth import NetsuiteOAuth
import requests


class NetSuiteQL:
    """
    """

    def __init__(self, account_id, consumer_key, consumer_secret, token_key=None, token_secret=None) -> None:
        self.auth = NetsuiteOAuth(
            account_id, consumer_key, consumer_secret, token_key, token_secret)
        self.url = "https://{}.suitetalk.api.netsuite.com/services/rest/query/v1/suiteql".format(
            account_id)
        self.items = []
        self.response_body = []

    def query(self, url, query_string: str):
        """
        Send SuiteQL query to Netsuite.

        This is the actual query function, or rather, the
        function that sends the Query itself to Netsuite via
        the Rest API. Since the response is limited and paginated,
        to return all the data for a query use the suiteql method.

        Args:
        -----
        - url (str) -> parameter passed from the RestAPI base_url
        - query_string (str) -> the SQL Query

        Returns:
        -------
        - response (obj) -> requests.response object from POST request.

        """

        body = '{"q": "' + query_string + '"}'

        headers = self.auth.generate_auth_header("POST", url)

        response = requests.post(url, headers=headers, data=body, cookies={
                                 'NS_ROUTING_VERSION': 'LAGGING'})

        return response

    def suiteql(self, query_string: str):
        """
        Returns all results for a SuiteQL query.

        Args:
        -----
        - query_string: the SuiteQL Query

        returns:
        -------
        An HTTP response as Dict

        """

        moreQueries = True
        next_url = self.url
        queryRun = 0

        while (moreQueries):
            moreQueries = False

            results = self.query(url=next_url, query_string=query_string)

            response = QueryResponse(results)

            if response.ok:
                moreQueries = response.hasMore

                if moreQueries:
                    next_url = response.links['next']

                self.response_body.extend(response.items)

                queryRun += 1
            else:
                return {}

        return self.response_body


class NetSuiteResponse:
    """ 
    Class for NetSuite API Reponses 
    """

    def __init__(self, response):
        self.response = response

        self.ok = response.ok
        self.status_code = response.status_code
        self.headers = response.headers

        if not response.ok:
            self.error_title = response.json()['title']
            self.error_type = response.json()['type']
            self.error_status = str(response.json()['status'])
            self.error_msg = response.json()['o:errorDetails'][0]['detail']

            self.print_error()

    def print_error(self):
        """
        Prints out any NetSuite API Reponses that result in errors

        args:
        -----
        - response: NetSuite API Response

        returns:
        -------
        response object that contains all messages associated with the error, 
        printed out in more reable format

        """

        print('ERROR')
        print('error_title: ' + self.error_title)
        print('error_title: ' + self.error_type)
        print('error_status: ' + str(self.error_status))
        print('error_msg: ' + str(self.error_msg))
        print('')


class QueryResponse(NetSuiteResponse):
    """ 
    Class for NetSuite SuiteQL Query Reponses. 
    Handles the parsing of the SuiteQL reponses and tidies it all up. 
    Handles the loop of the limit and offset that NetSuite imposes.
    """

    def __init__(self, response):
        super().__init__(response)

        self.links = {}
        self.count = 0
        self.hasMore = False
        self.offset = 0
        self.totalResults = 0
        self.items = []

        if response.ok:
            if response.status_code != 204:
                jsonResults = response.json()

                for link in jsonResults['links']:
                    self.links[link['rel']] = link['href']

                self.count = jsonResults['count']
                self.hasMore = jsonResults['hasMore']
                self.offset = jsonResults['offset']
                self.totalResults = jsonResults['totalResults']
                self.items = jsonResults['items']
