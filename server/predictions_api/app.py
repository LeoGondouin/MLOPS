from sklearn.datasets import load_iris

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from fastapi import FastAPI
import seaborn as sns
import pickle as pkl
import joblib

import pandas as pd

app = FastAPI()

@app.get("/predict/iris")
def predictIris(sepal_length,sepal_width,petal_length,petal_width,model_name):
    dict_model = {
                    "Decision Tree Classifier":"./models/iris_dtc.pkl",
                    "Random Forest":"./models/iris_rfc.pkl",
                    "SVC":"./models/iris_svc.pkl",
                }
    iris = load_iris()
    X, y = iris.data, iris.target    
    
    with open(dict_model[model_name], 'rb') as file:
        model = pkl.load(file)

    
    predicted_test = model.predict(X)
    accuracy = accuracy_score(y,predicted_test)

    prediction = model.predict([[sepal_length,sepal_width,petal_length,petal_width]])[0]
    prediction = iris.target_names[prediction]

    return f"Model accuracy : {accuracy}",f"Predicted specie : {prediction}"

@app.get("/predict/penguins")
def predictPenguins(island,bill_length,bill_depth,flipper_length,body_mass,sex,model_name):
    dict_model = {
                "Decision Tree Classifier":"./models/penguins_dtc.pkl",
                "Random Forest":"./models/penguins_rfc.pkl",
                "SVC":"./models/penguins_svc.pkl",
            }
    penguins = sns.load_dataset("penguins")
    
    X, y = penguins.iloc[:,0:], penguins.iloc[:,0]


    with open(dict_model[model_name], 'rb') as file:
        model = joblib.load(file)

        

    processed_data = model['preprocessor'].transform(X)
    predicted_test = model['classifier'].predict(processed_data)

    accuracy = accuracy_score(y, predicted_test)

    input_data = pd.DataFrame([[island, bill_length, bill_depth, flipper_length, body_mass, sex]],
                                   columns=["island", "bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g", "sex"])
    prediction = model.predict(input_data)[0]
    print(prediction)
    return f"Model accuracy : {accuracy}",f"Predicted specie : {prediction}"