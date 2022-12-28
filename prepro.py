"""Nettoyage des données pour pouvoir les utiliser en machine learning
"""

import json
import pandas as pd
from dataclasses import dataclass
from serde import serde
from serde.json import from_json, to_json
from typing import List

with open("stockage.json", "r") as read_content:
    df=json.load(read_content)

df = pd.DataFrame(df)


def price():
    """Nettoie la variable Room_price en enlevant le signe € et la virgule
    """
    df['Room_price_new'] = df['Room_price'].str.replace('€', '').str.replace(',', '')

def adress():
    """Créé 4 nouvelles variables (street, arr, city, country) grâce à la variable Hotel_adress
    """
    for i in range(0, len(df)):
        virgule_count = df['Hotel_address'][i].count(',')
        if virgule_count != 3:
            df['Hotel_address'][i] = df['Hotel_address'][i].replace(',', '', 1)
    for i in range(0, len(df)):
        street, arr, city, country = df['Hotel_address'][i].split(',')
        df['Hotel_Street'] = street
        df['Hotel_Arr'] = arr
        df['Hotel_City'] = city
        df['Hotel_Country'] = country
        #A voir : si pas Paris pas d'arr
        
def reviews():
    for i in range(0, len(df)):
        df['Hotel_nb_reviews_new'] = df['Hotel_nb_reviews'].str.replace(',','')
        #df['Hotel_nb_reviews_new'][i] = df['Hotel_nb_reviews_new'][i][3:-8]
    
