The San Francisco Municipal Transportation Agency (SFMTA) keeps an updated database on all parking tickets collected in the city since 2009, including information about the parking violation type, the street address where the violation occurred, the date of when the citation was issued, and more [1]. The overall goal of my project is to analyze these citations, how much revenue they generate, and how they are geospatially and temporarily distributed. I will approach this with a comprehensive pipeline including data collection, data processing, data analysis, and database upkeep.

An overview of the workflow of this project is as follows:
1.	Obtain a static download of SFMTA parking data and create a SQL database with its contents.
2.	Update the database with new parking citations as they occur by calling an API from the SFMTA [2].
3.	Subset the data where GPS coordinates exist, and conduct geospatial data analysis on the individual parking citation level.
4.	Subset the data and match street addresses with zipcodes using the USPS ZipCode Lookup API, and conduct geospatial data analysis on the zipcode level.
5.	Repeat steps 3-4, query the database, and subset and process the data as needed to conduct a robust data analysis.



*** SCRIPTS ***

fetch_api.py: Defines functions that:
	1. fetches parking citation data from the SMFTA API given a timeframe
	2. matches street addresses with zip codes using the USPS zipcode lookup API

create_database.py: Creates a SQLite database of parking citations from static csv download 
	(https://data.sfgov.org/widgets/ab4h-6ztd)

update_database.py: Adds new parking citation data (between the present and the last entry on the
	database) using the SMFTA API; fetches data one day at a time

get_data.py: Subsets data from the database based on year; matches zipcodes to street addresses on a subset of a given year; 	subsets data where coordinates (geom) exists.


*** NOTEBOOKS ***
exploratory_data_analysis.ipynb: Creates visualizations and explores summary statistics based on subsets on the parent data. 	Explores citations vs. time of day, estimated revenue vs. zip code, etc...

*** DATA SOURCES ***
SF Parking Citation Data - https://data.sfgov.org/widgets/ab4h-6ztd
SFMTA API - https://dev.socrata.com/foundry/data.sfgov.org/ab4h-6ztd
SF Zip Codes and Population GeoJSON - https://data.sfgov.org/Geographic-Locations-and-Boundaries/San-Francisco-ZIP-Codes/srq6-hmpi
USPS ZipCode Lookup API - https://www.usps.com/business/web-tools-apis/address-information-api.htm


