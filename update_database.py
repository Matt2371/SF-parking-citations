import sqlite3 as sql
from pandas import read_sql
import datetime as dt
import fetch_api
from tqdm import tqdm


def last_entry(connection):
    """Get the date of the last entry in the database"""
    # Get most recent entry
    query_str = """
    SELECT * FROM parking_citations
    ORDER BY citation_issued_datetime DESC
    LIMIT 1
    """
    result = read_sql(query_str, connection)
    last_datetime = result['Citation_Issued_DateTime'][0]

    return last_datetime


def update_citations(connection):
    """Update parking citations database using sfmta API. Fetch data (one day at
    a time) between last entry in database and current date"""

    # Get the time delta (in days) between the last entry on database and present date
    last_date = last_entry(connection=connection)  # Get last date from database
    last_date = dt.datetime.fromisoformat(last_date)  # Convert to datetime object
    present_date = dt.datetime.now()
    time_delta = present_date - last_date
    time_delta = time_delta.days

    # Read SFMTA app token
    sfmta_token = fetch_api.read_token('API_token/sfmta_app_token.txt')

    # Get new data (one day at a time)
    last_fetch_date = last_date
    for i in tqdm(range(1, time_delta + 1), desc='Updating citations: '):
        fetch_date = last_date + dt.timedelta(days=i)

        # Fetch days data from sfmta api
        new_data = fetch_api.sfmta_parking(app_token=sfmta_token, past_datetime=last_fetch_date.isoformat(),
                                           present_datetime=fetch_date.isoformat())

        # Update last_fetch_date for next iteration
        last_fetch_date = fetch_date

        # Update database with new data (if new data is not empty)
        if len(new_data.index) != 0:
            # Rename columns on new data to match columns in database
            rename_dict = {'violation_desc': 'Violation_Description'}
            new_data = new_data.rename(columns=rename_dict)

            # Sometimes geom is returned, which will need to be renamed and converted to str tpype
            if 'the_geom' in new_data.columns:
                rename_dict = {'the_geom': 'geom'}
                new_data = new_data.rename(columns=rename_dict)
                new_data['geom'] = new_data['geom'].astype('str')

            # Send new data to database
            new_data.to_sql('parking_citations', connection, if_exists='append', index=False)
    return


def main():
    # Open connection with db
    connection = sql.connect("sfmta_parking_citations.db")
    cursor = connection.cursor()

    # Update with new data
    update_citations(connection=connection)

    # Close database
    connection.close()
    return


if __name__ == "__main__":
    main()
