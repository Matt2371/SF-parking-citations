import pandas as pd
import requests
import xmltodict
import time
import numpy as np
import re


def read_token(filepath):
    """Read API token"""
    with open(filepath) as file:
        return file.readline().strip("\n")


def sfmta_parking(app_token, past_datetime='', present_datetime='', **kwargs):
    """Access sfmta parking citations API between `past_date` and `present_datetime` in ISO8601 format.
    Request `limit` as **kwargs
    Returns a Pandas Dataframe of results
    Full API documentation can be found: https://dev.socrata.com/foundry/data.sfgov.org/ab4h-6ztd"""

    # Read in api token as header
    header_dict = {'X-App-Token': app_token}

    # Get limit if provided
    limit = kwargs.get('limit', 100000)

    # Build dictionary of HTTP parameters
    # SoQL Query to limit result past a certain date
    params_dict = {'$where': 'citation_issued_datetime BETWEEN ' + '\'' + past_datetime + '\'' +
                             ' AND ' + '\'' + present_datetime + '\'',
                   '$limit': limit,
                   }

    # Get data
    request = requests.get('https://data.sfgov.org/resource/ab4h-6ztd.json', headers=header_dict, params=params_dict)
    request.raise_for_status()

    # Cast request into Pandas Dataframe
    request_df = pd.DataFrame(request.json())

    return request_df


def usps_zipcode(app_token, street_addresses):
    """Get zipcode given `street_addresses`, a LIST/ARRAY OF UP TO 5 addresses from San Francisco.
    RETURNS list of 5 corresponding zip codes
    Access USPS zipcode lookup (by address, city, state)
    Docs: https://www.usps.com/business/web-tools-apis/address-information-api.htm"""

    # Handle case when proceeding 0 breaks address search (i.e. 23 01ST instead of 23 1ST) using regular expressions
    for i in range(len(street_addresses)):
        if type(street_addresses[i]) == str:
            street_addresses[i] = re.sub(r'(?<=\s)0', '', street_addresses[i])

    # Handle case when length of street_addresses is shorter than 5 (fill with None)
    temp = np.empty(5, dtype=object)
    length_addresses = len(street_addresses) # keep track of original length
    temp[0:length_addresses] = street_addresses
    street_addresses = temp

    # Build XML input (takes up to 5 addresses)
    xml = "<ZipCodeLookupRequest USERID=\"" + app_token + "\">" + """
    <Address ID="1">
    <Address1></Address1>
    <Address2>""" + str(street_addresses[0]) + """"</Address2>
    <City>San Francisco</City>
    <State>CA</State>
    </Address>
    
    <Address ID="2">
    <Address1></Address1>
    <Address2>""" + str(street_addresses[1]) + """"</Address2>
    <City>San Francisco</City>
    <State>CA</State>
    </Address>
    
    <Address ID="3">
    <Address1></Address1>
    <Address2>""" + str(street_addresses[2]) + """"</Address2>
    <City>San Francisco</City>
    <State>CA</State>
    </Address>
    
    <Address ID="4">
    <Address1></Address1>
    <Address2>""" + str(street_addresses[3]) + """"</Address2>
    <City>San Francisco</City>
    <State>CA</State>
    </Address>
    
    <Address ID="5">
    <Address1></Address1>
    <Address2>""" + str(street_addresses[4]) + """"</Address2>
    <City>San Francisco</City>
    <State>CA</State>
    </Address>
    
    </ZipCodeLookupRequest>
    """

    # Query API
    url = 'https://secure.shippingapis.com/ShippingAPI.dll?API=ZipCodeLookup&XML=' + xml
    request = requests.get(url=url)
    request.raise_for_status()

    # Parse XML response as python dictionary
    response_data = xmltodict.parse(request.content)

    # Get list of zipcodes
    zipcode_list = []
    for i in range(5):
        try:
            zipcode_list.append(response_data['ZipCodeLookupResponse']['Address'][i]['Zip5'])
        # None address or address does not exist
        except KeyError:
            zipcode_list.append(None)

    # Cut list back to match original length of zip codes
    zipcode_list = zipcode_list[0:length_addresses]

    return zipcode_list

# ## Test SFMTA parking API
# # Read app token
# sfmta_token = read_token('API_token/sfmta_app_token.txt')
#
# # Set desired times in ISO format
# today = dt.datetime.now()
# yesterday = today - dt.timedelta(days=1)
# yesterday = yesterday.isoformat()
# today = today.isoformat()
#
# # Get and print data
# df = sfmta_parking(app_token=sfmta_token, past_datetime=yesterday, present_datetime=today)
# print(df.head())


# # Test USPS Zipcode Lookup API
# begin = time.time()
# street_addresses = np.array(['3529 WASHINGTON BLVD', '530 HAYES ST', None, '385 06TH ST'])
# app_token = read_token('API_token/usps_userid.txt')
# result = usps_zipcode(app_token=app_token, street_addresses=street_addresses)
# print(result)
# duration = time.time() - begin
# print(duration)
