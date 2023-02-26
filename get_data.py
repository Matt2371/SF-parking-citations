import numpy as np
import sqlite3 as sql
import pandas as pd
from pandas import read_sql
import matplotlib.pyplot as plt
from tqdm import tqdm
import fetch_api


def subset_year(connection, year):
    """Fetch data from database from a given year, save as csv"""
    next_year = year + 1

    query_str = f"""
            SELECT * FROM parking_citations
            WHERE citation_issued_datetime BETWEEN '{str(year)}-01-01' AND '{str(next_year)}-01-01'
            """

    result = read_sql(query_str, connection)
    result.to_csv('csv/parking_citations_' + str(year) + '.csv', index=False)

    return result


def zip_codes(year, app_token, frac=0.1):
    """Queries USPS zipcode lookup API to add zipcodes to a subset of data from a given year.
    frac is fraction of data to be subsetted
    Requires csv output from subset_year()"""

    # read csv parking citation data from a given year
    df = pd.read_csv(f'csv/parking_citations_{str(year)}.csv')
    # subset data
    df = df.sample(frac=frac, random_state=0)
    dimensions = df.shape

    # USPS Zipcode lookup only takes 5 inputs at a time
    # Create an array of indices to iterate over
    indices = np.arange(0, dimensions[0], 5)
    indices = np.concatenate((indices, [dimensions[0]]))

    # Query zip codes from 5 addresses at a time
    for i in tqdm(range(len(indices) - 1), desc='fetching zip codes:'):
        lower = indices[i]
        upper = indices[i + 1]

        # Get addresses from parking citation data
        addresses = df.loc[df.index[lower:upper], 'Citation_Location'].values

        # Get respective zip codes
        zip_codes = fetch_api.usps_zipcode(app_token=app_token, street_addresses=addresses)

        # Update dataframe
        df.loc[df.index[lower:upper], 'Zip_Code'] = zip_codes

    # Save result as csv
    df.to_csv(f'csv/subset_{year}_w_zipcodes.csv', index=False)

    return df


def geom_counts(connection):
    """Get a plot of number of geometries tracked per year"""

    years = np.arange(2008, 2023)
    # Store counts of geometries stored
    geom_counts = np.empty(15)

    for i in tqdm(range(15), desc='fetching counts'):
        year = years[i]
        next_year = year + 1

        query_str = f"""
        SELECT COUNT(citation_number) AS count FROM parking_citations
        WHERE citation_issued_datetime BETWEEN '{str(year)}-01-01' AND '{str(next_year)}-01-01'
        AND geom IS NOT NULL
        """
        result = read_sql(query_str, connection)

        # Update array of counts
        geom_counts[i] = result['count']

    plt.bar(years, geom_counts)
    plt.xlabel('Year')
    plt.ylabel('Coordinates')
    plt.title('Number of coordinates tracked per year')
    plt.tight_layout()
    plt.savefig('figures/num_coordinates.png', dpi=300)

    return geom_counts


def subset_geom(connection, year):
    """Get data where coordinates (geom) exists for a given year"""
    next_year = year + 1

    query_str = f"""
            SELECT * FROM parking_citations
            WHERE citation_issued_datetime BETWEEN '{str(year)}-01-01' AND '{str(next_year)}-01-01'
            AND geom IS NOT NULL
            """

    result = read_sql(query_str, connection)
    result.to_csv('csv/parking_citations_w_geom_' + str(year) + '.csv', index=False)

    return result


def main():
    # Open connection with db
    connection = sql.connect("sfmta_parking_citations.db")
    cursor = connection.cursor()

    # Save data from 2022 as csv
    subset_year(connection=connection, year=2022)

    # Match zip codes with subset of 2022 data, save as csv
    # Read USPS app token
    usps_token = fetch_api.read_token('API_token/usps_userid.txt')
    zip_codes(year=2022, app_token=usps_token, frac=0.001)

    # Get counts of coordinates per year
    geom_counts(connection=connection)

    # We find that coordinate tracking declines sharply after 2019. Grab datapoints from 2019 where geometries exist
    subset_geom(connection=connection, year=2019)

    # Close the connection
    connection.close()

    return


if __name__ == "__main__":
    main()
