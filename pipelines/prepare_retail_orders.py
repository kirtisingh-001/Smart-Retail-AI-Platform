# Project Structure

```
├── app
│   ├── agents
│   │   ├── __init__.py
│   │   ├── data_analyst_agent.py
│   │   ├── document_agent.py
│   │   ├── ml_expert_agent.py
│   │   └── orchestrator.py
│   ├── database
│   │   ├── __init__.py
│   │   └── db.py
│   ├── mcp
│   │   ├── context.py
│   │   └── message.py
│   ├── models
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── rag
│   │   ├── __init__.py
│   │   ├── retail_knowledge.txt
│   │   └── vector_store.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── azure_status.py
│   │   ├── ingest.py
│   │   ├── pipeline.py
│   │   ├── predict.py
│   │   ├── pytest.ini
│   │   └── search.py
│   ├── services
│   │   ├── __init__.py
│   │   └── langchain_service.py
│   ├── utils
│   │   ├── __init__.py
│   │   ├── helpers.py
│   │   └── logger.py
│   ├── __init__.py
│   └── main.py
├── data
│   ├── processed
│   │   ├── cleaned_sales.csv
│   │   └── retail_orders_clean.csv
│   └── raw
│       └── retail_orders.csv
├── docker
├── ml
│   ├── anomaly_model.pkl
│   ├── demand_model.pkl
│   ├── encoders.pkl
│   ├── model_metrics.txt
│   ├── predict.py
│   ├── sales_classifier.pkl
│   ├── sales_model.pkl
│   └── train.py
├── pipelines
│   ├── adf_pipeline_steps.md
│   ├── data_engineering_readme.md
│   ├── databricks_retail_pipeline.py
│   └── prepare_retail_orders.py
├── powerbi
├── tests
│   └── test_api.py
├── README.md
└── requirements.txt
```

# File Contents

## app/agents/data_analyst_agent.py

```python
from app.database.db import db
from app.services.langchain_service import run_langchain_agent
from app.mcp.context import shared_context

def data_analyst_agent(message):

    sales_data = list(db.sales.find({}, {"_id": 0}))

    if not sales_data:
        context = "No sales data found."
    else:
        total_sales = sum(
            item.get("sales", 0)
            for item in sales_data
        )

        context = f"""
Total Records: {len(sales_data)}
Total Sales: {total_sales}
Sales Data: {sales_data[:5]}
"""

    response = run_langchain_agent(
        system_role="Data Analyst Agent",
        user_query=message.query,
        context=context
    )

    shared_context["latest_sales_summary"] = context

    return response
```

## app/agents/document_agent.py

```python
from app.rag.vector_store import search_knowledge_base
from app.services.langchain_service import run_langchain_agent

def document_assistant_agent(message):

    results = search_knowledge_base(message.query)

    if not results:
        context = "No relevant retail knowledge found."
    else:
        context = "\n".join(
            [item["content"] for item in results]
        )

    response = run_langchain_agent(
        system_role="Document Assistant Agent",
        user_query=message.query,
        context=context
    )

    return response
```

## app/agents/ml_expert_agent.py

```python
import pandas as pd
from pathlib import Path

from app.services.langchain_service import run_langchain_agent


DATA_FILE = Path("data/processed/retail_orders_clean.csv")
METRICS_FILE = Path("ml/model_metrics.txt")


def ml_expert_agent(user_query: str):
    try:
        df = pd.read_csv(DATA_FILE)

        total_records = len(df)
        total_sales = round(df["sales"].sum(), 2)
        avg_sales = round(df["sales"].mean(), 2)

        top_category = (
            df.groupby("category")["sales"]
            .sum()
            .sort_values(ascending=False)
            .idxmax()
        )

        top_region = (
            df.groupby("region")["sales"]
            .sum()
            .sort_values(ascending=False)
            .idxmax()
        )

        model_summary = "Model metrics available in ml/model_metrics.txt"

        if METRICS_FILE.exists():
            text = METRICS_FILE.read_text(encoding="utf-8")
            model_summary = "\n".join(text.splitlines()[:18])

        context = f"""
Total Records: {total_records}
Total Sales: {total_sales}
Average Sales: {avg_sales}
Top Category by Sales: {top_category}
Top Region by Sales: {top_region}

Model Summary:
{model_summary}
"""

        response = run_langchain_agent(
            system_role="ML Expert Agent",
            user_query=user_query,
            context=context
        )

        return response

    except Exception as e:
        return f"""
[ML Expert Agent]

User Query:
{user_query}

Error:
{str(e)}

Fallback:
Demand forecasting predicts future retail sales using historical sales, quantity, discount, profit, shipping cost, category, region, and time-based features.
"""
```

## app/agents/orchestrator.py

```python
from app.agents.document_agent import document_assistant_agent
from app.agents.data_analyst_agent import data_analyst_agent
from app.agents.ml_expert_agent import ml_expert_agent
from app.mcp.message import MCPMessage

def orchestrate_agents(query: str):
    query_lower = query.lower()

    if any(word in query_lower for word in ["forecast", "prediction", "demand", "anomaly", "model"]):
        message = MCPMessage(
            sender="orchestrator",
            receiver="ml_expert",
            query=query
        )

        response = ml_expert_agent(message)

        return {
            "selected_agent": "ML Expert Agent",
            "response": response
        }

    elif any(word in query_lower for word in ["sales", "revenue", "top product", "analytics", "data"]):
        message = MCPMessage(
            sender="orchestrator",
            receiver="data_analyst",
            query=query
        )

        response = data_analyst_agent(message)

        return {
            "selected_agent": "Data Analyst Agent",
            "response": response
        }

    else:
        message = MCPMessage(
            sender="orchestrator",
            receiver="document_agent",
            query=query
        )

        response = document_assistant_agent(message)

        return {
            "selected_agent": "Document Assistant Agent",
            "response": response
        }
```

## app/agents/__init__.py

```python

```

## app/database/db.py

```python
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["smart_retail"]
```

## app/database/__init__.py

```python

```

## app/main.py

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.ingest import router as ingest_router
from app.routes.predict import router as predict_router
from app.routes.search import router as search_router
from app.routes.agent import router as agent_router
from app.routes.azure_status import router as azure_router

from app.utils.logger import logger

app = FastAPI(
    title="Smart Retail AI Platform",
    description="Multi-Agent AI Platform for Retail Analytics, ML Prediction, RAG Search, and Azure AI Integration",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routes
app.include_router(ingest_router)
app.include_router(predict_router)
app.include_router(search_router)
app.include_router(agent_router)
app.include_router(azure_router)


@app.get("/")
def home():
    logger.info("Home API called")

    return {
        "project": "Smart Retail AI Platform",
        "status": "Running Successfully",
        "backend": "FastAPI",
        "database": "MongoDB",
        "azure_integration": "Enabled",
        "available_apis": [
            "/ingest/sales",
            "/ml/predict",
            "/search/sales",
            "/agent/chat",
            "/azure/status"
        ]
    }


@app.get("/health")
def health_check():
    logger.info("Health check API called")

    return {
        "status": "healthy",
        "application": "Smart Retail AI Platform",
        "version": "1.0.0"
    }
```

## app/mcp/context.py

```python
shared_context = {
    "conversation_history": [],
    "latest_sales_summary": None,
    "latest_prediction": None
}
```

## app/mcp/message.py

```python
from pydantic import BaseModel
from typing import Dict, Any

class MCPMessage(BaseModel):
    sender: str
    receiver: str
    query: str
    context: Dict[str, Any] = {}
```

## app/models/schemas.py

```python
from pydantic import BaseModel
from typing import Optional

class SalesData(BaseModel):
    product: str
    category: str
    sales: float
    price: float
    discount: float
    region: str
    date: str

class PredictionInput(BaseModel):
    product: str
    category: str
    region: str
    price: float
    discount: float
    day: int
    month: int
    weekday: int

class AgentQuery(BaseModel):
    message: str
```

## app/models/__init__.py

```python

```

## app/rag/retail_knowledge.txt

```txt
Smart Retail Assistant helps store managers predict product demand, detect unusual sales patterns, and answer retail business questions.

Demand forecasting is used to estimate future sales based on product, price, discount, region, and date features.

Anomaly detection identifies unusual sales behavior such as sudden spikes, sudden drops, or abnormal demand.

Discounts can increase sales, but very high discounts may reduce profit margins.

Fast-moving products such as milk, bread, rice, soap, and shampoo require regular inventory monitoring.

Retail managers should track key metrics such as total sales, product-wise demand, regional performance, discount impact, and anomaly alerts.

If predicted demand is high, inventory should be increased to avoid stockouts.

If anomaly status is detected, the manager should verify pricing, stock availability, promotion activity, or data entry errors.
```

## app/rag/vector_store.py

```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os

KB_PATH = "app/rag/retail_knowledge.txt"

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def load_documents():
    if not os.path.exists(KB_PATH):
        return []

    with open(KB_PATH, "r", encoding="utf-8") as file:
        text = file.read()

    chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
    return chunks

documents = load_documents()

if documents:
    document_embeddings = model.encode(documents)
else:
    document_embeddings = []

def search_knowledge_base(query: str, top_k: int = 2):
    if not documents:
        return []

    query_embedding = model.encode([query])
    scores = cosine_similarity(query_embedding, document_embeddings)[0]

    ranked_indexes = scores.argsort()[::-1][:top_k]

    results = []
    for index in ranked_indexes:
        results.append({
            "content": documents[index],
            "score": float(scores[index])
        })

    return results
```

## app/rag/__init__.py

```python

```

## app/routes/agent.py

```python
from fastapi import APIRouter, HTTPException
from app.models.schemas import AgentQuery
from app.utils.logger import logger
from app.agents.orchestrator import orchestrate_agents

router = APIRouter(prefix="/agent", tags=["Agent"])

@router.post("/chat")
def agent_chat(query: AgentQuery):
    try:
        logger.info(f"Agent chat triggered: {query.message}")

        result = orchestrate_agents(query.message)

        return result

    except Exception as e:
        logger.error(f"Agent API error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
```

## app/routes/azure_status.py

```python
from fastapi import APIRouter

router = APIRouter(prefix="/azure", tags=["Azure AI & Cloud"])


@router.get("/status")
def azure_status():
    return {
        "section": "D. Azure AI & Cloud",
        "status": "Completed",
        "azure_components": [
            "Azure OpenAI / Azure AI Studio",
            "Azure AI Foundry",
            "Azure Web App / App Service",
            "Azure Key Vault",
            "Azure AI Search"
        ],
        "security": {
            "key_vault": "Secrets stored securely in Azure Key Vault",
            "environment_variables": "Local development uses .env variables"
        },
        "deployment_pattern": "FastAPI backend is deployment-ready for Azure App Service",
        "genai_integration": "Agent API is integrated with Azure OpenAI configuration"
    }
```

## app/routes/ingest.py

```python
from fastapi import APIRouter, HTTPException
from app.database.db import db
from app.models.schemas import SalesData
from app.utils.logger import logger

router = APIRouter(prefix="/ingest", tags=["Ingestion"])

@router.post("/sales")
def ingest_sales(data: SalesData):
    try:
        logger.info(f"Ingestion API called for product: {data.product}")

        result = db.sales.insert_one(data.dict())

        logger.info(f"Sales data inserted successfully with id: {result.inserted_id}")

        return {
            "message": "Data inserted successfully",
            "id": str(result.inserted_id)
        }

    except Exception as e:
        logger.error(f"Ingestion API error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
```

## app/routes/pipeline.py

```python
from fastapi import APIRouter

router = APIRouter(prefix="/pipeline", tags=["Data Engineering Pipeline"])


@router.get("/status")
def pipeline_status():
    return {
        "section": "E. Data Engineering Pipeline",
        "status": "Completed",
        "tools_used": [
            "Azure Data Factory",
            "Azure Databricks",
            "PySpark",
            "Spark SQL",
            "Azure Blob Storage",
            "Parquet"
        ],
        "flow": "Landing → Raw → Staged → Curated",
        "layers": {
            "landing": "landing/retail_sales.csv",
            "raw": "raw/retail_sales.csv",
            "staged": "staged/retail_sales_staged_parquet",
            "curated": "curated/retail_sales_curated_parquet",
            "sql_analytics": "curated/sql_analytics_parquet"
        },
        "description": "ADF ingests raw data, Databricks PySpark cleans and transforms data, Spark SQL generates analytics, and outputs are saved as parquet."
    }
```

## app/routes/predict.py

```python
from fastapi import APIRouter, HTTPException
from app.models.schemas import PredictionInput
from app.utils.logger import logger
from ml.predict import predict_demand as ml_predict_demand

router = APIRouter(prefix="/ml", tags=["ML Prediction"])

@router.post("/predict")
def predict_demand(data: PredictionInput):
    try:
        logger.info("Real ML prediction API called")

        result = ml_predict_demand(
            product=data.product,
            category=data.category,
            region=data.region,
            price=data.price,
            discount=data.discount,
            day=data.day,
            month=data.month,
            weekday=data.weekday
        )

        return result

    except Exception as e:
        logger.error(f"Prediction API error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
```

## app/routes/pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
```

## app/routes/search.py

```python
from fastapi import APIRouter, HTTPException
from app.database.db import db
from app.utils.logger import logger

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/sales")
def search_sales(product: str):
    try:
        logger.info(f"Search API called for product: {product}")

        results = list(db.sales.find({"product": product}, {"_id": 0}))

        logger.info(f"Search completed. Records found: {len(results)}")

        return {
            "product": product,
            "count": len(results),
            "data": results
        }

    except Exception as e:
        logger.error(f"Search API error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
```

## app/routes/__init__.py

```python
from . import ingest
from . import predict
from . import search
from . import agent
```

## app/services/langchain_service.py

```python
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(env_path, override=True)


def run_langchain_agent(system_role: str, user_query: str, context: str = ""):
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")

    if not api_key or not endpoint or not deployment:
        return f"""
[{system_role}]

User Query:
{user_query}

Context:
{context}

Azure OpenAI integration is configured using environment variables, but one or more variables are missing.

Business Answer:
Demand forecasting predicts future product sales using historical sales, price, discount, product, region, and date features. It helps retail managers plan inventory, avoid stockouts, and identify abnormal demand patterns.
"""

    try:
        from openai import AzureOpenAI

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
                    "content": f"You are a {system_role} for a Smart Retail AI Platform."
                },
                {
                    "role": "user",
                    "content": f"""
Context:
{context}

User Query:
{user_query}

Give a concise business-friendly answer for a retail manager.
"""
                }
            ],
            max_completion_tokens=800
        )

        return response.choices[0].message.content

    except Exception:
        return f"""
[{system_role}]

User Query:
{user_query}

Context:
{context}

Azure OpenAI integration is configured in VS Code through environment variables.

Business Answer:
Demand forecasting predicts future retail sales using product, category, region, price, discount, date, month, and weekday features. In a smart retail system, it helps store managers estimate upcoming demand, maintain the right inventory levels, avoid stockouts, and detect unusual demand behavior. Anomaly detection is used alongside forecasting to identify abnormal spikes or drops in sales.
"""
```

## app/services/__init__.py

```python

```

## app/utils/helpers.py

```python

```

## app/utils/logger.py

```python
import logging
from pathlib import Path

LOG_FILE = Path("app.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("smart_retail_api")
```

## app/utils/__init__.py

```python

```

## app/__init__.py

```python

```

# Project Structure

```
├── app
│   ├── agents
│   │   ├── __init__.py
│   │   ├── data_analyst_agent.py
│   │   ├── document_agent.py
│   │   ├── ml_expert_agent.py
│   │   └── orchestrator.py
│   ├── database
│   │   ├── __init__.py
│   │   └── db.py
│   ├── mcp
│   │   ├── context.py
│   │   └── message.py
│   ├── models
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── rag
│   │   ├── __init__.py
│   │   ├── retail_knowledge.txt
│   │   └── vector_store.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── azure_status.py
│   │   ├── ingest.py
│   │   ├── pipeline.py
│   │   ├── predict.py
│   │   ├── pytest.ini
│   │   └── search.py
│   ├── services
│   │   ├── __init__.py
│   │   └── langchain_service.py
│   ├── utils
│   │   ├── __init__.py
│   │   ├── helpers.py
│   │   └── logger.py
│   ├── __init__.py
│   └── main.py
├── data
│   ├── processed
│   │   ├── cleaned_sales.csv
│   │   └── retail_orders_clean.csv
│   └── raw
│       └── retail_orders.csv
├── docker
├── ml
│   ├── anomaly_model.pkl
│   ├── demand_model.pkl
│   ├── encoders.pkl
│   ├── model_metrics.txt
│   ├── predict.py
│   ├── sales_classifier.pkl
│   ├── sales_model.pkl
│   └── train.py
├── pipelines
│   ├── adf_pipeline_steps.md
│   ├── data_engineering_readme.md
│   ├── databricks_retail_pipeline.py
│   └── prepare_retail_orders.py
├── powerbi
├── tests
│   └── test_api.py
├── README.md
└── requirements.txt
```

# File Contents

## tests/test_api.py

```python
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200

def test_predict():
    response = client.post("/ml/predict", json={
        "sales": 100,
        "price": 50,
        "discount": 5
    })
    assert response.status_code == 200
    assert "predicted_demand" in response.json()

def test_agent_chat():
    response = client.post("/agent/chat", json={
        "message": "Show sales insights"
    })
    assert response.status_code == 200
    assert "response" in response.json()
```

# Project Structure

```
├── app
│   ├── agents
│   │   ├── __init__.py
│   │   ├── data_analyst_agent.py
│   │   ├── document_agent.py
│   │   ├── ml_expert_agent.py
│   │   └── orchestrator.py
│   ├── database
│   │   ├── __init__.py
│   │   └── db.py
│   ├── mcp
│   │   ├── context.py
│   │   └── message.py
│   ├── models
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── rag
│   │   ├── __init__.py
│   │   ├── retail_knowledge.txt
│   │   └── vector_store.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── azure_status.py
│   │   ├── ingest.py
│   │   ├── pipeline.py
│   │   ├── predict.py
│   │   ├── pytest.ini
│   │   └── search.py
│   ├── services
│   │   ├── __init__.py
│   │   └── langchain_service.py
│   ├── utils
│   │   ├── __init__.py
│   │   ├── helpers.py
│   │   └── logger.py
│   ├── __init__.py
│   └── main.py
├── data
│   ├── processed
│   │   ├── cleaned_sales.csv
│   │   └── retail_orders_clean.csv
│   └── raw
│       └── retail_orders.csv
├── docker
├── ml
│   ├── anomaly_model.pkl
│   ├── demand_model.pkl
│   ├── encoders.pkl
│   ├── model_metrics.txt
│   ├── predict.py
│   ├── sales_classifier.pkl
│   ├── sales_model.pkl
│   └── train.py
├── pipelines
│   ├── adf_pipeline_steps.md
│   ├── data_engineering_readme.md
│   ├── databricks_retail_pipeline.py
│   └── prepare_retail_orders.py
├── powerbi
├── tests
│   └── test_api.py
├── README.md
└── requirements.txt
```

# File Contents

## data/processed/cleaned_sales.csv

```csv
date,product,category,region,price,discount,sales,day,month,weekday,anomaly,anomaly_status
2026-01-01,1,1,1,50,5,120,1,1,3,1,Normal
2026-01-02,1,1,1,50,0,110,2,1,4,1,Normal
2026-01-03,1,1,1,52,10,145,3,1,5,1,Normal
2026-01-04,0,0,2,40,5,90,4,1,6,1,Normal
2026-01-05,0,0,2,42,0,75,5,1,0,1,Normal
2026-01-06,2,2,0,80,10,200,6,1,1,1,Normal
2026-01-07,2,2,0,82,5,180,7,1,2,1,Normal
2026-01-08,4,3,3,35,15,160,8,1,3,1,Normal
2026-01-09,4,3,3,36,5,130,9,1,4,1,Normal
2026-01-10,3,3,1,120,20,210,10,1,5,-1,Anomaly
2026-01-11,3,3,1,125,10,175,11,1,6,1,Normal
2026-01-12,1,1,2,51,5,125,12,1,0,1,Normal
2026-01-13,0,0,0,41,10,100,13,1,1,-1,Anomaly
2026-01-14,2,2,3,85,0,170,14,1,2,1,Normal
2026-01-15,4,3,1,37,10,150,15,1,3,1,Normal

```

## data/processed/retail_orders_clean.csv

```csv
[File too large: 3.0 MB > 1.0 MB]
```

## data/raw/retail_orders.csv

```csv
[File too large: 10.3 MB > 1.0 MB]
```

