import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
import json

# Load cleaned data
df = pd.read_csv("data/processed/clean_marketing.csv")  # Assumes you've converted Delta to CSV

# Prepare features and target
features = [
    "Income", "Kidhome", "Teenhome", "Recency",
    "NumWebPurchases", "NumCatalogPurchases", "NumStorePurchases", "NumWebVisitsMonth",
    "MntTotal", "MntRegularProds",
    "marital_Single", "marital_Married", "education_Graduation", "education_Master"
]
target = "Response"  # Changed from Segmentation to Response

X = df[features]
y = df[target]

# Define preprocessing for categorical and numerical columns
categorical_features = []
numeric_features = features

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
    ]
)

# Create pipeline
pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression())
])

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ---------------------------------------------
# Hyperparameter tuning with GridSearchCV
# ---------------------------------------------
# This will search over multiple values of the regularisation parameter `C` for Logistic Regression.
# A lower C means stronger regularisation; higher C reduces regularisation.
# GridSearchCV will perform cross-validation for each value to find the best one.
param_grid = {
    "classifier__C": [0.01, 0.1, 1.0, 10.0, 100.0]
}

# GridSearchCV wraps around our pipeline and performs 5-fold cross-validation for each parameter setting.
grid_search = GridSearchCV(pipeline, param_grid, cv=5)

# Fit the model using grid search
grid_search.fit(X_train, y_train)

# Print the best parameter combination and the best cross-validation score
print("🔍 Best Parameters:", grid_search.best_params_)
print("🏆 Best Cross-Validated Score: {:.4f}".format(grid_search.best_score_))

# Update pipeline to the best estimator found via GridSearchCV for downstream prediction/evaluation
pipeline = grid_search.best_estimator_

# Evaluate
y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred))
# This helps users to understand model stability across different subsets of the data.

# Extra evaluation
print("✅ Additional Evaluation")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Save evaluation metrics to JSON
metrics = {
    "best_params": grid_search.best_params_,
    "cv_score_mean": grid_search.best_score_,
    "test_accuracy": accuracy_score(y_test, y_pred),
    "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
    "classification_report": classification_report(y_test, y_pred, output_dict=True)
}

with open("models/model_metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

print("📊 Evaluation metrics saved to models/model_metrics.json")

# Save test predictions
results = pd.DataFrame({
    "Actual": y_test,
    "Predicted": y_pred
})
results.to_csv("models/test_predictions.csv", index=False)
print("📄 Test predictions saved to models/test_predictions.csv")

# Try predicting on a new example
new_data = pd.DataFrame([{
    "Income": 65000,
    "Kidhome": 0,
    "Teenhome": 1,
    "Recency": 20,
    "NumWebPurchases": 4,
    "NumCatalogPurchases": 2,
    "NumStorePurchases": 5,
    "NumWebVisitsMonth": 6,
    "MntTotal": 1000,
    "MntRegularProds": 700,
    "marital_Single": 1,
    "marital_Married": 0,
    "education_Graduation": 1,
    "education_Master": 0
}])

new_pred = pipeline.predict(new_data)
print("🧪 Prediction for new customer:", new_pred[0])

# Save model
joblib.dump(pipeline, "models/lead_scoring_model.pkl")
print("✅ Model trained and saved.")
