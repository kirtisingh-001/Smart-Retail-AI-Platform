from fastapi import APIRouter, HTTPException

from app.services.keyvault_service import check_keyvault_status
from app.utils.logger import logger


router = APIRouter(prefix="/azure", tags=["Azure Key Vault"])


@router.get("/keyvault-status")
def keyvault_status():
    try:
        logger.info("Azure Key Vault status API called")

        status = check_keyvault_status()

        return {
            "service": "Azure Key Vault",
            "status": "checked",
            "message": "Secret availability checked without exposing values",
            "details": status
        }

    except Exception as e:
        logger.error(f"Azure Key Vault status error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))