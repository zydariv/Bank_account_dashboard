import pandas as pd
import random
from datetime import datetime
import numpy as np


zahlungsempfaenger_list = ['PayPal', 'Rewe', 'Lidl', 'Bauhaus', 'Sparkasse', 'Hans']
gehalt = 2165
columns = ["Buchungsdatum",
           "Zahlungsempfänger*in",
           "Betrag"]

buchungs_datum = pd.date_range(
                start=pd.to_datetime("1/1/2015").tz_localize("Europe/Berlin"),
                end=pd.to_datetime("1/11/2023").tz_localize("Europe/Berlin"))

df = pd.DataFrame()
df["Buchungsdatum"] = buchungs_datum
df["Wertstellung"] = buchungs_datum
df["Wochentag"] = df["Buchungsdatum"].dt.day_name(locale="de_DE")
df["Monat"] = df["Buchungsdatum"].dt.month_name(locale="de_DE")

def create_random_betrag():
    offset = random.randint(0,30)
    offset2 = random.randint(0,40)
    betrag = random.randrange(offset, 300-offset2)

    return round(-1 * betrag, 2)

betraege = []
for i in range(len(df)):
    betraege.append(create_random_betrag())
betraege = np.asarray(betraege)
frac = 0.25
mask = sample = np.random.binomial(1, frac, size=len(df))
df['Betrag'] = np.multiply(mask, betraege)


mask_indices = np.where(mask == 1)[0]
random_zahlungsempfaenger = [random.choice(zahlungsempfaenger_list) for x in range(len(df))]
df.loc[mask_indices, 'Zahlungsempfänger*in'] = [random_zahlungsempfaenger[i] for i in mask_indices]

df.loc[df['Buchungsdatum'].dt.is_month_end == True, 'Betrag'] = gehalt
df.loc[df['Buchungsdatum'].dt.is_month_end == True, 'Zahlungsempfänger*in'] = 'Max Mustermann'
df = df.dropna()
df['Betrag'] = df['Betrag'].astype(str)
df['Betrag'] = df['Betrag'].map(lambda x: f"{x}\xa0€".replace('.', ','))
df.drop(columns=['Wochentag', 'Monat'], inplace=True)
df['Buchungsdatum'] = df['Buchungsdatum'].dt.strftime("%d.%m.%Y").astype(str)
df['Wertstellung'] = df['Wertstellung'].dt.strftime("%d.%m.%Y").astype(str)
df = df[::-1]
df.to_csv('Transactions/artificial_max_mustermann.csv', sep=';', index=False)
print(df)