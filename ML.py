import joblib
from fastapi import FastAPI

app = FastAPI()
model = joblib.load("./knn.joblib")


def predict(manuals):
    feature = manuals
    prediction = model.get_top_recipes(feature)
    return {
        'prediction': prediction
    }
