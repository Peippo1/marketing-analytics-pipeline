import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
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

# Save model
joblib.dump(pipeline, "models/lead_scoring_model.pkl")
print("✅ Model trained and saved.")
