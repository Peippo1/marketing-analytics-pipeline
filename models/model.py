import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib

# Load cleaned data
df = pd.read_csv("data/processed/clean_delta.csv")  # Assumes you've converted Delta to CSV

# Prepare features and target
features = ["Age", "Income", "Education", "Marital_Status", "TotalSpend"]
target = "Response"

X = df[features]
y = df[target]

# Define preprocessing for categorical and numerical columns
categorical_features = ["Education", "Marital_Status"]
numeric_features = ["Age", "Income", "TotalSpend"]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ]
)

# Create pipeline
pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression())
])

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
pipeline.fit(X_train, y_train)

# Evaluate
y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred))

# Extra evaluation
print("✅ Additional Evaluation")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Save test predictions
results = pd.DataFrame({
    "Actual": y_test,
    "Predicted": y_pred
})
results.to_csv("models/test_predictions.csv", index=False)
print("📄 Test predictions saved to models/test_predictions.csv")

# Try predicting on a new example
new_data = pd.DataFrame([{
    "Age": 35,
    "Income": 65000,
    "Education": "Graduate",
    "Marital_Status": "Single",
    "TotalSpend": 1200
}])

new_pred = pipeline.predict(new_data)
print("🧪 Prediction for new customer:", new_pred[0])

# Save model
joblib.dump(pipeline, "models/lead_scoring_model.pkl")
print("✅ Model trained and saved.")
