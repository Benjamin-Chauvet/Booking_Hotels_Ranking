"""Description

Librairie de machine learning permettant de trouver le modèle le plus adéquat à exprimer le prix d'une chambre d'hotel en fonction des caractéristiques de celle-ci.
"""


from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVR
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    AdaBoostRegressor,
)
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.naive_bayes import BernoulliNB
from xgboost import XGBRegressor
import pandas as pd
import numpy as np
import json
from rich import print
from rich.table import Table


def training(df, room_to_rank):
    """Entraine le prédicteur sur différents modèles, séléctionne le plus performant et compare les valeurs prédites
    par ce modèle aux valeurs réelles sur les différentes chambres choisies par l'utilisateur."""
    list_facilities = []
    for i in range(0, len(df)):
        for keys, values in df["Hotel_facilities"][i].items():
            if keys not in list_facilities:
                list_facilities.append(keys)

    for facility in list_facilities:
        df = df.drop(columns=[f"{facility}"])

    y = df["Room_price"]
    X = df[
        [
            "Room_sleeps",
            "Room_size",
            "Hotel_grade",
            "Hotel_nb_reviews",
            "Hotel_stars",
            "Lift_bin",
            "Luggage storage_bin",
            "No parking available._bin",
            "Staff",
            "Facilities",
            "Cleanliness",
            "Comfort",
            "Value for money",
            "Location",
            "Free WiFi",
            "Room_promo_bin",
            "Room_cancellation_bin",
            "Room_prepayment_bin",
            "Room_breakfast_bin",
            "Room_breakfast_price",
        ]
    ]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, random_state=85)

    # Regression linéaire

    lr = LinearRegression()
    lr_final = lr.fit(X_tr, y_tr)

    # Lasso

    ls = Lasso()
    ls_final = ls.fit(X_tr, y_tr)

    # Ridge

    ri = Ridge()
    ri_final = ri.fit(X_tr, y_tr)

    # Elastic Net

    en = ElasticNet()
    en_gs = GridSearchCV(
        en,
        {
            "alpha": [2**p for p in range(-6, 6)],
            "l1_ratio": (0.01, 0.25, 0.5, 0.75, 1),
        },
    )
    en_gs_final = en_gs.fit(X_tr, y_tr)

    # K Nearest Neighbors

    knr = KNeighborsRegressor()
    knr_gs = GridSearchCV(
        knr,
        {
            "n_neighbors": (2, 4, 8, 16, 32),
            "weights": ("uniform", "distance"),
        },
    )
    knr_gs_final = knr_gs.fit(X_tr, y_tr)

    # Gaussian process Regression

    gpr = GaussianProcessRegressor()
    gpr_final = gpr.fit(X_tr, y_tr)

    # Random Forest

    rfr = RandomForestRegressor()
    rfr_gs = GridSearchCV(
        rfr,
        {
            "n_estimators": (16, 32, 64, 128, 256),
            "max_depth": (1, 10, 50, 100, None),
            "min_samples_leaf": (1, 2, 5, 10),
            "max_features": ["auto", "sqrt", "log2"],
        },
    )
    rfr_gs_final = rfr_gs.fit(X_tr, y_tr)

    # Support Vector Regression

    pl = Pipeline([("mise_echelle", MinMaxScaler()), ("support_vecteurs", SVR())])
    pl_gs = GridSearchCV(
        pl,
        {
            "support_vecteurs__C": (0.1, 1.0, 10),
            "support_vecteurs__epsilon": (0.1, 1.0, 10),
        },
    )
    svr_gs_final = pl_gs.fit(X_tr, y_tr)

    # Multi Layer Perceptron

    pln = Pipeline([("mise_echelle", MinMaxScaler()), ("neurones", MLPRegressor())])

    pln_gs = GridSearchCV(
        pln,
        {
            "neurones__alpha": 10.0 ** -np.arange(1, 7),
            "neurones__hidden_layer_sizes": ((25,), (50,), (100,), (20, 20)),
        },
    )
    mlp_gs_final = pln_gs.fit(X_tr, y_tr)

    # Bayesian Naif

    nb = BernoulliNB()
    naive_gs = GridSearchCV(
        nb,
        {
            "alpha": np.linspace(0.01, 1, 10),
        },
    )
    naive_gs_final = naive_gs.fit(X_tr, y_tr)

    # Regression logistique

    log_gs = GridSearchCV(
        LogisticRegression(),
        [
            {
                "penalty": ["l1", "elasticnet"],
                "C": [0.1, 0.5, 1.0, 5.0, 10.0],
                "max_iter": [
                    100,
                ],
                "solver": [
                    "saga",
                ],
            },
            {
                "penalty": ["l2"],
                "C": [0.1, 0.5, 1.0, 5.0, 10.0],
                "max_iter": [
                    100,
                ],
            },
            {
                "penalty": ["none"],
            },
        ],
    )
    log_gs_final = log_gs.fit(X_tr, y_tr)

    # XGBoost

    gs_boost = GridSearchCV(
        XGBRegressor(),
        {
            "nthread": [4],
            "objective": ["reg:linear"],
            "learning_rate": [0.03, 0.05, 0.07],
            "max_depth": [5, 6, 7],
            "min_child_weight": [4],
            "silent": [1],
            "subsample": [0.7],
            "colsample_bytree": [0.7],
            "n_estimators": [500],
        },
    )

    xgb_gs_final = gs_boost.fit(X_tr, y_tr)

    # Gradient boosting regressor

    gb_gs = GridSearchCV(
        GradientBoostingRegressor(),
        {
            "n_estimators": [50, 100, 500],
            "learning_rate": [0.01, 0.1, 1.0],
            "subsample": [0.5, 0.7, 1.0],
            "max_depth": [3, 7, 9],
        },
    )
    gb_gs_final = gb_gs.fit(X_tr, y_tr)

    # Adaboost

    adb_gs = GridSearchCV(
        AdaBoostRegressor(),
        {"learning_rate": [0.01, 0.1, 1.0], "n_estimators": [50, 100, 150, 200]},
    )

    adb_gs_final = adb_gs.fit(X_tr, y_tr)

    # Overview

    overview = Table(
        "Model",
        "Train score",
        "Mean CV score",
        "Dispersion CV score",
        "Best score",
        "Best params",
        title="Synthèse des modèles",
    )

    models = [
        lr_final,
        ls_final,
        ri_final,
        en_gs_final,
        knr_gs_final,
        gpr_final,
        rfr_gs_final,
        svr_gs_final,
        mlp_gs_final,
        naive_gs_final,
        log_gs_final,
        xgb_gs_final,
        gb_gs_final,
        adb_gs_final,
    ]

    for model in models:
        if "GridSearchCV" in str(model):
            model_name = str(model.estimator)
            best_score = model.best_score_
            best_params = model.best_params_
            if "Pipeline" in str(model):
                model_name = str(model.estimator[1])
        else:
            model_name = str(model)
            best_score = "/"
            best_params = "/"

        cv_scores = cross_val_score(model, X_tr, y_tr, cv=5)
        overview.add_row(
            str(model_name),
            str(model.score(X_tr, y_tr)),
            str(cv_scores.mean()),
            str(cv_scores.std()),
            str(best_score),
            str(best_params),
        )
    print(overview)

    value = 0
    for row in range(0, overview.row_count):
        value = overview.columns[1]._cells
        if value[row] > value[row - 1]:
            value = value[row]
            best_row = row
    best_model = models[best_row]

    y_true, y_pred = y_te, best_model.predict(X_te)

    true = np.array(y_true)
    pred = np.array(y_pred)
    pred = np.around(pred, decimals=1)

    ranking = Table(
        "Réalité",
        "Prédiction",
        "Ecart",
        title="Résulat de la prédiction",
        show_header=True,
    )
    for id in room_to_rank:
        x = df.index[df["Room_id"] == id].astype(int)
        for i in x:
            ranking.add_row(
                f"{id}",
                f"{true[i]} €",
                f"{pred[i]:.1f} €",
                f"{((pred[i] - true[i]) / true[i]) * 100:.2f} %",
            )
    print(ranking, f"Accuracy: {rfr_gs_final.score(X_te, y_te)*100:.2f}%")
