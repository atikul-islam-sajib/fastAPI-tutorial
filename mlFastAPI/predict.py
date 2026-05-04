import pandas as pd
import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score

import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Annotated, List, Dict

from mlFastAPI.classifier import Classifier

app = FastAPI()

def load_model():
    dataset = pd.read_csv("/Users/shahmuhammadraditrahman/Desktop/fastAPI-tutorial/mlFastAPI/diabetes.csv")
    
    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, -1].values
    
    classifier = Classifier(in_features=X.shape[1], num_output=len(set(y))-1)
    model_dict = torch.load("classifier.pth")
    classifier.load_state_dict(model_dict)

    return classifier


class Features(BaseModel):
    Pregnancies: Annotated[
        int, Field(..., description="The number of pregnancies", examples=[1, 2, 3])
    ]
    Glucose: Annotated[
        int, Field(..., description="The glucose level", examples=[120, 130, 140])
    ]
    BloodPressure: Annotated[
        int, Field(..., description="The blood pressure", examples=[70, 80, 90])
    ]
    SkinThickness: Annotated[
        int, Field(..., description="The skin thickness", examples=[20, 25, 30])
    ]
    Insulin: Annotated[
        int, Field(..., description="The insulin level", examples=[80, 90, 100])
    ]
    BMI: Annotated[
        float, Field(..., description="The BMI", examples=[25.0, 30.0, 35.0])
    ]
    DiabetesPedigreeFunction: Annotated[
        float,
        Field(
            ..., description="The diabetes pedigree function", examples=[0.5, 0.6, 0.7]
        ),
    ]
    Age: Annotated[int, Field(..., description="The age", examples=[30, 40, 50])]


@app.post("/predict")
def prediction(features: Features):
    input_features = features.model_dump()
    input_features = list(input_features.values())
    input_features = torch.tensor([input_features], dtype=torch.float32)

    clf = load_model()

    clf.eval()

    predicted = clf(input_features)
    predicted = torch.where(predicted > 0.5, 1, 0)

    return {"Prediction": predicted[0].item()}
