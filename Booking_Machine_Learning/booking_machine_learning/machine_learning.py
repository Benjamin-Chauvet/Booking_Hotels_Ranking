"""Description

Librairie de machine learning permettant de trouver le modèle le plus adéquat à exprimer le prix d'une chambre d'hotel en fonction des caractéristiques de celle-ci.
"""


from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.naive_bayes import BernoulliNB

import pandas as pd
import numpy as np
import json

from rich import print
from rich.table import Table 

with open("Booking_Hotels_Paris_cleaned.json", "r") as read_content:
    Paris=json.load(read_content)
    
Paris = pd.DataFrame(Paris)    
Paris_updated = Paris.dropna(axis=0)

i = Paris_updated[(Paris_updated.Hotel_type != 'Hotel')].index
Paris_updated = Paris_updated.drop(i)

list_facilities = []
for i in range(0, len(Paris_updated)):
    for keys, values in Paris_updated["Hotel_facilities"][i].items():
        if keys not in list_facilities:
            list_facilities.append(keys)
            
Paris_updated = Paris_updated.drop(['Room_id', 'Room_name', 'Room_promo', 'Room_breakfast','Room_cancellation', 'Room_prepayment', 'Hotel_id', 'Hotel_Name', 'Hotel_address', 'Hotel_type', 'Hotel_facilities', 'Hotel_categories', 'Hotel_Street', 'Hotel_City', 'Hotel_Country'], axis=1)
for facility in list_facilities:
    Paris_updated = Paris_updated.drop(columns=[f'{facility}'])

y = Paris_updated.Room_price
X = Paris_updated.drop('Room_price', axis=1)

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
gpr_final = gpr.fit(X_tr, y_tr)

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
pl = Pipeline(
    [
        ("mise_echelle", MinMaxScaler()),
        ("support_vecteurs", SVR())
    ]
)
pl_gs = GridSearchCV(
    pl,
    {
        'support_vecteurs__C': (0.1, 1.0, 10), 
        'support_vecteurs__epsilon': (0.1, 1.0, 10), 
    }
)
svr_gs_final = pl_gs.fit(X_tr, y_tr)

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
mlp_gs_final = pln_gs.fit(X_tr, y_tr)

# Réseau de neurones
# pln = Pipeline(
#     [
#         ("mise_echelle", MinMaxScaler()),
#         ("neurones", MLPRegressor()),
#     ]
# )
# neurones_gs = GridSearchCV(
#     #MLPClassifier(),
#     pln,
#     {
#         'hidden_layer_sizes': [(10,), (50,), (100,), (10, 10,)],
#         'activation': ['logistic', 'tanh', 'relu'],
#         'alpha': 10.0 ** -np.arange(1, 7)
#     } 
    
# )
# neurones_gs_final = neurones_gs.fit(X_tr, y_tr)

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
            "max_iter": [100,],
            "solver": ["saga",],
        },
        {
            "penalty": ["l2"],
            "C": [0.1, 0.5, 1.0, 5.0, 10.0],
            "max_iter": [100,],
        },
        {
            "penalty": ["none"],
        },
    ]
)
log_gs_final = log_gs.fit(X_tr, y_tr)

tableau = Table(
    "Modèle",
    'Train score', 
    'Test score',
    'Cross-validation \nscore',
    'Cross-validation \ndispersion',
    title = "Synthèse des modèles"
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
    log_gs_final
]

for model in models:
    if 'GridSearchCV' in str(model):
        model_name = str(model.estimator)
        if 'Pipeline' in str(model):
            model_name = str(model.estimator[1])
    else:
        model_name = str(model)
    cv_scores = cross_val_score(model, X_tr, y_tr, cv = 5)
    tableau.add_row(
        str(model_name),
        str(model.score(X_tr, y_tr)),
        str(model.score(X_te, y_te)),
        str(cv_scores.mean()),
        str(cv_scores.std()))
print(tableau)