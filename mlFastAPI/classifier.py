import pandas as pd
import torch
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

dataset = pd.read_csv("/Users/shahmuhammadraditrahman/Desktop/fastAPI-tutorial/mlFastAPI/diabetes.csv")

X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

X_train = torch.tensor(X_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)

y_train = torch.tensor(y_train, dtype=torch.float32)
y_test = torch.tensor(y_test, dtype=torch.float32)

train_dataloader = DataLoader(
    dataset=list(zip(X_train, y_train)), batch_size=32, shuffle=True
)

test_dataloader = DataLoader(
    dataset=list(zip(X_test, y_test)), batch_size=32, shuffle=True
)

class Classifier(nn.Module):
    def __init__(self, in_features: int = 8, num_output: int = 1):
        super().__init__()
        
        self.in_features = in_features
        self.num_outputs = num_output
        self.out_features = self.num_outputs * 32 if self.num_outputs == 1 else self.out_features * 16
        
        self.layers = []
        
        for index in range(4):
            if index == 0:
                self.layers.append(nn.Linear(in_features=self.in_features, out_features=self.out_features))
            else:
                self.layers.append(nn.Linear(in_features=self.out_features, out_features=self.out_features // 2))
                self.layers.append(nn.BatchNorm1d(self.out_features//2))
                self.layers.append(nn.ReLU())
            
                self.out_features = self.out_features // 2
            
        self.network = self.layers.append(
            nn.Sequential(nn.Linear(in_features=self.out_features, out_features=self.num_outputs), nn.Sigmoid())
        )
        self.model = nn.Sequential(*self.layers)
        
    def forward(self, x):
        if not isinstance(x, torch.Tensor):
            raise TypeError("Input must be a tensor")
        x = self.model(x)
        
        return x.view(-1)
    
clf = Classifier(in_features=X.shape[1], num_output=1)

device = "mps" if torch.backends.mps.is_available() else "cpu"

clf.to(device)

criterion = nn.BCELoss()
optimizer = torch.optim.Adam(clf.parameters(), lr=0.001)


def train(model, epochs, train_dataloader, test_dataloader):
    for epoch in range(epochs):
        for features, labels in train_dataloader:
            features = features.to(device)
            labels = labels.to(device)
            
            predicted = model(features)
            loss = criterion(predicted, labels)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        if epoch % 10 == 0:
            print(f"Epoch {epoch} loss: {loss}")
            
            with torch.no_grad():
                for features, labels in test_dataloader:
                    features = features.to(device)
                    labels = labels.to(device)
                    
                    predicted = model(features)
                    loss = criterion(predicted, labels)
                    
    torch.save(clf.state_dict(), "classifier.pth")
    print("Model saved and training is done".title())


if __name__ == "__main__":
    train(clf, 20, train_dataloader, test_dataloader)
    