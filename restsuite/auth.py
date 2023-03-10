"""
Authentication methods for Netsuite API Usage
"""

import hmac
import hashlib
import base64
import struct
import time
import datetime as dt
import uuid
import requests
import urllib.parse


class NetsuiteOAuth:

    def __init__(self, account_id: str, consumer_key: str, consumer_secret: str, token_key=None, token_secret=None):
        self.realm = account_id
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.token_key = token_key
        self.token_secret = token_secret
        self.signature_method = "HMAC-SHA256"
        self.nonce = None
        self.timestamp = None
        self.request_parameters = None
        self.signature = None
        self.normalized_request_parameters = None
        self.headers = None
        self.base_string = None
        self.oauth_string = None

    def generate_nonce(self):
        """

        RFC5849: 3.3
        ------------
        A nonce is a random string, uniquely generated by the client to allow
        the server to verify that a request has never been made before and
        helps prevent replay attacks when requests are made over a non-secure
        channel.  The nonce value MUST be unique across all requests with the
        same timestamp, client credentials, and token combinations.

        """

        self.nonce = uuid.uuid4().hex + uuid.uuid1().hex

    def generate_timestamp(self):
        """

        RFC5849: 3.3
        ------------
        The timestamp value MUST be a positive integer.  Unless otherwise
        specified by the server's documentation, the timestamp is expressed
        in the number of seconds since January 1, 1970 00:00:00 GMT.

        """

        self.timestamp = str(int(time.time()))

    def generate_base_string(self, http_method, url):
        """
        RFC 5849: Section 3.4.1 (https://www.rfc-editor.org/rfc/rfc5849#section-3.4.1)
        ------------------------------------------------------------------------------

        The signature base string is a consistent, reproducible concatenation of several of the HTTP request elements into a single string. 
        The string is used as an input to the "HMAC-SHA1" and "RSA-SHA1" signature methods.

            - The HTTP request method (e.g. "GET", "POST", etc.).
            - The authority as declared by the HTTP "Host" request header field.
            - The path and query components of the request resource URI.
            - The protocol parameters excluding the "oauth_signature".
            - Parameters included in the request entity-body if they comply with the strict restrictions defined in Section 3.4.1.3. (https://www.rfc-editor.org/rfc/rfc5849#section-3.4.1.3)

        e.g. from Netsuite:
            GET&https%3A%2F%2F123456.suitetalk.api.netsuite.com%2Fservices%2Frest%2Frecord%2Fv1%2Femployee%2F40&oauth_consumer_key%3Def40afdd8abaac111b13825dd5e5e2ddddb44f86d5a0dd6dcf38c20aae6b67e4%26oauth_nonce%3DfjaLirsIcCGVZWzBX0pg%26oauth_signature_method%3DHMAC-SHA256%26oauth_timestamp%3D1508242306%26oauth_token%3D2b0ce516420110bcbd36b69e99196d1b7f6de3c6234c5afb799b73d87569f5cc%26oauth_version%3D1.0 

        """

        # Nonce and Timestamp are needed for the base uri
        self.generate_nonce()
        self.generate_timestamp()

        # remove parameters from base_url
        base_url, url_params = self.parse_url_parameters(url)

        # TODO: add url params to params to be normalized

        try:
            self.normalize_request_parameters(url_params)

        except KeyError as err:
            raise KeyError(
                "Missing Key for parameter string: {}. Please set this attribute before generating the base string. For reference to all available attributes, refer to this modules README.".format(err.args[0]))

        self.base_string = "{}&{}&{}".format(
            http_method, self.encode_oauth(base_url), self.normalized_request_parameters)

    def generate_signature(self):
        """
        signature = HMAC-SHA256(key, text)

        Where:

        - The value of the text parameter is the base string formatted acccording to RFC 5849 Section 3.4.1.2 (https://www.rfc-editor.org/rfc/rfc5849#section-3.4.1.2)

        - The value of the key parameter is the concatenation???using the ampersand (&) 
            character???of the consumer secret and the token secret with both values 
            encoded by the algorithm described in Encoding.

        - The result digest octet string is used as the resulting 
            oauth_signature parameter after:

            - being Base64-encoded. (For more information about Base64 
                Content-Transfer-Encoding, see Section 6.8 of RFC 2045.

            - being encoded using the algorithm described in Encoding.
        """

        # step 1: create the key and text values

        key = "{}&{}".format(self.consumer_secret,
                             self.token_secret)

        text = self.base_string

        # step 2: pass key and text values into the HMAC-SHA256 formula to generate signature
        signature = hmac.new(key=str.encode(key),
                             msg=str.encode(text), digestmod=hashlib.sha256).digest()

        # step 3: base64 encode the resulting signature
        encoded_signature = base64.b64encode(signature).decode()

        # step 4: encode using Percent Encoding
        self.signature = self.encode_oauth(encoded_signature)

    def generate_auth_header(self, http_method, url):
        """
        NOTE: See 3.5 of RFC 5849 for when to normalize request parameters (https://www.rfc-editor.org/rfc/rfc5849#section-3.5)


        """

        self.generate_base_string(http_method, url)
        self.generate_signature()

        self.oauth_string = "OAuth realm=\"" + self.realm + "\"," \
            "oauth_consumer_key=\"" + self.consumer_key + "\"," \
            "oauth_token=\"" + self.token_key + "\"," \
            "oauth_signature_method=\"HMAC-SHA256\"," \
            "oauth_timestamp=\"" + self.timestamp + "\"," \
            "oauth_nonce=\"" + self.nonce + "\"," \
            "oauth_version=\"1.0\"," \
            "oauth_signature=\"" + self.signature + "\""

        self.headers = {
            "Prefer": "transient",
            "Content-Type": "application/json",
            "Authorization": self.oauth_string,
            "cache-control": "no-cache"
        }

        return self.headers

    def normalize_request_parameters(self, query_parameters=None):
        """
        NOTE: See 3.5 of RFC 5849 for when to normalize request parameters (https://www.rfc-editor.org/rfc/rfc5849#section-3.5)

        The following parameters to be normalized into a single string are:

        - oauth_consumer_key
        - oauth_token
        - oauth_nonce
        - oauth_signature_method
        - oauth_timestamp

        Note: The single string of normalized parameters is to be encoded using the algorithm 
            described in Request Parameters Normalization.


        * The parameters that are used include: (refer to Request Parameters, Section 3.4.1.3 of RFC 5849):

        - parameters from the Authorization header (excluding ???realm??? and ???oauth_signature??? : "The "oauth_signature" parameter MUST be 
                                                        excluded from the signature base string if present." - Section 3.4.1.3.1 of RFC 5849)
        - parameters from the HTTP request entity body
        - parameters from the query part of the request URL

        Algorithm for normalizing parameters (see Section 3.4.1.3.2 of RFC 5849)
        ------------------------------------------------------------------------
            1. Encoding of parameter names and values occurs using the algorithm described in Encoding.

            2. Sorting by name is performed using ascending byte value ordering. If names are identical, sorting is done by values.

            3. Names and values form pairs separated by the equal (=) symbol, even when there is no value.

            4. Pairs are concatenated in the defined order by the ampersand (&) symbol.

        """

        # step 1: Encode the name-value request parameter pairs
        # ------------------------------------------------------

        request_params = {
            "oauth_consumer_key": self.consumer_key,
            "oauth_token": self.token_key,
            "oauth_signature_method": self.signature_method,
            "oauth_timestamp": self.timestamp,  # percent encode timestamp here for signature
            "oauth_nonce": self.nonce,
            "oauth_version": "1.0"
        }

        # add the query parameters if present
        if query_parameters:
            for key, value in query_parameters.items():
                request_params[key] = value

        # encoded_params = {}  # declare a new empty dictionary for storing encoded keys and values
        # for key, value in request_params.items():
        #     try:
        #         encoded_params[self.encode_oauth(
        #             key)] = self.encode_oauth(value)
        #     except TypeError as err:
        #         print("Missing required parameter: {}.".format(key))

        # step 2: sort by name
        # ---------------------
        sorted_encoded_params = {}

        for key in sorted(request_params.keys()):
            sorted_encoded_params[key] = request_params[key]

        # step 3: compile request parameter string
        # -----------------------------------------
        param_string = ""
        for key, value in sorted_encoded_params.items():
            param_string += "{}={}&".format(key, value)

        param_string = param_string[:-1]  # remove the final amperstand

        self.normalized_request_parameters = self.encode_oauth(
            param_string)  # encode the amperstands

    @staticmethod
    def encode_oauth(_string):
        """
        Encode desired string with Percent-Encoding




        NETSUITE DOCS SNIPPET: 
        -------------

        For more information about encoding, refer to Section 3.6 of RFC 5849:

            - For Text values, refer to RFC 3629. Text values must be encoded as UTF-8 octets if they are not already encoded.

            - Values are escaped using the Percent-Encoding (%XX) mechanism:

                - Do not encode characters from the unreserved character set. 
                Refer to Section 2.3 of RFC 3986 for documentation of the unreserved character set.

                - All other characters must be encoded.

                - Two hexadecimal characters used to represent encoded characters must be uppercase.

        * IMPORTANT: A blank symbol is encoded as %20 and not as the plus (+) symbol.
        Be aware that some framework functions may return unwanted results.

        """

        from urllib.parse import quote_plus, quote

        # quote_plus defaults to no safe encodings and replaces spaces with + which corresponds to oauth standards
        return quote_plus(_string, safe='-._~')  # , safe='~()*!.\''
        # if the endpoints require the blank spaces to be percent encoded instead, use quote(uri, safe='') instead

    @staticmethod
    def parse_url_parameters(url: str):
        """
        Converts the url parameters into a dictionary.

        NOTE: This parsing function is specific for Netsuite API functionality.
        It is not set to handle multiple parameters of the same name. If multiple
        parameters are passed, it will only take the first parameter in the returned
        list from parse_qs.

        Args:
        -----
            - url (str) -> The full url with parameters that need parsing

        Returns:
        --------
            - base_url (str) -> The base url without query parameters
            - parameters (dict) -> The query parameters in dictionary form

        """

        url_list = url.split("?")

        base_url = url_list[0]

        if len(url_list) > 1:
            params_list_form = urllib.parse.parse_qs(url_list[1])

            # parse_qs returns values as lists, so these will need to be converted
            # for the oauth signature method.
            parameters = {}
            for key, value in params_list_form.items():
                # only take the first parameter if multiple are present
                parameters[key] = value[0]

        # If no URL parameters, return None
        else:
            parameters = None

        return base_url, parameters

    # the following functions were referenced from: https://stackoverflow.com/questions/8529265/google-authenticator-implementation-in-python
    @staticmethod
    def generateHOTP(secret, intervals_no):
        key = base64.b32decode(secret, True)
        # decoding our key
        msg = struct.pack(">Q", intervals_no)
        # conversions between Python values and C structs represented
        h = hmac.new(key, msg, hashlib.sha1).digest()
        o = h[19] & 15
        # generate a hash using both of these. Hashing algo is HMAC
        h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
        # unpack
        return h

    @classmethod
    def generateTOTP(cls, secret):
        # ensure to give the same otp for 30 seconds
        return cls.generateHOTP(secret, intervals_no=int(time.time())//30)
