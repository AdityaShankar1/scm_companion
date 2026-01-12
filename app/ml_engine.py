# ml_engine.py
from sklearn.linear_model import LinearRegression
import numpy as np


def predict_days_left(current_stock: int, sales_history: list):
    """
    Predicts how many days until stock hits zero using Linear Regression.
    sales_history: e.g., [5, 7, 6, 8, 10] (last 5 days sales)
    """
    if not sales_history or current_stock <= 0:
        return 0

    # X = days (0, 1, 2...), y = sales units
    X = np.array(range(len(sales_history))).reshape(-1, 1)
    y = np.array(sales_history)

    # Train a simple linear model
    model = LinearRegression()
    model.fit(X, y)

    # Predict average daily sales for the next time step
    avg_future_sales = model.predict([[len(sales_history)]])[0]

    # Avoid division by zero or negative sales
    avg_future_sales = max(avg_future_sales, 1)

    return int(current_stock / avg_future_sales)


def analyze_supplier_risk(supplier_note: str):
    """
    NLP-based Risk Assessment (Heuristic version for performance).
    In a production app, this would call a HuggingFace Transformer.
    """
    risk_keywords = ["delay", "shortage", "strike", "bankruptcy", "fire", "disruption"]
    note_lower = supplier_note.lower()

    if any(word in note_lower for word in risk_keywords):
        return "HIGH RISK"
    return "STABLE"