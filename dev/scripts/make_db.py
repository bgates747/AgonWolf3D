import sqlite3
import csv

def create_database(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    # Close the connection
    conn.close()

if __name__ == "__main__":
    db_path = 'build/data/build.db'
    create_database(db_path)
    print(f"Database and table created at {db_path}")

