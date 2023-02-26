*** SCRIPTS ***

fetch_api.py: Defines functions that:
	1. fetches parking citation data from the SMFTA API given a timeframe
	2. matches street addresses with zip codes using the USPS zipcode lookup API

create_database.py: Creates a SQLite database of parking citations from static csv download 
	(https://data.sfgov.org/widgets/ab4h-6ztd)

update_database.py: Adds new parking citation data (between the present and the last entry on the
	database) using the SMFTA API; fetches data one day at a time

get_data.py: Subsets data from the database based on year (also adds zipcodes to a subset of a given year); subsets data where coordinates (geom) exists.
		


