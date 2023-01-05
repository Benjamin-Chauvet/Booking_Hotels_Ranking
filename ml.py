from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC, SVR
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.tree import  DecisionTreeRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.naive_bayes import BernoulliNB
from sklearn.neural_network import MLPClassifier

import pandas as pd
import numpy as np
import json

from rich import print
from rich.table import Table 

with open("???.json", "r") as read_content:
    Booking=json.load(read_content)

list_facilities = []
for i in range(0, len(Booking)):
    for keys, values in Booking["Hotel_facilities"][i].items():
        if keys not in list_facilities:
            list_facilities.append(keys)
            
Booking = Booking.drop(['Room_id', 'Room_name', 'Room_promo', 'Room_breakfast','Room_cancellation', 'Room_prepayment', 'Hotel_id', 'Hotel_Name', 'Hotel_address', 'Hotel_type', 'Hotel_facilities', 'Hotel_categories', 'Hotel_Street', 'Hotel_City', 'Hotel_Country'], axis=1)
for facility in list_facilities:
    Booking = Booking.drop(columns=[f'{facility}'])

y = Booking.Room_price
X = Booking.drop('Room_price', axis=1)

X_tr, X_te, y_tr, y_te = train_test_split(X, y)

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
        "alpha": [2 ** p for p in range(-6, 6)],
        "l1_ratio": (0.01, 0.25, 0.5, 0.75, 1),
    }
)
en_gs_final = en_gs.fit(X_tr, y_tr)

# K Nearest Neighbors
knr = KNeighborsRegressor()
knr_gs = GridSearchCV(
    knr,
    {
        "n_neighbors": (2, 4, 8, 16, 32),
        "weights" : ('uniform', 'distance'),
    }
)
knr_gs_final = knr_gs.fit(X_tr, y_tr)

# Gaussian process Regression  
gpr = GaussianProcessRegressor()
gpr.fit(X_tr, y_tr)

# Random Forest
rfr = RandomForestRegressor()
rfr_gs = GridSearchCV(
    rfr,
    {
        'n_estimators' : (8, 16, 32, 64, 128, 256),        
    }
)
rfr_gs_final = rfr_gs.fit(X_tr, y_tr)

# Support Vector Regression 
svr = SVR()
svr_gs = GridSearchCV(
    svr,
    {
        'C': (0.1, 1.0, 10), #zone de sécurité, pénalisation(cb de membres de chaque famille il peut y avoir à l'extérieur de la bande)
        'epsilon': (0.1, 1.0, 10), #zone de confiance
    }
)
svr_gs_final = svr_gs(X_tr, y_tr)

# Support Vector avec Pipeline
pl = Pipeline(
    [
        ("mise_echelle", MinMaxScaler()),
        ("support_vecteurs", SVR())
    ]
)
pl_gs = GridSearchCV(
    pl,
    {
        'support_vecteurs__C': (0.1, 1.0, 10), #zone de sécurité, pénalisation(cb de membres de chaque famille il peut y avoir à l'extérieur de la bande)
        'support_vecteurs__epsilon': (0.1, 1.0, 10), #zone de confiance
    }
)
pl_gs_final = pl_gs.fit(X_tr, y_tr)

# Multi Layer Perceptron 
pln = Pipeline(
    [
        ("mise_echelle", MinMaxScaler()),
        ("neurones", MLPRegressor())
    ]
)

pln_gs = GridSearchCV(
    pln,
    {
        'neurones__alpha': 10.0 ** -np.arange(1, 7),
        'neurones__hidden_layer_sizes': ((25, ), (50, ), (100,), (20, 20)),
    }
)
pln_gs_final = pln_gs.fit(X_tr, y_tr)

# Réseau de neurones
neurones_gs = GridSearchCV(
    MLPClassifier(),
    {
        'hidden_layer_sizes': [(10,), (50,), (100,), (10, 10,)],
        'activation': ['logistic', 'tanh', 'relu'],
        'alpha': 10.0 ** -np.arange(1, 7)
    } 
    
)
neurones_gs_final = neurones_gs.fit(X_tr, y_tr)

# Bayesian Naif
nb = BernoulliNB()
naive_gs = GridSearchCV(
    nb,
    {
        "alpha": np.linspace(0.01, 1, 10),
    }
)
naive_gs_final = naive_gs.fit(X_tr, y_tr)

#Regression logistique 

log_gs = GridSearchCV(
    LogisticRegression(),
    [
        {
           "penalty" : ['l1', 'elasticnet'],
            "C": [0.1, 0.5, 1.0, 5.0, 10.0],
            "max_iter": [500,],
            "solver": ["saga",],
        },
        {
            "penalty": ["l2"],
            "C": [0.1, 0.5, 1.0, 5.0, 10.0],
            "max_iter": [500,],
        },
        {
            "penalty": ["none"],
        },
    ]
)
log_gs_final = log_gs.fit(X_tr, y_tr)

#Tableau final - A REVOIR AVEC LES X TE ET Y TE

tableau = Table(
    "modèle",
    "score entrainement",
    "score test",
    title = "Synthèse des modèles"
)

modeles = [
    lr_final,
    ls_final,
    ri_final,
    en_gs_final,
    knr_gs_final,
    rfr_gs_final,
    svr_gs_final,
    pl_gs_final,
    pln_gs_final,
    neurones_gs_final,
    naive_gs_final,
    log_gs_final
]

for modele in modeles: 
    tableau.add_row(
        str(modele),
        str(modele.score()),
        str(modele.score(X_te, y_te))
        )
    
print(tableau)