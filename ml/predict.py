import pickle
from pathlib import Path

import pandas as pd


REG_MODEL_FILE = Path("ml/sales_model.pkl")
CLS_MODEL_FILE = Path("ml/sales_classifier.pkl")


def predict_sales(
    product_id: str,
    ship_mode: str,
    segment: str,
    state: str,
    country: str,
    market: str,
    region: str,
    category: str,
    sub_category: str,
    order_priority: str,
    quantity: int,
    discount: float,
    profit: float,
    shipping_cost: float,
    ship_days: int,
    order_month: int,
    order_year: int,
    profit_margin: float
):
    """
    This function loads saved ML models and predicts:
    1. Sales value using regression model
    2. Sales class using classification model
    """

    if not REG_MODEL_FILE.exists():
        raise FileNotFoundError("Regression model not found. Please run ml/train.py first.")

    if not CLS_MODEL_FILE.exists():
        raise FileNotFoundError("Classification model not found. Please run ml/train.py first.")

    with open(REG_MODEL_FILE, "rb") as file:
        regression_model = pickle.load(file)

    with open(CLS_MODEL_FILE, "rb") as file:
        classification_model = pickle.load(file)

    input_data = pd.DataFrame([
        {
            "product_id": product_id,
            "ship_mode": ship_mode,
            "segment": segment,
            "state": state,
            "country": country,
            "market": market,
            "region": region,
            "category": category,
            "sub_category": sub_category,
            "order_priority": order_priority,
            "quantity": quantity,
            "discount": discount,
            "profit": profit,
            "shipping_cost": shipping_cost,
            "ship_days": ship_days,
            "order_month": order_month,
            "order_year": order_year,
            "profit_margin": profit_margin
        }
    ])

    predicted_sales = regression_model.predict(input_data)[0]
    predicted_class = classification_model.predict(input_data)[0]

    return {
        "predicted_sales": round(float(predicted_sales), 2),
        "predicted_sales_class": str(predicted_class)
    }