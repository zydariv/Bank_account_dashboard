import sqlite3
from sqlite3 import Error
import pandas as pd


def connect_to_db(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return conn


def read_all_transactions(transaction_table, conn):
    transactions_df = pd.read_sql(f"SELECT * FROM {transaction_table}", conn)

    return transactions_df


def write_transactions(transactions_df, transaction_table, conn):
    row_count = transactions_df.to_sql(name=transaction_table, con=conn, if_exists='append')
    print(f"{row_count} rows inserted into {transaction_table}")