"""Description

Librairie permettant de comparer le prix d'une chambre d'hotel de Booking.com à la concurrence.

Exemple : 
    >>> C:\path> python main.py Paris 15 January 2023
    1. Récupère les informations des chambres d'hotels de Paris trouvés sur booking.com pour la nuit du 15 Janvier 2023 pour 2 personnes.
    2. Nettoie les données récoltées avec le fichier preprocessing.py
    3. Entraine les modèles et selectionne le plus performant.
    4. Compare les valeurs prédites aux valeurs réelles de l'hotel choisi par l'utilisateur
"""

import typer
from typing import Tuple, List
from scraping import collect_data
from preprocessing import cleaning
from prediction import training
import pandas as pd
import json

app = typer.Typer()


@app.command()
def ranking(
    destination: str, checkin_date: Tuple[int, str, int], room_to_rank: List[str]
):
    collect_data(destination, checkin_date)
    with open("Booking_Hotels.json", "r") as read_content:
        df = json.load(read_content)
    df = pd.DataFrame(df)
    print(df.head())
    cleaning(df)
    with open("Booking_Hotels_cleaned.json", "r") as read_content:
        df = json.load(read_content)
    df = pd.DataFrame(df)
    print(df.head())
    training(df, room_to_rank)


if __name__ == "__main__":
    app()
