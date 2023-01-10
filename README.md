# Restsuite

Restsuite is a python package developed to help developers interact with the Netsuite REST API. Restsuite offers a number of classes that can be utilized to interact with Netsuite's Suite-Talk, RESTlet, or SuiteQL services. Restsuite currently utilizes Netsuite's token authentication methods, however, current development is under way for supporting Netsuite's Oauth2 authentication methods. 

### Disclaimer:  

*Restsuite is still in developement stages and is currently being tested through usage in our company. Although open to the public for use, understand that this is not a stable version of the restsuite package. Integrating Restsuite into production applications at this stage is not advised.*

## Installation

Restsuite is part of the Python Package Index (PyPI) and can thus be installed with pip:

```
pip install restsuite
```

Restsuite requires a python version of 3.8 or higher and depends only on the [requests python package](https://requests.readthedocs.io/en/latest/) 


## Getting Started

As Restsuite is an abstraction of the Netsuite API, it will be helpful to become familiar with, or at least reference, the Netsuite API documentation:

- [Suite-Talk Documentation](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/chapter_1540391670.html)
- [RESTlet Documentation](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N2970701.html)
- [SuiteQL Documentation](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_156257770590.html)

### Authentication

Each of the provided classes (NetSuiteRest, NetSuiteRESTlet, NetSuiteQL) handle authentication for the developer. All that is required is basic account information that can be generated in the user's account integration settings (see [REST Web Services Prerequisites and Setup](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1544787084.html) for a guide on setting up your Netsuite application to utilize REST capabilities)

Each class requires that you pass the following attributes upon object instantiation:
- Netsuite Account ID : This can be found the Netsuite url path (e.g: *https://{{ account_id }}.app.netsuite.com)*)
- Consumer Key : Consumer Key and Secret are provided upon integration record creation [Integration Record Overview](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_4389727047.html).
- Consumer Secret : Consumer Secret is provided upon integation record creation [Integration Record Overview](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_4389727047.html)
- Token Key : Tokens can be generated a number of ways. We are currently developing a Class for generating tokens with the [issuetoken endpoint](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/chapter_157017286140.html). For the time being, you can [generate a token with the Netsuite UI](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/bridgehead_4254081947.html).
- Token Secret : See Token Key


## Suite-Talk

The *restsuite.NetSuiteRest* class provides an interface to NetSuite's [Suite-Talk API](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/chapter_1540391670.html). 

For a full list of available resources, see the [NetSuite REST API Browser: Record API v1](https://system.netsuite.com/help/helpcenter/en_US/APIs/REST_API_Browser/record/v1/2022.2/index.html)

#### Examples:

Instantiating a Suite-Talk object:
```python
import restsuite

netsuite = restsuite.NetSuiteRest(
    account_id = NS_ACCOUNT_ID,
    consumer_key = CONSUMER_KEY,
    consumer_secret = CONSUMER_SECRET,
    token_key = TOKEN_KEY,
    token_secret = TOKEN_SECRET
)
```

#### Getting a Record (GET):
```python
url = "https://{}.suitetalk.api.netsuite.com/services/rest/record/v1/job".format(NS_ACCOUNT_ID)

response = netsuite.get(url)

if response.status_code <= 300:
    data = response.json()
```
*[Getting docs]()*

*It is important to note here that all classes will require the full URL to be passed to each request method.*

#### Creating a Record object (POST):
```python
url = "https://{}.suitetalk.api.netsuite.com/services/rest/record/v1/job/12345".format(NS_ACCOUNT_ID)

body = {"entityid": "New Customer", "companyname": "My Company", "subsidiary": {"id": "1"}}

response = netsuite.post(url=url, body=body)
```
*[Creating docs](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1545141395.html)*

#### Updating a Record object (PATCH):
```python
url = "https://{}.suitetalk.api.netsuite.com/services/rest/record/v1/job/12345".format(NS_ACCOUNT_ID)

body = {"entityid": "Updated Customer"}

response = netsuite.patch(url=url, body=body)
```
*[Updating docs](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_1545142173.html)*

#### Upserting a Record object (PUT):
```python
url = "https://{}.suitetalk.api.netsuite.com/services/rest/record/v1/job/12345".format(NS_ACCOUNT_ID)

body = {"firstName": "John", "lastName": "Smith"}

response = netsuite.put(url=url, body=body)
```
*[Upsert docs](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_156335203191.html)*

#### Deleting a Record object (DELETE)
```python
url = "https://{}.suitetalk.api.netsuite.com/services/rest/record/v1/job/12345".format(NS_ACCOUNT_ID)

response = netsuite.delete(url=url)
```

## RESTlet

"A restlet is a SuiteScript that executes when called by an external application or by another SuiteScript. Depending on how the RESTlet is written and called, it may also return data to the calling application."

The *restsuite.NetSuiteRESTlet* class acts as an external application that allows you to activate RESTlets based on a handful of HTTP verbs:

- GET
- POST
- PUT
- DELETE

These verbs, however, act more as a guide than as the strict HTTP verbs described [here](https://www.w3schools.in/http/http-request-methods). This is because the actual actions taken are defined in the RESTlets themselves, and the verbs are used to call certain functions within the RESTlet. More information can be found on RESTlets [here](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N2970701.html).

#### Examples:

Calling a RESTlet is similar to the Suite-Talk methods shown above. Only one example will be given here to highlight the difference in the URL path, everything else will be the same.

#### Sending a GET request to RESTlet:
```python
import restsuite

netsuite = restsuite.NetSuiteRESTlet(
    account_id = NS_ACCOUNT_ID,
    consumer_key = CONSUMER_KEY,
    consumer_secret = CONSUMER_SECRET,
    token_key = TOKEN_KEY,
    token_secret = TOKEN_SECRET
)

url = "https://{}.restlets.api.netsuite.com/app/site/hosting/restlet.nl?script={}&deploy={}".format(NS_ACCOUNT_ID, SCRIPT_ID, DEPLOYMENT_ID)

response = netsuite.get(url)
```

## SuiteQL