from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from fastapi import FastAPI,Request

dict_model = {
                "Decision Tree Classifier":DecisionTreeClassifier(),
                "Random Forest":RandomForestClassifier(),
                "SVC":SVC(),
            }

app = FastAPI()


@app.get("/iris/predict")
def predict(sepal_length,sepal_width,petal_length,petal_width,model_name):

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