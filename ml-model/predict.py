import json
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Query, Path
from typing import Optional, Annotated, List, Dict, Union
import pickle
import pandas as pd

app = FastAPI()

# Load model
def load_model():
    with open("iris_model.pkl", "rb") as file:
        loaded_model = pickle.load(file)
        print("Model loaded successfully")
        
        return loaded_model


class Iris(BaseModel):
    sepal_length: Annotated[float, Field(..., description="The sepal length", examples=[5.1, 5.2, 5.3])]
    sepal_width: Annotated[float, Field(..., description="The sepal width", examples=[3.5, 3.6, 3.7])]
    petal_length: Annotated[float, Field(..., description="The petal length", examples=[1.4, 1.5, 1.6])]
    petal_width: Annotated[float, Field(..., description="The petal width", examples=[0.2, 0.3, 0.4])]
    
    
@app.post("/predict")
def prediction(features: Iris):
    model = load_model()
    data = pd.DataFrame([features.model_dump()])
    predicted = model.predict(data.values)
    return {"prediction": int(predicted[0])}  # convert numpy int to Python int