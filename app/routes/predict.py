from fastapi import APIRouter, HTTPException

from app.models.schemas import PredictionInput
from app.utils.logger import logger
from ml.predict import predict_sales

router = APIRouter(prefix="/ml", tags=["ML Prediction"])


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