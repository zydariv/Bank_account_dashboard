# Timestamps are UTC

from io_utils import *
from visualization_utils import *
from data_processing import *

import streamlit as st
from dateutil.relativedelta import relativedelta
import locale


st.set_page_config(
    page_title='Finanzdashboard',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='collapsed'
    )

transaction_file ="artificial_max_mustermann.csv"
config = parse_toml_conf()
locale.setlocale(locale.LC_ALL, config['locale'])
transactions_df = read_transaction_file(transaction_file)

transactions_df = preprocess_transactions_df(transactions_df, config)


index_datum = 'Buchungsdatum'
umsatztypen = transactions_df['Umsatztyp'].unique()


# Begin Layout
st.header("Finanz Dashboard", divider=True)

# 2 column layout
col1, col2 = st.columns(2)
df_ausgaben = filter_df_by_value(df=transactions_df, col='Umsatztyp', value='Ausgang')

with col1:
    
    
    st.subheader(f"Ausgaben nach Kategorien")
    torten_datum = datetime64_to_datetime(df_ausgaben[index_datum].values[0]) - relativedelta(years=1)
    torten_datum = st.date_input("Ausgaben seit:", value=torten_datum)
    mask = df_ausgaben[index_datum] > to_datetime(torten_datum)
    df_ausgaben_torte = df_ausgaben.loc[mask]
    pie_chart = create_plotly_pie_chart(df_ausgaben_torte, values='Betrag_absolut', names='kategorie', title='Kategorien')
    st.plotly_chart(pie_chart, theme="streamlit", use_container_width=True)
    summe = df_ausgaben_torte['Betrag_absolut'].sum()
    st.write(f"\n\nIn diesem Zeitraum wurden {summe}€ ausgegeben.")

    st.subheader(f"Top 10 Ausgaben seit {torten_datum}")
    df_top_10_ausgaben = df_ausgaben_torte.sort_values(by = ['Betrag_absolut'], ascending=False).head(10)
    st.dataframe(df_top_10_ausgaben)

with col2:
    st.subheader(f"Einnahmen und Ausgaben")
    frequenzen = {'Wöchentlich': 'W', 'Monatlich': 'M', 'Jährlich': 'Y'}
    frequenz = st.selectbox("Frequenz:", sorted(list(frequenzen.keys())),  index=0)

    transactions_df = transactions_df.set_index(index_datum)
    resampled_transactions_df = resample_transactions(transactions_df, index_datum, frequenzen[frequenz], umsatztypen)

    line_chart_betrag_absolut = aufstellung_bar_chart(resampled_transactions_df[[index_datum, 'Betrag_absolut', 'Umsatztyp']], index_datum, "Betrag_absolut", "Aufstellung")
    st.plotly_chart(line_chart_betrag_absolut, theme="streamlit", use_container_width=True)

    st.subheader("Verteilung der Ausgabenbeträge")
    bins = [5,8,13,21,34,55,89,144,233,377,610,987,1597,2000,2500,5000]
    hist_df = cut_in_bins(df_ausgaben, bins)
    hist_df.index.name = "Betragsspanne"
    plot = bar_chart(hist_df, y_axis="sum", title="Summe aller Betragsspannen")
    st.plotly_chart(plot, theme="streamlit", use_container_width=True)
    quantile_25, quantile_75 = df_ausgaben['Betrag_absolut'].quantile([0.25, 0.75])
    df_50_perc = df_ausgaben[(df_ausgaben['Betrag_absolut'] > quantile_25) & (df_ausgaben['Betrag_absolut'] < quantile_75)]

st.subheader("Saisonale Analyse der Ausgaben")

# 2 Column Layout
col1_saison, col2_saison = st.columns(2)

with col1_saison:
    df_ = group_by_time(df_ausgaben, index_datum, config, 'weekday', agg_freq=None)
    plot = bar_chart(df_, "Betrag_absolut", title="Summe aller Ausgaben nach Wochentag")
    st.plotly_chart(plot, theme="streamlit", use_container_width=True)
with col2_saison:
    df_ = group_by_time(df_ausgaben, index_datum, config, 'month', agg_freq='year')
    plot = bar_chart(df_, "Betrag_absolut", title="Summe aller Ausgaben nach Monat")
    st.plotly_chart(plot, theme="streamlit", use_container_width=True)

st.markdown("***")
st.subheader("Unkategorisierte Ausgaben")

min_date = datetime64_to_datetime(df_ausgaben[index_datum].values[-1])
max_date = datetime64_to_datetime(df_ausgaben[index_datum].values[0])

min_date = st.date_input("von", min_date)
max_date = st.date_input("bis", max_date)
mask = (df_ausgaben[index_datum] > to_datetime(min_date)) & (df_ausgaben[index_datum] <= to_datetime(max_date))

df_ausgaben_unbekannt = df_ausgaben.loc[mask]
df_ausgaben_unbekannt = df_ausgaben_unbekannt[pd.isnull(df_ausgaben['kategorie'])]
st.dataframe(df_ausgaben_unbekannt)
summe = df_ausgaben_unbekannt['Betrag_absolut'].sum()
st.write(f"In diesem Zeitraum wurden {summe}€ ausgegeben.")