import requests
from fastapi import APIRouter, HTTPException, Query

from app.services.keyvault_service import get_config_value
from app.utils.logger import logger


router = APIRouter(prefix="/azure-search", tags=["Azure AI Search"])

API_VERSION = "2024-07-01"


def get_search_config():
    """
    Reads Azure AI Search configuration from:
    1. Azure Key Vault, if enabled and accessible
    2. .env / environment variables as fallback
    """

    endpoint = get_config_value("AZURE_SEARCH_ENDPOINT", required=True)

    index_name = get_config_value(
        "AZURE_SEARCH_INDEX_NAME",
        default="retail-knowledge-index"
    )

    key = get_config_value("AZURE_SEARCH_ADMIN_KEY", required=True)

    return endpoint.rstrip("/"), index_name, key


@router.post("/sync")
def sync_retail_knowledge_to_search():
    """
    Creates Azure AI Search index and uploads sample retail knowledge documents.
    This endpoint proves Azure Cognitive Search / Azure AI Search integration.
    """

    try:
        endpoint, index_name, key = get_search_config()

        headers = {
            "Content-Type": "application/json",
            "api-key": key
        }

        index_schema = {
            "name": index_name,
            "fields": [
                {
                    "name": "id",
                    "type": "Edm.String",
                    "key": True,
                    "filterable": True
                },
                {
                    "name": "title",
                    "type": "Edm.String",
                    "searchable": True
                },
                {
                    "name": "content",
                    "type": "Edm.String",
                    "searchable": True
                },
                {
                    "name": "category",
                    "type": "Edm.String",
                    "searchable": True,
                    "filterable": True,
                    "facetable": True
                },
                {
                    "name": "source",
                    "type": "Edm.String",
                    "filterable": True
                }
            ]
        }

        create_index_url = (
            f"{endpoint}/indexes/{index_name}"
            f"?api-version={API_VERSION}"
        )

        index_response = requests.put(
            create_index_url,
            headers=headers,
            json=index_schema,
            timeout=20
        )

        if index_response.status_code not in [200, 201, 204]:
            logger.error(f"Azure Search index creation failed: {index_response.text}")
            raise HTTPException(
                status_code=index_response.status_code,
                detail=index_response.text
            )

        documents = {
            "value": [
                {
                    "@search.action": "upload",
                    "id": "1",
                    "title": "Demand Forecasting",
                    "content": (
                        "Demand forecasting predicts future retail sales using "
                        "historical sales, product category, region, discount, "
                        "seasonality and customer demand patterns. It helps "
                        "retailers avoid stockouts and overstocking."
                    ),
                    "category": "Machine Learning",
                    "source": "Smart Retail Knowledge Base"
                },
                {
                    "@search.action": "upload",
                    "id": "2",
                    "title": "Anomaly Detection",
                    "content": (
                        "Anomaly detection identifies unusual sales spikes, "
                        "sudden drops, suspicious discounts, or abnormal demand "
                        "behavior in retail data."
                    ),
                    "category": "Analytics",
                    "source": "Smart Retail Knowledge Base"
                },
                {
                    "@search.action": "upload",
                    "id": "3",
                    "title": "Inventory Optimization",
                    "content": (
                        "Inventory optimization helps store managers maintain "
                        "the right stock level, reduce stockouts, avoid "
                        "overstocking and improve customer satisfaction."
                    ),
                    "category": "Retail Operations",
                    "source": "Smart Retail Knowledge Base"
                },
                {
                    "@search.action": "upload",
                    "id": "4",
                    "title": "Smart Retail AI Assistant",
                    "content": (
                        "A Smart Retail AI Assistant combines machine learning, "
                        "analytics, retrieval search, and GenAI agents to support "
                        "retail decision making."
                    ),
                    "category": "GenAI",
                    "source": "Smart Retail Knowledge Base"
                }
            ]
        }

        upload_url = (
            f"{endpoint}/indexes/{index_name}/docs/index"
            f"?api-version={API_VERSION}"
        )

        upload_response = requests.post(
            upload_url,
            headers=headers,
            json=documents,
            timeout=20
        )

        if upload_response.status_code not in [200, 201, 204]:
            logger.error(f"Azure Search document upload failed: {upload_response.text}")
            raise HTTPException(
                status_code=upload_response.status_code,
                detail=upload_response.text
            )

        logger.info("Azure AI Search sync completed successfully")

        return {
            "service": "Azure AI Search",
            "operation": "sync",
            "status": "completed",
            "index_name": index_name,
            "index_status_code": index_response.status_code,
            "upload_status_code": upload_response.status_code,
            "documents_uploaded": 4,
            "config_source": "Azure Key Vault / Environment Variables"
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Azure AI Search sync error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/query")
def query_azure_search(
    q: str = Query("demand forecasting inventory", description="Search query"),
    top: int = Query(3, description="Number of search results")
):
    """
    Queries Azure AI Search index.
    This endpoint proves cloud-based search retrieval is working.
    """

    try:
        endpoint, index_name, key = get_search_config()

        url = (
            f"{endpoint}/indexes/{index_name}/docs/search"
            f"?api-version={API_VERSION}"
        )

        headers = {
            "Content-Type": "application/json",
            "api-key": key
        }

        body = {
            "search": q,
            "top": top
        }

        response = requests.post(
            url,
            headers=headers,
            json=body,
            timeout=20
        )

        logger.info(f"Azure AI Search query called: {q}")
        logger.info(f"Azure AI Search status code: {response.status_code}")

        if response.status_code != 200:
            logger.error(f"Azure AI Search query failed: {response.text}")
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text
            )

        data = response.json()

        results = []

        for item in data.get("value", []):
            results.append({
                "title": item.get("title"),
                "category": item.get("category"),
                "content": item.get("content"),
                "score": item.get("@search.score")
            })

        return {
            "service": "Azure AI Search",
            "operation": "query",
            "status": "working",
            "status_code": response.status_code,
            "index_name": index_name,
            "query": q,
            "count": len(results),
            "results": results,
            "config_source": "Azure Key Vault / Environment Variables"
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Azure AI Search query error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))