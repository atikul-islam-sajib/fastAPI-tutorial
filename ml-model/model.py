import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load dataset
iris = load_iris()
X, y = iris.data, iris.target

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")

# Save model
with open("iris_model.pkl", "wb") as file:
    pickle.dump(model, file)
    print("Model saved successfully")

# Load model
with open("iris_model.pkl", "rb") as file:
    loaded_model = pickle.load(file)
    print("Model loaded successfully")

# Predict with loaded model
sample = [[5.1, 3.5, 1.4, 0.2]]  # expected: setosa
prediction = loaded_model.predict(sample)
print(prediction)
print(f"Prediction: {iris.target_names[prediction[0]]}")


print(X[0])
