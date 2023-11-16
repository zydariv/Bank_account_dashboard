import pandas as pd
import numpy as np
from datetime import datetime


def parse_kategorie(df, kategorie, keywords):
   regex_keywords = '|'.join(f'(?i){keyword}' for keyword in keywords)
   regex_keywords = '|'.join(f'{keyword}' for keyword in keywords)

   df.loc[df['Zahlungsempfänger*in'].str.contains(regex_keywords, case=False), 'kategorie'] = kategorie
   return df


def add_kategorien(df, config):
   kategorien = config["kategorien"]
   for kategorie in kategorien.keys():
      df = parse_kategorie(df, kategorie, kategorien[kategorie])
   
   return df


def add_additional_columns(df, config):
   df['Betrag_absolut'] = df['Betrag'].abs()
   df = add_kategorien(df, config)
   return df   


def preprocess_transactions_df(transactions_df, config):
   transactions_df.dropna(subset=['Zahlungsempfänger*in'], inplace=True)
   transactions_df.loc[transactions_df['Betrag'] > 0, 'Umsatztyp'] = 'Eingang'
   transactions_df.loc[transactions_df['Betrag'] < 0, 'Umsatztyp'] = 'Ausgang' 
   transactions_df = add_additional_columns(transactions_df, config)
   return transactions_df


def filter_df_by_value(df, col, value):
   df = df[df[col] == value]
   return df


def resample_df(df, by, col, type_):
   df = df.resample(by).sum()
   df[col] = df.index
   df['Umsatztyp'] = type_
   return df


def resample_transactions(df, col, by, types):
   df_list = []
   for t in types:
      type_df = df[df['Umsatztyp'] == t]
      df_list.append(resample_df(type_df, by, col, t))

   df = pd.concat(df_list)
   df = df.sort_index()
   return df


def datetime64_to_datetime(datetime64):
   ts_ns = datetime64.astype(datetime)
   ts = ts_ns / 1000000000
   datetime_ = datetime.utcfromtimestamp(ts)
   return datetime_


def to_datetime(date):
    return np.datetime64(int(date.strftime("%s")),'s')


def cut_in_bins(df, bins):

   # Create a new DataFrame for results with a formatted index
   result_df = pd.DataFrame(index=[f'{lower+0.01}€-{upper:.2f}€' for lower, upper in zip([0-0.01] + bins[:-1], bins)],
                           columns=['sum', 'mean', 'std'])

   # Create a categorical column for grouping based on bins
   df['group'] = pd.cut(df['Betrag_absolut'], bins=[0]+bins, right=False)

   # Apply aggregation functions using groupby
   grouped = df.groupby('group')['Betrag_absolut']
   result_df['sum'] = grouped.sum().values
   result_df['mean'] = grouped.mean().values
   result_df['std'] = grouped.std().values

   # Drop the temporary 'group' column
   df.drop('group', axis=1, inplace=True)

   return result_df


def group_by_time(df, index_date, config, freq, agg_freq=None):
   """
   Params
   df DataFrame   : Containing transactional Data
   index_date str : Name of date column
   freq str       : What frequency do you want observe? 'weekday', 'month' 
   agg_freq str   : 'month', 'year' 
   """
   df = df.copy()

   if freq == "weekday":
      resample_col = "Wochentag"
      df[resample_col] = df[index_date].dt.day_name(locale=config['locale'])
      df[f"{resample_col}_idx"] = df[index_date].dt.dayofweek
   elif freq == "month":
      resample_col = "Monat"
      df[resample_col] = df[index_date].dt.month_name(locale=config['locale'])
      df[f"{resample_col}_idx"] = df[index_date].dt.month


   df = df.sort_values(by=f"{resample_col}_idx")
   if agg_freq:
      if agg_freq == "month":
         agg_column = "Monat"
         df[f"{agg_column}"] = df[index_date].dt.month_name(locale=config['locale'])
      elif agg_freq == "year":
         agg_column = "Jahr"
         df[f"{agg_column}"] = df[index_date].dt.year

      df = df[[resample_col, f'{resample_col}_idx', agg_column, 'Betrag_absolut']].groupby(by=[agg_column,resample_col], sort=False).sum().groupby(level=1, sort=False).sum()
   else:
      df = df[[resample_col, f'{resample_col}_idx', 'Betrag_absolut']].groupby(by=[resample_col], sort=False).sum()

   return df