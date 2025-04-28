import pandas as pd
import joblib
import json
import logging
from datetime import datetime
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

# This script handles the entire workflow for training a logistic regression model
# to predict marketing campaign responses. It includes data loading, preprocessing,
# model training with hyperparameter tuning, evaluation, and saving of results.

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_data(filepath):
    """
    Load data from a CSV file into a pandas DataFrame.

    Parameters:
    filepath (str): Path to the CSV file.

    Returns:
    pd.DataFrame: Loaded data.
    """
    logging.info(f"Loading data from {filepath}")
    # Read CSV file into DataFrame
    df = pd.read_csv(filepath)
    return df

def build_pipeline(features):
    """
    Create a machine learning pipeline that preprocesses numeric features using standard scaling
    and applies logistic regression for classification.

    Parameters:
    features (list): List of feature column names to include in the model.

    Returns:
    Pipeline: Configured sklearn Pipeline object.
    """
    # Define which features are numeric for preprocessing
    numeric_features = features

    # Setup ColumnTransformer to apply StandardScaler to numeric features
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
        ]
    )

    # Create a pipeline that first preprocesses data then fits logistic regression
    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression())
    ])
    return pipeline

def train_model(X_train, y_train, pipeline, param_grid):
    """
    Train the logistic regression model using GridSearchCV to find the best hyperparameters.

    Parameters:
    X_train (pd.DataFrame): Training feature set.
    y_train (pd.Series): Training target values.
    pipeline (Pipeline): The sklearn pipeline including preprocessing and classifier.
    param_grid (dict): Dictionary with parameters names (str) as keys and lists of parameter settings to try as values.

    Returns:
    best_estimator_: The estimator that was chosen by the search, i.e. estimator which gave highest score.
    best_params_: Parameter setting that gave the best results on the hold out data.
    best_score_: Mean cross-validated score of the best_estimator.
    """
    logging.info("Starting model training with GridSearchCV")
    # Initialize GridSearchCV to tune hyperparameters with 5-fold cross-validation
    grid_search = GridSearchCV(pipeline, param_grid, cv=5)
    # Fit the model on training data
    grid_search.fit(X_train, y_train)

    # Log the best hyperparameters and corresponding score
    logging.info(f"Best Parameters: {grid_search.best_params_}")
    logging.info(f"Best Cross-Validated Score: {grid_search.best_score_:.4f}")

    return grid_search.best_estimator_, grid_search.best_params_, grid_search.best_score_

def evaluate_model(model, X_test, y_test):
    """
    Evaluate the trained model on the test set and generate performance metrics.

    Parameters:
    model (Pipeline): Trained sklearn pipeline/model.
    X_test (pd.DataFrame): Test feature set.
    y_test (pd.Series): True target values for the test set.

    Returns:
    y_pred (np.ndarray): Predicted labels for the test set.
    dict: Dictionary containing accuracy, confusion matrix, and classification report.
    """
    logging.info("Evaluating model on test set")
    # Predict target values using the trained model
    y_pred = model.predict(X_test)
    # Generate detailed classification report as dictionary
    report = classification_report(y_test, y_pred, output_dict=True)
    # Calculate accuracy score
    accuracy = accuracy_score(y_test, y_pred)
    # Create confusion matrix as a list for JSON serialization
    confusion = confusion_matrix(y_test, y_pred)

    logging.info(f"Accuracy: {accuracy:.4f}")

    return y_pred, {
        "test_accuracy": accuracy,
        "confusion_matrix": confusion.tolist(),
        "classification_report": report
    }

def save_artifacts(model, metrics, y_test, y_pred):
    """
    Save the trained model, evaluation metrics, and test predictions to disk.

    Parameters:
    model (Pipeline): Trained sklearn pipeline/model.
    metrics (dict): Dictionary of evaluation metrics to save.
    y_test (pd.Series): True target values for the test set.
    y_pred (np.ndarray): Predicted labels for the test set.
    """
    # Generate timestamp for unique file names
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    model_filename = f"models/lead_scoring_model_{timestamp}.pkl"

    # Save the trained model using joblib
    joblib.dump(model, model_filename)
    logging.info(f"Model saved to {model_filename}")

    # Save metrics as a JSON file
    with open("models/model_metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)
    logging.info("Metrics saved to models/model_metrics.json")

    # Save actual vs predicted results to CSV for further analysis
    results = pd.DataFrame({
        "Actual": y_test,
        "Predicted": y_pred
    })
    results.to_csv("models/test_predictions.csv", index=False)
    logging.info("Test predictions saved to models/test_predictions.csv")

def run_training():
    """
    Main function to run the entire training workflow:
    - Load data
    - Split into train/test sets
    - Build preprocessing and modeling pipeline
    - Train model with hyperparameter tuning
    - Evaluate model on test set
    - Save model, metrics, and predictions
    """
    # Configurations
    filepath = "data/processed/clean_marketing.csv"
    features = [
        "Income", "Kidhome", "Teenhome", "Recency",
        "NumWebPurchases", "NumCatalogPurchases", "NumStorePurchases", "NumWebVisitsMonth",
        "MntTotal", "MntRegularProds",
        "marital_Single", "marital_Married", "education_Graduation", "education_Master"
    ]
    target = "Response"
    param_grid = {
        # Regularization strength parameter for LogisticRegression to tune
        "classifier__C": [0.01, 0.1, 1.0, 10.0, 100.0]
    }

    # Load dataset
    df = load_data(filepath)
    # Select features and target variable
    X = df[features]
    y = df[target]

    # Split the data into training and test sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Build the machine learning pipeline
    pipeline = build_pipeline(features)

    # Train the model with hyperparameter tuning
    model, best_params, cv_score = train_model(X_train, y_train, pipeline, param_grid)

    # Evaluate the trained model on the test set
    y_pred, eval_metrics = evaluate_model(model, X_test, y_test)

    # Combine best params, CV score, and evaluation metrics into one dictionary
    full_metrics = {
        "best_params": best_params,
        "cv_score_mean": cv_score,
        **eval_metrics
    }

    # Save model, metrics, and predictions to files
    save_artifacts(model, full_metrics, y_test, y_pred)

if __name__ == "__main__":
    run_training()
