*** SCRIPTS ***

fetch_api.py: Defines functions that:
	1. fetches parking citation data from the SMFTA API given a timeframe
	2. matches street addresses with zip codes using the USPS zipcode lookup API

create_database.py: Creates a SQLite database of parking citations from static csv download 
	(https://data.sfgov.org/widgets/ab4h-6ztd)

update_database.py: Adds new parking citation data (between the present and the last entry on the
	database) using the SMFTA API; fetches data one day at a time

get_data.py: Subsets data from the database based on year (also adds zipcodes to a subset of a given year); subsets data where coordinates (geom) exists.


*** NOTEBOOKS ***
visualizations.ipynb: Creates visualizations based on subset on the data. Explores citations vs. time of day, estimated revenue vs. zip code, etc...

*** DATA SOURCES ***
SF Parking Citation Data - https://data.sfgov.org/widgets/ab4h-6ztd
SFMTA API - https://dev.socrata.com/foundry/data.sfgov.org/ab4h-6ztd
SF Zip Codes and Econometrics GeoJSON - https://data.sfgov.org/Geographic-Locations-and-Boundaries/San-Francisco-ZIP-Codes/srq6-hmpi
USPS ZipCode Lookup API - https://www.usps.com/business/web-tools-apis/address-information-api.htm


