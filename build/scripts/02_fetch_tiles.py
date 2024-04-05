from PIL import Image
import pandas as pd
from agonImages import rgba8_to_img
import sqlite3
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import csv


def make_tbl_tiles(db_path, tbl_name, src_tiles_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f'DROP TABLE IF EXISTS {tbl_name}')
    cursor.execute(f'''
        CREATE TABLE {tbl_name} (
            bank_id INT,
            obj_id INT PRIMARY KEY,
            tile_name TEXT,
            is_active INT,
            is_door INT,
            is_wall INT,
            is_trigger INT,
            is_blocking INT,
            render_type TEXT,
            render_as INT,
            scale INT,
            special TEXT,
            notes TEXT
        )
    ''')
    df_tiles = pd.read_csv(src_tiles_path, sep='\t')
    df_tiles = df_tiles[df_tiles['is_active'] == 1]
    df_tiles.to_sql(tbl_name, conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()

import sqlite3

def get_column_names(db_path, tbl_name):
    """
    Queries the SQLite database schema for a specific table to retrieve the column names.

    Parameters:
    - db_path: Path to the SQLite database file.
    - tbl_name: Name of the table for which to retrieve the column names.

    Returns:
    - columns: A list of column names for the specified table.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Use PRAGMA table_info to get information about the table schema
    query = f"PRAGMA table_info({tbl_name})"
    cursor.execute(query)

    # Extract the column names from the query result
    columns = [row[1] for row in cursor.fetchall()]

    # Close the database connection
    conn.close()

    return columns

def get_google_sheets(db_path, src_tiles_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('src/assets/credentials.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    sheet = client.open("Tiles").sheet1

    # Extract and print all of the values
    list_of_hashes = sheet.get_all_records()
    df = pd.DataFrame(list_of_hashes)
    df.to_csv(src_tiles_path, sep='\t', index=False)

    # Read the tab-delimited file and insert into the database
    with open(src_tiles_path, 'r', encoding='utf-8') as file:
        dr = csv.DictReader(file, delimiter='\t', fieldnames=columns)
        to_db = [(i['Column1'], i['Column2'], i['Column3']) for i in dr]  # Adjust this line

    # Insert the data into the table
    cursor.executemany(f"INSERT INTO {tbl_name} (Column1, Column2, Column3) VALUES (?, ?, ?);", to_db)  # Adjust this line
    conn.commit()

    # Close the connection
    conn.close()

if __name__ == "__main__":
    db_path = 'build/data/build.db'
    tbl_name = 'tbl_02_tiles'
    data_dir = 'build/data'
    mapmaker_tiles_dir = 'src/assets/mapmaker'
    src_tiles_path = f'{mapmaker_tiles_dir}/tiles.txt'
    base_texture_tgt_dir = 'build/panels/uv'

    make_tbl_tiles(db_path, tbl_name, src_tiles_path)
    columns = get_column_names(db_path, tbl_name)

    print("Data loaded into SQLite database successfully.")
