"""Nettoyage des données pour pouvoir les utiliser en machine learning
"""

import json
import pandas as pd
from dataclasses import dataclass
from serde import serde
from serde.json import from_json, to_json
from typing import List
import re

with open("hotels_Paris_75.json", "r") as read_content:
    df=json.load(read_content)

df = pd.DataFrame(df)

def price():
    """Modifie la variable Room_price en enlevant le signe € et la virgule
    """
    df['Room_price'] = df['Room_price'].str.replace('€', '').str.replace(',', '')

def address():
    """Créé 4 nouvelles variables (street, arr, city, country) grâce à la variable Hotel_adress
    """
    for i in range(0, len(df)):
        virgule_count = df['Hotel_address'][i].count(',')
        if virgule_count != 3:
            df['Hotel_address'][i] = df['Hotel_address'][i].replace(',', '', virgule_count-3)
    for i in range(0, len(df)):
        street, arr, city, country = df['Hotel_address'][i].split(',')
        df['Hotel_Street'] = street
        df['Hotel_Arr'] = arr
        df['Hotel_City'] = city
        df['Hotel_Country'] = country
        #A voir : si pas Paris pas d'arr

def reviews():
    """Modifie la variable Hotel_nb_reviews
    """        
    df['Hotel_nb_reviews'] = df['Hotel_nb_reviews'].str.replace(',','')
    for i in range(0, len(df)):
        df['Hotel_nb_reviews'][i] = df['Hotel_nb_reviews'][i][3:-8]

def facilities():
    """Créer une nouvelle variable pour chaque facilities se trouvant dans Hotel_facilities
    """
    list_facilities = []
    for i in range(0, len(df)):
        for keys, values in df["Hotel_facilities"][i].items():
            if keys not in list_facilities:
                list_facilities.append(keys)
    
    for i in range(0, len(df)):
        for facility in list_facilities:
            if facility not in df['Hotel_facilities'][i]:
                df['Hotel_facilities'][i][f'{facility}'] = ''
    
    for i in range(0, len(df)):
        for facility in list_facilities:
            if i == 0:
                df[facility] = ''
            df[facility][i] = df['Hotel_facilities'][i].get(f'{facility}')
    
def categories():
    """Créer une nouvelle variable pour chaque categories se trouvant dans Hotel_categories
    """
    list_category = []
    for i in range(0, len(df)):
        for keys, values in df['Hotel_categories'][i].items():
            if keys not in list_category:
                list_category.append(keys)
    
    for i in range(0, len(df)):
        for category in list_category:
            if category not in df['Hotel_facilities'][i]:
                df['Hotel_facilities'][i][f'{category}'] = ''
        
    for i in range(0, len(df)):
        for category in list_category:
            if i == 0:
                df[category] = ''
            df[category][i] = df['Hotel_categories'][i].get(f'{category}')
            
def promo():
    """Modifie la variable Room_promo pour ne garder que le montant
    """
    motif = re.compile('([1-9][0-9]*)')
    groupes = df.Room_promo.str.extract(motif)
    for i in range(0, len(df)):
        if df['Room_promo'][i] != None:
            df['Room_promo'][i] = groupes[0][i]
        else:
            df['Room_promo'] == 0

def promo_bin():
    """Créer une nouvelle variable binaire à partir de Room_promo, valant 1 si promotion et 0 sinon
    """
    for i in range(0, len(df)):
        if df['Room_promo'][i] != None:
            df['Room_promo_bin'] = 1
        else:
            df['Room_promo_bin'] = 0
        
        
price()
address()
reviews()
facilities()
categories()
promo()
print(df)

#code_json = to_json(room_list)
#with open('stockage.json', 'w') as fichier:
    #fichier.write(code_json)
    
