"""
Module for interacting with Netsuite Restlets
"""

from .base_rest import Rest


class NetSuiteRESTlet(Rest):
    """
    """

    def __init__(self, account_id, consumer_key, consumer_secret, token_key=None, token_secret=None) -> None:
        super().__init__(account_id, consumer_key, consumer_secret, token_key, token_secret)


"""
Notes on Restlets:

A restlet is a SuiteScript that executes when called by an external application or by another SuiteScript.
Depending on how the RESTlet is written and called, it may also return data to the calling application.

High level overview of RESTlet functionality:
---------------------------------------------

    - Retrieving, adding, or manipulating data within NetSuite, from an external source. In this sense, 
        RESTlets can be seen as an alternative to NetSuite's SOAP-based web services.
    - Customizing the behavior of pages and features within NetSuite. In this sense, RESTlets can be 
        seen as an alternative to other script types, such as Suitelets. The advantage of using a RESTlet 
        compared with a Suitelet is that the RESTlet can return data, in plain text or JSON, to the client
        script.

To use a RESTlet, you must create a script record and a deployment record based on the RESTlet script file.

When you save a script deployment record for a RESTlet, the system automatically generates a URL that 
can be used to call the RESTlet. NOTE: Because a RESTlet executes only when it is called, this information
is critical for using the RESTlet.

When you are ready to call a RESTlet that you have deployed, you can use one of four supported HTTP
methods:
    1. DELETE
    2. GET
    3. POST
    4. PUT

For most RESTlet calls, you must also include a content-type header, which tells Netsuite how your request body
will be formatted and how NetSuite should format its response.



DEPLOYING A RESTLET:

Before using a RESTlet, you must ensure the following two guidelines are met:
    1. Make sure the script is formattted properly (https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_4618456517.html#bridgehead_4625305314)
    2. Create a Script and Script Deployment Record (https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_4618456517.html#bridgehead_4625321026)

1. Make sure the script is formatted properly:

All of the following must be True:
    - The script must have an interface that includes at least one entry point appropriate for RESlet script type. 
    - The script must contain a corresponding entry point as the interface.
    - The script must use the required JSDoc tags. The @NScriptType must be RESTlet (or Restlet; not case-sensiive)

2. Create a Script and Script Deployment Record:
    - RESTlet script must be uploaded to File Cabinet before it can be called.
    - From the file cabinet, you can create a script record ad script deployment record.
    - When creating these records, be aware of the following:
        - You should enter meaningful data in the script record's ID field and the script 
            deployment record's ID field. When you save the records, the system creates IDs 
            that include the text you entered. One possible use of these IDS is to identify 
            the RESTlet when calling it from another SuiteScript. For this reason, it may 
            be helpful to have created meaningful ID strings.
        - Unlike some other script types, you do not deploy a RESTlet for any particular 
            record type. Each RESTlet is available independently of any particular record type 
            or record instance.
        - The script deployment record includes a field called Status, which has possible 
            values of Released and Testing. Before you can call the RESTlet from an external 
            source, the Status field must be set to Released.
        - When you save a script deployment record for a RESTlet, the system automatically 
            generates a partial and full URL that you can use to call the RESTlet. However, if 
            you are calling the RESTlet from within an integration and you want to use the full 
            URL, you must include logic that dynamically discovers the RESTlet domain. See the 
            following image for an example of internal and external RESTlet URLs. For more information, 
            see Identifying a RESTlet in a Call.



IDENTIFYING A RESTLET IN A CALL:

This module will assume all RESTlet calls to be made from an external client (i.e. Not from Netsuite itself).
Thus, it will need to be identified as follows:
"A full URL, similar to the one shown on the script deployment record, in the External URL field."

Dynamically Generating a Full URL
---------------------------------

"When you save a script deployment record for a RESTlet, the system automatically generates a full URL
that can be used to call the RESTlet. This value is shown in the External URL field.

However, in general, you should not hard-code this URL in a script, or in any other part of your integration.
Instead, you should create logic that dynamically generates the portion of the URL that represents
the RESTlet domain. This can be done with the REST Roles Service.

NOTE: As of 2017.2, account-specific domains are supported for RESTlets, and you can access your 
RESTlet domain at the following URL:
    
    <accountID>.restlets.api.netsuite.com

The data-center specific domains supported before 2017.2 will continue to be supported.

NOTE: I think maybe adding the Roles Service dynamic creation is something for a later version.
Doesn't seem to high priority for a working roll out if the above account-specific domain will work 
for majority of use cases.



SELECTING AN HTTP METHOD FOR CALLING A RESTLET:

For a method call to be successful, the method used in the call must match an entry point defined
in the RESTlet's interface.

Example (JavaScript) from NetSuite docs:

// Here, a Suitelet calls a RESTlet: 
var response = https.get({url: url, headers: headers})

// RESTlet script
// In this function, the RESTlet retrieves 
// a standard NetSuite record.
function _get(context) {
    doValidation([context.recordtype, context.id], ['recordtype', 'id'], 'GET');

    return record.load({
        type: context.recordtype,
        id: context.id
    })
}

return {
    get: _get,
}

NOTE: Although the entry points must match between the request and the RESTlet interface,
the functionality is determined by the RESTlet, which means the functionality may not
necessarily correlate with the intended behavior of the HTTP method being used.


"""
