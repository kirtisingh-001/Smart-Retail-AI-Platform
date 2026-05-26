from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import AzureOpenAI

from app.services.keyvault_service import get_config_value
from app.utils.logger import logger


router = APIRouter(prefix="/azure", tags=["Azure OpenAI"])


class AzureChatRequest(BaseModel):
    message: str


@router.post("/openai-chat")
def azure_openai_chat(request: AzureChatRequest):
    try:
        api_key = get_config_value("AZURE_OPENAI_API_KEY", required=True)
        endpoint = get_config_value("AZURE_OPENAI_ENDPOINT", required=True)
        deployment = get_config_value("AZURE_OPENAI_DEPLOYMENT", required=True)
        api_version = get_config_value(
            "AZURE_OPENAI_API_VERSION",
            default="2024-12-01-preview"
        )

        client = AzureOpenAI(
            api_key=api_key,
            azure_endpoint=endpoint,
            api_version=api_version
        )

        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {
                    "role": "system",
                    "content": "You are an Azure OpenAI assistant for a Smart Retail AI project."
                },
                {
                    "role": "user",
                    "content": request.message
                }
            ],
            max_completion_tokens=200
        )

        logger.info("Azure OpenAI direct chat endpoint called successfully")

        return {
            "service": "Azure OpenAI",
            "deployment": deployment,
            "status": "working",
            "config_source": "Azure Key Vault / Environment Variables",
            "response": response.choices[0].message.content
        }

    except Exception as e:
        logger.error(f"Azure OpenAI direct chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))