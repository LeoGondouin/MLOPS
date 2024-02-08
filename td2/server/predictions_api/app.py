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

import pandas as pd

dict_model = {
                "Decision Tree Classifier":DecisionTreeClassifier(),
                "Random Forest":RandomForestClassifier(),
                "SVC":SVC(),
            }

app = FastAPI()


@app.get("/predict/iris")
def predictIris(sepal_length,sepal_width,petal_length,petal_width,model_name):

    iris = load_iris()
    X, y = iris.data, iris.target


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    model = dict_model[model_name]

    
    model.fit(X_train, y_train)

    predicted_test = model.predict(X_test)
    accuracy = accuracy_score(y_test,predicted_test)

    prediction = model.predict([[sepal_length,sepal_width,petal_length,petal_width]])[0]
    prediction = iris.target_names[prediction]

    return f"Model accuracy : {accuracy}",f"Predicted specie : {prediction}"

@app.get("/predict/penguins")
def predictPenguins(island,bill_length,bill_depth,flipper_length,body_mass,sex,model_name):
    penguins = sns.load_dataset("penguins")

    X, y = penguins.iloc[:,0:], penguins.iloc[:,0]

    categorical_cols = ["island", "sex"]
    numerical_cols = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', SimpleImputer(strategy="median"), numerical_cols),
            ('cat', OneHotEncoder(), categorical_cols)
        ])

    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', dict_model[model_name])
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,stratify=penguins["species"])

    model.fit(X_train, y_train)

    predicted_test = model.predict(X_test)

    accuracy = accuracy_score(y_test, predicted_test)

    input_data = pd.DataFrame([[island, bill_length, bill_depth, flipper_length, body_mass, sex]],
                                   columns=["island", "bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g", "sex"])
    prediction = model.predict(input_data)[0]

    return f"Model accuracy : {accuracy}",f"Predicted specie : {prediction}"