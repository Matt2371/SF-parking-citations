import pandas as pd
import sqlite3 as sql


### RUN SCRIPT ONCE TO CREATE DATABASE FROM STATIC CSV DOWNLOAD ###

def main():
    """Read in static csv (downloaded from https://data.sfgov.org/widgets/ab4h-6ztd). Create SQLite database from
    file """
    # read data, rename columns
    df = pd.read_csv('csv/SFMTA_-_Parking_Citations.csv')

    rename_dict = {'Citation Number': 'Citation_Number',
                   'Citation Issued DateTime': 'Citation_Issued_DateTime',
                   'Violation': 'Violation',
                   'Violation Description': 'Violation_Description',
                   'Citation Location': 'Citation_Location',
                   'Vehicle Plate State': 'Vehicle_Plate_State',
                   'Vehicle Plate': 'Vehicle_Plate',
                   'Fine Amount': 'Fine_Amount',
                   'Date Added': 'Date_Added',
                   'geom': 'geom'}
    df = df.rename(columns=rename_dict)

    # Convert dates to ISO format
    df['Citation_Issued_DateTime'] = pd.to_datetime(df['Citation_Issued_DateTime'])
    df['Citation_Issued_DateTime'] = df['Citation_Issued_DateTime'].map(lambda x: x.isoformat())
    df['Date_Added'] = pd.to_datetime(df['Date_Added'])
    df['Date_Added'] = df['Date_Added'].map(lambda x: x.isoformat())

    # Create SQL Database (sql.connect() will make a new database if one does not already exist)
    connection = sql.connect("sfmta_parking_citations.db")
    cursor = connection.cursor()

    # Create table to store parking citation data
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS parking_citations
        (Citation_Number TEXT,
        Citation_Issued_DateTime DATETIME,
        Violation TEXT,
        Violation_Description TEXT,
        Citation_Location TEXT,
        Vehicle_Plate_State TEXT,
        Vehicle_Plate TEXT,
        Fine_Amount REAL,
        Date_Added DATETIME,
        geom TEXT)

    ''')

    # Update database from Pandas
    df.to_sql('parking_citations', connection, if_exists='replace', index=False)

    # # Check work
    # test = read_sql("SELECT * FROM parking_citations", connection)
    # print(test.head())

    # Close database
    connection.close()

    return


if __name__ == "__main__":
    main()
