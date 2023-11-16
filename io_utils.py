import pandas as pd
import streamlit as st
from os.path import join
from datetime import datetime
import toml


pd.set_option('display.max_columns', 12)

def parse_dtypes(df):
    parse_currency = lambda x: float(x.replace('.','').replace(',','.').replace('\xa0€', ''))
    df['Betrag'] = df['Betrag'].map(parse_currency)
    return df

@st.cache_data
def read_transaction_file(transaction_file_name):
    # New format
    #dateparse = lambda x: datetime.strptime(x, '%d.%m.%y')
    dateparse = lambda x: datetime.strptime(x, '%d.%m.%Y') # old format
    
    raw_transaction_df = pd.read_csv(join("Transactions", transaction_file_name),
                                     sep=";", parse_dates=["Buchungsdatum", "Wertstellung"],
                                     date_parser=dateparse)
    transaction_df = parse_dtypes(raw_transaction_df)
    return transaction_df


def parse_toml_conf():
    toml_conf = toml.load("config.toml")
    return toml_conf