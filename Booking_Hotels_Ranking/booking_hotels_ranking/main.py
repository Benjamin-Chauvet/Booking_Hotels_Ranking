"""Description

Application permettant de comparer le prix d'une chambre d'hotel à la concurrence.

Exemple : 
    >>> C:\path> python main.py Paris 15 January 2023
    1. Récupère les informations des chambres d'hotels de Paris trouvés sur booking.com pour la nuit du 15 Janvier 2023 pour 2 personnes.
    2. Nettoie les données récoltées avec le fichier preprocessing.py
    3. Entraine les modèles et selectionne le plus performant.
    4. Compare les valeurs prédites aux valeurs réelles de l'hotel choisi par l'utilisateur
"""

import typer
from typing import Tuple

# from scraping import collect_data

# from preprocessing import (
#     price,
#     address,
#     reviews,
#     grade,
#     facilities,
#     categories,
#     promo_bin,
#     cancellation,
#     cancellation_bin,
#     prepayment_bin,
#     breakfast,
#     breakfast_bin,
#     breakfast_price,
#     size,
#     type_converter,
#     ml_file,
# )
# from preprocessing import cleaning, type_converter, ml_file
from prediction import training
import pandas as pd
import json

app = typer.Typer()


# @app.command()
# def scraping(
#     destination: str,
#     checkin_date: Tuple[int, str, int],
# ):
#     collect_data(destination, checkin_date)
#     with open("Booking_Hotels.json", "r") as read_content:
#         df = json.load(read_content)
#     df = pd.DataFrame(df)
#     print(df.head())
#     # price(df)
#     # address(df)
#     # reviews(df)
#     # grade(df)
#     # facilities(df)
#     # categories(df)
#     # promo_bin(df)
#     # cancellation(df)
#     # cancellation_bin(df)
#     # prepayment_bin(df)
#     # breakfast(df)
#     # breakfast_bin(df)
#     # breakfast_price(df)
#     # size(df)
#     cleaning(df)
#     type_converter(df)
#     ml_file(df)
#     with open("Booking_Hotels_cleaned.json", "r") as read_content:
#         df = json.load(read_content)
#     df = pd.DataFrame(df)
#     print(df.head())
#     # training(df)


@app.command()
def prediction(room_test: str):
    with open("Booking_Hotels_Paris_cleaned.json", "r") as read_content:
        df = json.load(read_content)
    df = pd.DataFrame(df)
    training(df, room_test)
    # compare(, room_test: str)


if __name__ == "__main__":
    app()
