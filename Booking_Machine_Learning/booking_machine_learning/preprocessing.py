"""Description

Librairie de nettoyage des données json brutes sortant un fichier json exploitable pour le machine learning.
"""


import json
import pandas as pd

with open("Booking_Hotels.json", "r") as read_content:
    df=json.load(read_content)

df = pd.DataFrame(df)

def price():
    """Modifie la variable Room_price en enlevant le signe €, la virgule entre les milliers et les espaces.
    """
    df['Room_price'] = (
        df['Room_price']
        .str.replace('€', '')
        .str.replace(',', '')
        .str.strip()
    )
 
def address():
    """Créé 4 nouvelles variables (street, arr, city, country) grâce à la variable Hotel_adress.
    """
    df['Hotel_Street'] = ''
    df['Hotel_City'] = ''
    df['Hotel_Country'] = ''
    for i in range(0, len(df)):
        virgule_split = df['Hotel_address'][i].split(',')
        df['Hotel_Street'][i] = virgule_split[0]
        df['Hotel_City'][i] = virgule_split[1:-1]
        df['Hotel_Country'][i] = virgule_split[-1]

def reviews():
    """Modifie la variable Hotel_nb_reviews.
    """        
    df['Hotel_nb_reviews'] = df['Hotel_nb_reviews'].str.replace(',', '').str.strip()
    for i in range(0, len(df)):
        df['Hotel_nb_reviews'][i] = df['Hotel_nb_reviews'][i][3:-8]
    df['Hotel_nb_reviews'] = df['Hotel_nb_reviews'].replace('', 0)

def grade():
    """Modifie la variable Hotel_grade.
    """  
    df['Hotel_grade'] = df['Hotel_grade'].replace('', 0.0)

def facilities():
    """Créer une nouvelle variable pour chaque facilities se trouvant dans Hotel_facilities.
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

    list_mots = ['Lift', 'Luggage storage', 'No parking available.']
    for mot in list_mots:
        df[f'{mot}_bin'] = 0
        for i in range(0, len(df)):
            for facility in list_facilities:
                if mot in df[facility][i]:
                    df[f'{mot}_bin'][i] = 1
                    break
    
def categories():
    """Créer une nouvelle variable pour chaque categories se trouvant dans Hotel_categories.
    """
    list_categories = []
    for i in range(0, len(df)):
        for keys, values in df['Hotel_categories'][i].items():
            if keys not in list_categories:
                list_categories.append(keys)

    for i in range(0, len(df)):
        for category in list_categories:
            if category not in df['Hotel_categories'][i]:
                df['Hotel_categories'][i][f'{category}'] = ''

    for category in list_categories:
        df[f'{category}'] = 0.0
        for i in range(0, len(df)):
            if type(df['Hotel_categories'][i][f'{category}']) == list:
                df[f'{category}'][i] = float(df['Hotel_categories'][i][f'{category}'][0])
        df[f'{category}'] = df[f'{category}'].replace(0.0, None)

def promo_bin():
    """Créer une nouvelle variable binaire à partir de Room_promo, valant 1 si promotion et 0 sinon.
    """
    df['Room_promo_bin'] = 0
    for i in range(0, len(df)):
        if df['Room_promo'][i] != '':
            df['Room_promo_bin'][i] = 1

def cancellation():
    """Modifie la présentation de la variable Room_cancellation
    """
    for i in range(0, len(df)):
        if df['Room_cancellation'][i][0:2] == "•\n":
            df['Room_cancellation'][i] = df['Room_cancellation'][i].replace('•\n', '')
    for i in range(0, len(df)):
        if 'Free cancellation' in df['Room_cancellation'][i]:
            df['Room_cancellation'][i] = "Free cancellation"

def cancellation_bin():
    """Créé une variable binaire à partir de Room_cancellation valant 1 si l'annulation est gratuite, 0 sinon.
    """
    df['Room_cancellation_bin'] = 0
    for i in range(0, len (df)):
        if df['Room_cancellation'][i] == "Free cancellation":
            df['Room_cancellation_bin'][i] = 1

def prepayment_bin():
    """Créé une variable binaire à partir de Room_prepayment valant 1 si un prépaiment est possible, 0 sinon.
    """
    for i in range(0, len(df)):
        if df['Room_prepayment'][i][0:2] == "•\n":
            df['Room_prepayment'][i] = df['Room_prepayment'][i].replace('•\n', '')
    df['Room_prepayment_bin'] = 1
    for i in range(0, len(df)):
        if df['Room_prepayment'][i] == 'NO PREPAYMENT NEEDED – pay at the property':
            df['Room_prepayment_bin'][i] = 0
            
def breakfast():
    """Modidife la présentation de Room_breakfast.
    """
    df['Room_breakfast'] = df['Room_breakfast'].str.replace('Breakfast', 'breakfast')
    for i in range(0, len(df)):
        if 'breakfast' not in df['Room_breakfast'][i]:
            df['Room_breakfast'][i] = ""

def breakfast_bin():
    """Créé une variable binaire à partir de Room_breakfast, valant 1 si le petit déjeuner et inclu, 0 sinon.
    """
    df['Room_breakfast_bin'] = 0
    for i in range(0, len(df)):
        if 'included' in df['Room_breakfast'][i]:
            df['Room_breakfast_bin'][i] = 1
            
def breakfast_price():
    """Crée une variable à partir de Room_breakfast, qui affiche le prix du petit déjeuner s'il n'est pas inclu.
    """
    df["Room_breakfast_price"] = 0
    for i in range(0, len(df)):
        if '€' in df['Room_breakfast'][i]:
            df["Room_breakfast_price"][i] = df['Room_breakfast'][i].split('€')[-1].strip()
            if '(optional)' in df["Room_breakfast_price"][i]:
                df["Room_breakfast_price"][i] = df["Room_breakfast_price"][i].split(" ")[0]

def size():
    """"Modifie la présentation de la variable Room_size.
    """
    df['Room_size'] = (
        df['Room_size']
        .str.replace(':', '')
        .str.strip()
        )
    for i in range(0, len(df)):
        if len(df['Room_size'][i]) > 3 or df['Room_size'][i] == '':
                df['Room_size'][i] = 0

def type_converter():
    """Modifie le type des variables et attribue les valeurs manquantes.
    """
    df['Room_price'] = df['Room_price'].astype(int)
    df['Hotel_nb_reviews'] = df['Hotel_nb_reviews'].astype(int)
    df['Room_sleeps'] = df['Room_sleeps'].astype(int)
    df['Room_size'] = df['Room_size'].astype(int)
    df['Room_size'] = df['Room_size'].replace(0, None)
    df['Hotel_grade'] = df['Hotel_grade'].astype(float)
    df['Hotel_grade'] = df['Hotel_grade'].replace(0.0, None)
    df["Room_breakfast_price"] = df["Room_breakfast_price"].astype(float)

def ml_file():
    """Retire lignes ayant des valeurs manquantes et sélectionne les chambres d'hotels.
    """
    df_ml = df.dropna(axis=0)
    i = df[(df.Hotel_type != 'Hotel')].index
    df_ml = df_ml.drop(i)
    print(df)
    df.to_csv('Booking_Hotels.csv', index=False)

    json_data = df_ml.to_json()
    with open('Booking_Hotels_clean.json', 'w') as file:
        file.write(json_data)

price()
address()
reviews()
grade()
facilities()
categories()
promo_bin()
cancellation()
cancellation_bin()
prepayment_bin()
breakfast()
breakfast_bin()
breakfast_price()
size()
type_converter()
ml_file()

    
