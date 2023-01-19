"""Description

Librairie d'interface en ligne de commande permettant de comparer le prix de chambres d'hotels Booking à la concurrence.

    1. Récupère les informations des chambres d'hotels de la destination et de la date sélectionnée (`scraping.py`).
    2. Nettoie les données récoltées sous format json (`preprocessing.py`).
    3. Entraine le prédicteur sur différents modèles, séléctionne le plus performant et compare les valeurs prédites
    par ce modèle aux valeurs réelles sur les différentes chambres choisies par l'utilisateur (`prediction.py`).

Exemple : 
    >>> C:\path> python main.py ranking Paris 15 January 2023 112030409_91947049_0_2_0
    - Récolte les données des chambres d'hotels de Paris trouvées sur booking.com pour la nuit du 15 Janvier 2023 pour 2 personnes.
    - Nettoie le dataset pour le machine learning.
    - Entraine et sélectionne le meilleur modèle et compare le prix prédit au prix affiché (sur Booking) de la chambre d'id "112030409_91947049_0_2_0".
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
