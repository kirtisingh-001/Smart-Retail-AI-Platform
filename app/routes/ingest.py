from fastapi import APIRouter, HTTPException

from app.database.db import db
from app.models.schemas import SalesData
from app.utils.logger import logger

router = APIRouter(prefix="/ingest", tags=["Ingestion"])


@router.post("/sales")
def ingest_sales(data: SalesData):
    try:
        logger.info(
            f"Ingestion API called for order_id: {data.order_id}, product: {data.product_name}"
        )

        # Pydantic v2 uses model_dump(), older versions use dict()
        try:
            sales_record = data.model_dump()
        except AttributeError:
            sales_record = data.dict()

        result = db.sales.insert_one(sales_record)

        logger.info(
            f"Sales record inserted successfully with id: {result.inserted_id}"
        )

        return {
            "message": "Data inserted successfully",
            "id": str(result.inserted_id),
            "order_id": data.order_id,
            "product_name": data.product_name
        }

    except Exception as e:
        logger.error(f"Ingestion API error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )