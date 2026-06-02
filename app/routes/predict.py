from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib

from app.models.schemas import PredictionInput
from app.utils.logger import logger
from ml.predict import predict_sales

router = APIRouter(prefix="/ml", tags=["ML Prediction"])


anomaly_model = joblib.load("ml/anomaly_model.pkl")


class AnomalyInput(BaseModel):
    quantity: int
    discount: float
    profit: float
    shipping_cost: float
    sales: float


@router.post("/predict")
def predict_demand(data: PredictionInput):
    try:
        logger.info("ML prediction API called")

        result = predict_sales(
            product_id=data.product_id,
            ship_mode=data.ship_mode,
            segment=data.segment,
            state=data.state,
            country=data.country,
            market=data.market,
            region=data.region,
            category=data.category,
            sub_category=data.sub_category,
            order_priority=data.order_priority,
            quantity=data.quantity,
            discount=data.discount,
            profit=data.profit,
            shipping_cost=data.shipping_cost,
            ship_days=data.ship_days,
            order_month=data.order_month,
            order_year=data.order_year,
            profit_margin=data.profit_margin
        )

        logger.info(f"Prediction result: {result}")
        return result

    except Exception as e:
        logger.error(f"Prediction API error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/anomaly-detect")
def detect_anomaly(data: AnomalyInput):
    try:
        logger.info("Anomaly detection API called")

        input_df = pd.DataFrame([{
            "quantity": data.quantity,
            "discount": data.discount,
            "profit": data.profit,
            "shipping_cost": data.shipping_cost,
            "sales": data.sales,
            "price": data.sales,
            "month": 5,
            "day": 15,
            "category": 0,
            "region": 0
        }])

        expected_columns = list(anomaly_model.feature_names_in_)

        for col in expected_columns:
            if col not in input_df.columns:
                input_df[col] = 0

        input_df = input_df[expected_columns]

        prediction = anomaly_model.predict(input_df)[0]

        result = "Anomaly" if prediction == -1 else "Normal"

        return {
            "feature": "Anomaly Detection",
            "model": "Isolation Forest",
            "status": "success",
            "prediction": result,
            "message": (
                "This transaction is unusual or suspicious."
                if result == "Anomaly"
                else "This transaction looks normal."
            ),
            "input_data": {
                "quantity": data.quantity,
                "discount": data.discount,
                "profit": data.profit,
                "shipping_cost": data.shipping_cost,
                "sales": data.sales
            }
        }

    except Exception as e:
        logger.error(f"Anomaly detection API error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))