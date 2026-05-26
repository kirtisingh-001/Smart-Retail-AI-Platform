\# Smart Retail AI Platform



\## Project Overview



Smart Retail AI Platform is an end-to-end Data + AI solution built using Python, FastAPI, Machine Learning, GenAI agents, Azure AI services, Azure Data Engineering components, and Power BI analytics.



The platform helps retail teams analyze sales performance, predict demand, detect anomalies, search retail knowledge, and interact with AI agents for business insights.



\---



\## Live Deployment



The application is deployed on \*\*Azure App Service / Azure Web App\*\*.



\### Live Application URL



```text

https://smart-retail-api3-hkc0dsadcnfqcmaa.koreacentral-01.azurewebsites.net

```



\### Live Swagger API Documentation



```text

https://smart-retail-api3-hkc0dsadcnfqcmaa.koreacentral-01.azurewebsites.net/docs

```



\### Live Health Check



```text

https://smart-retail-api3-hkc0dsadcnfqcmaa.koreacentral-01.azurewebsites.net/health

```



The multi-agent system is live and executable through:



```http

POST /agent/chat

```



\---



\## Project Modules Covered



| Module | Requirement | Status |

|---|---|---|

| A. Python Fullstack Backend + APIs | FastAPI backend, 4+ REST APIs, MongoDB integration, logging, pytest | Completed |

| B. Machine Learning / Deep Learning | Regression/classification model, feature engineering, training, evaluation, pickle persistence | Completed |

| C. GenAI / Agents | Multi-agent system, prompt engineering, RAG, vector store, MCP-style orchestration | Completed |

| D. Azure AI \& Cloud | Azure OpenAI, Azure AI Foundry, Azure AI Search, Key Vault / environment variables | Completed |

| E. Data Engineering Pipeline | ADF, Databricks, PySpark, Spark SQL, Raw → Staged → Curated flow, Parquet | Completed |

| F. Analytics \& Visualization | Power BI dashboard with KPIs, model outputs, anomaly trends, agent insights | Completed |

| G. Final Deployment | Azure App Service / Web App deployment with live executable APIs | Completed |



\---



\## Tech Stack



\### Backend



\- Python

\- FastAPI

\- Uvicorn

\- Gunicorn

\- Pydantic



\### Database



\- MongoDB / MongoDB Atlas



\### Machine Learning



\- Scikit-learn

\- Pandas

\- NumPy

\- Joblib / Pickle



\### GenAI and Agents



\- Azure OpenAI

\- Azure AI Foundry deployment

\- RAG-based knowledge retrieval

\- Vector store

\- Multi-agent orchestration

\- MCP-style context/message flow



\### Azure Services



\- Azure App Service / Azure Web App

\- Azure OpenAI / Azure AI Studio

\- Azure AI Foundry

\- Azure AI Search

\- Azure Key Vault-ready configuration

\- Azure Data Factory

\- Azure Databricks

\- Azure Blob Storage



\### Analytics



\- Power BI

\- Curated analytics data

\- ML output dashboard

\- Anomaly trend dashboard

\- Agent insights dashboard



\---



\## System Architecture



```mermaid

flowchart TD



&#x20;   USER\[User / Evaluator] --> SWAGGER\[Swagger UI / REST API Testing]



&#x20;   SWAGGER --> API\[FastAPI Backend]



&#x20;   API --> HOME\[Home API]

&#x20;   API --> HEALTH\[Health Check API]

&#x20;   API --> INGEST\[Data Ingestion API]

&#x20;   API --> MLAPI\[ML Prediction API]

&#x20;   API --> SEARCHAPI\[Sales Search API]

&#x20;   API --> AGENTAPI\[Agent Chat API]

&#x20;   API --> AZUREAPI\[Azure AI APIs]

&#x20;   API --> PIPELINEAPI\[Pipeline Status API]



&#x20;   INGEST --> MONGO\[(MongoDB / MongoDB Atlas)]

&#x20;   SEARCHAPI --> MONGO



&#x20;   MLAPI --> MODELFILES\[Saved ML Model Files]

&#x20;   MODELFILES --> REGMODEL\[sales\_model.pkl]

&#x20;   MODELFILES --> CLSMODEL\[sales\_classifier.pkl]



&#x20;   AGENTAPI --> ORCH\[Multi-Agent Orchestrator]



&#x20;   ORCH --> DATAAGENT\[Data Analyst Agent]

&#x20;   ORCH --> DOCAGENT\[Document Assistant Agent]

&#x20;   ORCH --> MLAGENT\[ML Expert Agent]



&#x20;   DATAAGENT --> MONGO

&#x20;   DOCAGENT --> RAG\[RAG Knowledge Base]

&#x20;   MLAGENT --> MODELFILES



&#x20;   RAG --> VECTOR\[Vector Store]

&#x20;   VECTOR --> KB\[Retail Knowledge Base]



&#x20;   AZUREAPI --> OPENAI\[Azure OpenAI / Azure AI Foundry]

&#x20;   AZUREAPI --> SEARCH\[Azure AI Search]

&#x20;   AZUREAPI --> KV\[Key Vault / Environment Variables]



&#x20;   ADF\[Azure Data Factory] --> RAW\[Raw Layer]

&#x20;   RAW --> DBX\[Azure Databricks / PySpark]

&#x20;   DBX --> STAGED\[Staged Parquet Layer]

&#x20;   STAGED --> CURATED\[Curated Parquet Layer]

&#x20;   CURATED --> POWERBI\[Power BI Dashboard]

```



\---



\## Deployment Diagram



```mermaid

flowchart LR



&#x20;   DEV\[Developer Machine<br/>Local Project] --> GIT\[GitHub Repository<br/>kirtisingh-001/smart-retail-ai-platform]



&#x20;   GIT --> DEPLOY\[Azure App Service Deployment<br/>GitHub / Azure Deployment Center]



&#x20;   DEPLOY --> APP\[Azure Web App<br/>smart-retail-api3]



&#x20;   APP --> FASTAPI\[FastAPI Application<br/>app.main:app]



&#x20;   FASTAPI --> SWAGGER\[Live Swagger UI<br/>/docs]



&#x20;   SWAGGER --> EVALUATOR\[Evaluator / User<br/>Live API Testing]



&#x20;   FASTAPI --> HEALTH\[GET /health]

&#x20;   FASTAPI --> ML\[POST /ml/predict]

&#x20;   FASTAPI --> AGENT\[POST /agent/chat]

&#x20;   FASTAPI --> AZSTATUS\[GET /azure/status]

&#x20;   FASTAPI --> AZSEARCH\[GET /azure-search/query]

&#x20;   FASTAPI --> KVSTATUS\[GET /azure/keyvault-status]

&#x20;   FASTAPI --> PIPELINE\[GET /pipeline/status]



&#x20;   ML --> MODELS\[Pickle ML Models]

&#x20;   MODELS --> SALES\[sales\_model.pkl]

&#x20;   MODELS --> CLASSIFIER\[sales\_classifier.pkl]



&#x20;   AGENT --> ORCH\[Multi-Agent Orchestrator]

&#x20;   ORCH --> DATA\[Data Analyst Agent]

&#x20;   ORCH --> DOC\[Document Assistant Agent]

&#x20;   ORCH --> MLEXPERT\[ML Expert Agent]



&#x20;   DOC --> RAG\[RAG Knowledge Base]

&#x20;   RAG --> VECTOR\[Vector Store]



&#x20;   FASTAPI --> MONGO\[(MongoDB Atlas)]

&#x20;   FASTAPI --> OPENAI\[Azure OpenAI / Foundry]

&#x20;   FASTAPI --> SEARCH\[Azure AI Search]

&#x20;   FASTAPI --> ENV\[Azure App Settings<br/>Environment Variables]



&#x20;   ENV --> FASTAPI

```



\---



\## Data Engineering Pipeline Diagram



```mermaid

flowchart TD



&#x20;   LANDING\[Landing Layer<br/>Retail CSV Data] --> RAW\[Raw Layer<br/>Ingested Raw Data]



&#x20;   RAW --> ADF\[Azure Data Factory<br/>Data Ingestion]



&#x20;   ADF --> DBX\[Azure Databricks<br/>PySpark Cleaning and Transformation]



&#x20;   DBX --> STAGED\[Staged Layer<br/>Cleaned Parquet Data]



&#x20;   STAGED --> CURATED\[Curated Layer<br/>Business-ready Parquet Data]



&#x20;   CURATED --> SQL\[Spark SQL Analytics]



&#x20;   SQL --> POWERBI\[Power BI Dashboard]



&#x20;   CURATED --> ML\[ML Training and Prediction]



&#x20;   CURATED --> AGENTS\[Agent-driven Insights]

```



\---



\## Multi-Agent System



The platform includes a multi-agent AI system for retail intelligence.



\### 1. Data Analyst Agent



Answers business analytics questions using retail sales data.



Examples:



\- Sales by region

\- Category performance

\- Top products

\- Business KPI analysis



\### 2. Document Assistant Agent



Uses RAG-based retrieval to answer questions from the retail knowledge base.



Examples:



\- Inventory planning

\- Stockout prevention

\- Demand forecasting concepts

\- Anomaly detection explanation



\### 3. ML Expert Agent



Explains machine learning outputs such as demand prediction and anomaly detection.



Examples:



\- Predicted sales explanation

\- Forecasting output interpretation

\- Anomaly alert reasoning



\---



\## REST API Endpoints



| Method | Endpoint | Purpose |

|---|---|---|

| GET | `/` | Home API |

| GET | `/health` | Health check API |

| POST | `/ingest/sales` | Insert sales data into MongoDB |

| POST | `/ml/predict` | Predict sales and sales class using ML model |

| GET | `/search/sales` | Search sales records |

| POST | `/agent/chat` | Chat with multi-agent system |

| GET | `/azure/status` | Azure AI \& Cloud status |

| POST | `/azure/openai-chat` | Azure OpenAI direct chat test |

| POST | `/azure-search/sync` | Sync retail knowledge to Azure AI Search |

| GET | `/azure-search/query` | Query Azure AI Search index |

| GET | `/azure/keyvault-status` | Check Key Vault / environment variable security status |

| GET | `/pipeline/status` | Data engineering pipeline status |



\---



\## API Testing Proof



The following APIs were tested using Swagger UI and pytest:



| Test | Status |

|---|---|

| Home API | Passed |

| Health API | Passed |

| ML Prediction API | Passed |

| Agent Chat API | Passed |

| Search Sales API | Passed |

| Azure Status API | Passed |

| Pipeline Status API | Passed |



Pytest result:



```text

7 passed

```



\---



\## Sample API Requests



\### 1. Health Check



```http

GET /health

```



Expected response:



```json

{

&#x20; "status": "healthy",

&#x20; "application": "Smart Retail AI Platform",

&#x20; "version": "1.0.0"

}

```



\---



\### 2. ML Prediction



```http

POST /ml/predict

```



Request body:



```json

{

&#x20; "product\_id": "TEC-PH-10000000",

&#x20; "ship\_mode": "Standard Class",

&#x20; "segment": "Consumer",

&#x20; "state": "California",

&#x20; "country": "United States",

&#x20; "market": "US",

&#x20; "region": "West",

&#x20; "category": "Technology",

&#x20; "sub\_category": "Phones",

&#x20; "order\_priority": "Medium",

&#x20; "quantity": 2,

&#x20; "discount": 0.1,

&#x20; "profit": 50.0,

&#x20; "shipping\_cost": 10.0,

&#x20; "ship\_days": 4,

&#x20; "order\_month": 5,

&#x20; "order\_year": 2014,

&#x20; "profit\_margin": 0.2

}

```



Expected response contains:



```json

{

&#x20; "predicted\_sales": 164.29,

&#x20; "predicted\_sales\_class": "Medium",

&#x20; "sales\_class": "Medium"

}

```



\---



\### 3. Agent Chat



```http

POST /agent/chat

```



Request body:



```json

{

&#x20; "message": "Explain demand forecasting and anomaly detection for retail sales."

}

```



Expected response contains:



```json

{

&#x20; "selected\_agent": "ML Expert Agent",

&#x20; "response": "..."

}

```



\---



\### 4. Azure AI Search Query



```http

GET /azure-search/query?q=demand forecasting inventory stockouts\&top=3

```



Expected response contains:



```json

{

&#x20; "service": "Azure AI Search",

&#x20; "operation": "query",

&#x20; "status": "working",

&#x20; "status\_code": 200

}

```



\---



\## Machine Learning Module



The ML module includes:



\- Data cleaning

\- Feature engineering

\- Regression model for sales prediction

\- Classification model for sales class prediction

\- Model evaluation

\- Pickle / Joblib model persistence



Model files:



```text

ml/sales\_model.pkl

ml/sales\_classifier.pkl

ml/model\_metrics.txt

```



The `/ml/predict` endpoint loads these saved model files and returns prediction output.



\---



\## GenAI / RAG Module



The GenAI module includes:



\- Retail knowledge base

\- Vector store

\- Retrieval-Augmented Generation

\- Prompt engineering

\- Multi-agent orchestration

\- Azure OpenAI integration



RAG files:



```text

app/rag/retail\_knowledge.txt

app/rag/vector\_store.py

```



Agent files:



```text

app/agents/data\_analyst\_agent.py

app/agents/document\_agent.py

app/agents/ml\_expert\_agent.py

app/agents/orchestrator.py

```



MCP-style files:



```text

app/mcp/context.py

app/mcp/message.py

```



\---



\## Azure AI \& Cloud Module



The project uses the following Azure components:



| Azure Component | Usage |

|---|---|

| Azure OpenAI / Azure AI Studio | LLM-based response generation |

| Azure AI Foundry | Model deployment pattern |

| Azure AI Search | Retail knowledge search and RAG retrieval |

| Azure Key Vault / Environment Variables | Secret management and security consideration |

| Azure App Service / Web App | Final deployment |

| Azure Data Factory | Raw data ingestion |

| Azure Databricks | PySpark transformation |

| Azure Blob Storage | Raw, staged and curated data storage |



\---



\## Security Considerations



Secrets are not hardcoded in the source code.



Local development uses `.env`.



Production deployment uses Azure App Service environment variables and Key Vault-ready configuration.



Required environment variables:



```env

MONGO\_URI=your\_mongodb\_connection\_string



AZURE\_OPENAI\_API\_KEY=your\_azure\_openai\_key

AZURE\_OPENAI\_ENDPOINT=https://your-resource-name.services.ai.azure.com/

AZURE\_OPENAI\_DEPLOYMENT=o4-mini

AZURE\_OPENAI\_API\_VERSION=2024-12-01-preview



AZURE\_SEARCH\_ENDPOINT=https://your-search-service.search.windows.net

AZURE\_SEARCH\_ADMIN\_KEY=your\_search\_admin\_key

AZURE\_SEARCH\_INDEX\_NAME=retail-knowledge-index



KEY\_VAULT\_URL=https://your-key-vault-name.vault.azure.net/

USE\_KEY\_VAULT=false

```



The `.env` file is ignored by Git using `.gitignore`.



\---



\## Data Engineering Pipeline



The data engineering pipeline follows:



```text

Landing → Raw → Staged → Curated

```



Tools used:



\- Azure Data Factory

\- Azure Databricks

\- PySpark

\- Spark SQL

\- Azure Blob Storage

\- Parquet



Pipeline layers:



| Layer | Description |

|---|---|

| Landing | Initial retail CSV file |

| Raw | Raw ingested data |

| Staged | Cleaned and transformed parquet data |

| Curated | Business-ready analytics data |

| SQL Analytics | Spark SQL output for reporting |

| Power BI | Final analytics dashboard |



\---



\## Power BI Dashboard



The Power BI report contains multiple pages.



\### Page 1: Smart Retail Overview



Shows:



\- Total sales

\- Average sales

\- Sales by category

\- Sales by region

\- Top products

\- Business insights



\### Page 2: ML \& Anomaly Insights



Shows:



\- Predicted sales

\- Actual vs predicted sales

\- Forecast error

\- Anomaly count

\- Anomaly trends

\- High-risk records



\### Page 3: AI Intelligence Hub



Shows:



\- Agent recommendations

\- Data pipeline flow

\- Azure cloud components

\- Project completion checklist

\- Deployment architecture summary



\---



\## Local Setup



\### 1. Clone the repository



```bash

git clone https://github.com/kirtisingh-001/smart-retail-ai-platform.git

cd smart-retail-ai-platform

```



\### 2. Create virtual environment



```bash

python -m venv venv

```



\### 3. Activate virtual environment



For Windows:



```bash

venv\\Scripts\\activate

```



\### 4. Install dependencies



```bash

pip install -r requirements.txt

```



\### 5. Add environment variables



Create a `.env` file using `.env.example`.



\### 6. Run the app locally



```bash

python -m uvicorn app.main:app --reload

```



Local Swagger URL:



```text

http://127.0.0.1:8000/docs

```



\---



\## Testing



Run all tests:



```bash

python -m pytest -v

```



Expected result:



```text

7 passed

```



\---



\## Deployment



The application is deployed using Azure App Service / Azure Web App.



\### Azure Startup Command



```bash

gunicorn -w 1 -k uvicorn.workers.UvicornWorker --timeout 600 --bind 0.0.0.0:8000 app.main:app

```



Alternative startup command:



```bash

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

```



\### Required Azure App Settings



```text

SCM\_DO\_BUILD\_DURING\_DEPLOYMENT=true

ENABLE\_ORYX\_BUILD=true

SCM\_COMMAND\_IDLE\_TIMEOUT=1800

WEBSITES\_PORT=8000

```



\### Live Application URLs



```text

Application:

https://smart-retail-api3-hkc0dsadcnfqcmaa.koreacentral-01.azurewebsites.net



Swagger:

https://smart-retail-api3-hkc0dsadcnfqcmaa.koreacentral-01.azurewebsites.net/docs



Health:

https://smart-retail-api3-hkc0dsadcnfqcmaa.koreacentral-01.azurewebsites.net/health

```



\---



\## Final Deployment Proof



For evaluation, the following screenshots should be attached:



1\. GitHub repository with clean project structure

2\. Azure App Service overview page

3\. Successful deployment log / GitHub Actions success

4\. Live `/health` API response

5\. Live Swagger `/docs` page

6\. Live `/ml/predict` response

7\. Live `/agent/chat` response

8\. Live `/azure-search/query` response

9\. Live `/pipeline/status` response

10\. Power BI dashboard pages

11\. Pytest result showing `7 passed`



\---



\## Project Structure



```text

smart-retail-ai-platform/

│

├── app/

│   ├── agents/

│   ├── database/

│   ├── mcp/

│   ├── models/

│   ├── rag/

│   ├── routes/

│   ├── services/

│   ├── utils/

│   └── main.py

│

├── data/

│   ├── raw/

│   └── processed/

│

├── ml/

│   ├── predict.py

│   ├── train.py

│   ├── sales\_model.pkl

│   ├── sales\_classifier.pkl

│   └── model\_metrics.txt

│

├── pipelines/

│   ├── adf\_pipeline\_steps.md

│   ├── databricks\_retail\_pipeline.py

│   ├── prepare\_retail\_orders.py

│   └── data\_engineering\_readme.md

│

├── scripts/

│   └── setup\_azure\_search.py

│

├── tests/

│   └── test\_api.py

│

├── requirements.txt

├── pytest.ini

├── README.md

├── .gitignore

└── Dockerfile

```



\---



\## Final Status



The Smart Retail AI Platform successfully integrates:



\- FastAPI backend

\- MongoDB database

\- ML prediction models

\- Multi-agent GenAI system

\- RAG knowledge retrieval

\- Azure OpenAI

\- Azure AI Search

\- Key Vault-ready security

\- Azure data pipeline

\- Power BI analytics

\- Azure deployment-ready backend APIs



The deployed application is ready for evaluation with live API execution through Swagger UI.

