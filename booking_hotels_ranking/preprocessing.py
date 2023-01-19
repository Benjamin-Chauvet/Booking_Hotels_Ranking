"""Description

Librairie de nettoyage des données json brutes sortant un fichier json exploitable pour le machine learning.
"""

import json
import pandas as pd
import numpy as np
from janitor import deconcatenate_column

with open("Booking_Hotels.json", "r") as read_content:
    df = json.load(read_content)

df = pd.DataFrame(df)


def price(df):
    """
    Modifie la variable `Room_price` en enlevant le signe €, la virgule entre les milliers et les espaces.
    """
    df["Room_price"] = (
        df["Room_price"].str.replace("€", "").str.replace(",", "").str.strip()
    )
    return df


def address(df):
    """
    Modifie la variable `Hotel_address`.
    """

    def adress_mod(x):
        virgule = x.count(",")
        if virgule != 3:
            x = x.replace(",", "", 1)
        return x

    df["Hotel_address"] = list(map(adress_mod, df["Hotel_address"]))
    df = df.deconcatenate_column(
        "Hotel_address",
        sep=",",
        new_column_names=["Hotel_street", "Hotel_arr", "Hotel_city", "Hotel_country"],
    )
    return df


def reviews(df):
    """
    Modifie la variable `Hotel_nb_reviews`.
    """
    df["Hotel_nb_reviews"] = (
        df["Hotel_nb_reviews"]
        .str.replace(",", "")
        .str.replace("·", "")
        .str.replace("reviews", "")
        .str.strip()
        .replace("", np.nan)
    )
    return df


def grade(df):
    """
    Modifie la variable `Hotel_grade` en retirant les valeurs manquantes.
    """
    df["Hotel_grade"] = df["Hotel_grade"].replace("", np.nan)
    return df


def facilities(df):
    """
    Crée une nouvelle variable pour chaque facilities se trouvant dans `Hotel_facilities`.
    """
    list_facilities = []
    for i in range(0, len(df)):
        for keys, values in df["Hotel_facilities"][i].items():
            if keys not in list_facilities:
                list_facilities.append(keys)

    for i in range(0, len(df)):
        for facility in list_facilities:
            if facility not in df["Hotel_facilities"][i]:
                df["Hotel_facilities"][i][f"{facility}"] = ""

    for i in range(0, len(df)):
        for facility in list_facilities:
            if i == 0:
                df[facility] = ""
            df[facility][i] = df["Hotel_facilities"][i].get(f"{facility}")

    list_mots = ["Lift", "Luggage storage", "No parking available."]
    for mot in list_mots:
        df[f"{mot}_bin"] = 0
        for i in range(0, len(df)):
            for facility in list_facilities:
                if mot in df[facility][i]:
                    df[f"{mot}_bin"][i] = 1
                    break
    return df


def categories(df):
    """
    Crée une nouvelle variable pour chaque categories se trouvant dans `Hotel_categories`.
    """
    list_categories = []
    for i in range(0, len(df)):
        for keys, values in df["Hotel_categories"][i].items():
            if keys not in list_categories:
                list_categories.append(keys)

    for i in range(0, len(df)):
        for category in list_categories:
            if category not in df["Hotel_categories"][i]:
                df["Hotel_categories"][i][f"{category}"] = ""

    for category in list_categories:
        df[f"{category}"] = np.nan
        for i in range(0, len(df)):
            if type(df["Hotel_categories"][i][f"{category}"]) == list:
                df[f"{category}"][i] = float(
                    df["Hotel_categories"][i][f"{category}"][0]
                )
        # df[f"{category}"] = df[f"{category}"].replace(0.0, np.nan)
    return df


def promo_bin(df):
    """
    Crée une variable binaire à partir de `Room_promo` qui indique si la chambre est soumise à une réduction.
    """
    df = df.case_when(
        df["Room_promo"] == "",
        0,
        df["Room_promo"] != "",
        1,
        column_name="Room_promo_bin",
    )
    return df


def cancellation(df):
    """
    Modifie la présentation de la variable `Room_cancellation` et crée `Room_cancellation_bin` qui vaut 1 s'il est possible d'annuler gratuitement.
    """

    def cancellation_mod(x):
        x = x.replace("•\n", "")
        if "Free cancellation" in x:
            x = "Free cancellation"
        return x

    df["Room_cancellation"] = list(map(cancellation_mod, df["Room_cancellation"]))
    df = df.case_when(
        df["Room_cancellation"].str.contains("Free cancellation"),
        1,
        0,
        column_name="Room_cancellation_bin",
    )
    return df


def prepayment_bin(df):
    """
    Crée une variable binaire à partir de `Room_prepayment` indiquant s'il y a besoin de prépayer la chambre.
    """
    df = df.case_when(
        df["Room_prepayment"].str.contains("NO PREPAYMENT NEEDED"),
        0,
        1,
        column_name="Room_prepayment_bin",
    )
    return df


def breakfast(df):
    """
    Modifie la présentation de `Room_breakfast`, crée une variable binaire indiquant si le petit déjeuner est inclut
    et crée une variable sur le prix du petit déjeuner.
    """

    def breakfast_mod(x):
        if "breakfast" not in x:
            x = ""
        return x

    df["Room_breakfast"] = (
        df["Room_breakfast"]
        .str.replace("Breakfast", "breakfast")
        .map(lambda x: breakfast_mod(x))
    )

    df = df.case_when(
        df["Room_breakfast"].str.contains("included"),
        1,
        0,
        column_name="Room_breakfast_bin",
    )

    df = df.case_when(
        df["Room_breakfast"].str.contains("€"),
        df["Room_breakfast"].str.split("€"),
        0.0,
        column_name="Room_breakfast_price",
    )

    def breakfast_price_mod(x):
        if x != 0.0:
            x = x[1]
            if "(optional)" in x:
                x = x.split(" ")[1]
            x = x.strip()
        return x

    df["Room_breakfast_price"] = df["Room_breakfast_price"].map(
        lambda x: breakfast_price_mod(x)
    )
    return df


def size(df):
    """
    Modifie la variable `Room_size` et retire les valeurs aberrantes.
    """

    def size_mod(x):
        if len(x) > 3 or x == "":
            x = np.nan
        return x

    df["Room_size"] = (
        df["Room_size"].str.replace(":", "").str.strip().map(lambda x: size_mod(x))
    )
    return df


def type_converter(df):
    """
    Retire les lignes ayant des valeurs manquantes et convertie le type des variables
    """
    df = df.dropna(axis=0)
    df["Room_price"] = df["Room_price"].astype(int)
    df["Hotel_nb_reviews"] = df["Hotel_nb_reviews"].astype(int)
    df["Room_sleeps"] = df["Room_sleeps"].astype(int)
    df["Room_size"] = df["Room_size"].astype(int)
    df["Hotel_grade"] = df["Hotel_grade"].astype(float)
    df["Room_breakfast_price"] = df["Room_breakfast_price"].astype(float)
    return df


def ml_file(df):
    """
    Sélectionne les chambres d'hotels uniquement et écrit le fichier json prêt pour le machine learning.
    """
    i = df[(df.Hotel_type != "Hotel")].index
    df_ml = df.drop(i)
    print(df)
    json_data = df_ml.to_json()
    with open("Booking_Hotels_cleaned.json", "w") as file:
        file.write(json_data)


def cleaning(df):
    df = price(df)
    df = address(df)
    df = reviews(df)
    df = grade(df)
    df = facilities(df)
    df = categories(df)
    df = promo_bin(df)
    df = cancellation(df)
    df = prepayment_bin(df)
    df = breakfast(df)
    df = size(df)
    df = type_converter(df)
    df = ml_file(df)
    return df
