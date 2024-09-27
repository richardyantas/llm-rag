# llm-rag

This project consist on implement a RAG system that consume data from a document `documento.pdf` and vectorize it using
chromadb and also consume it by similarities using and API implemented using FastApi.

## 1.To run the project in the development mode use:
- create an environment: `make conda-create` then, execute`conda activate llm-rag`
- create the binaries: `python data-ingestion.py`
- Testing the scripts: `make test`
- Run the api: `uvicorn app.app.main:app --host 0.0.0.0 --port 8000 --reload`

## 2. To run the project in docker container use:
- Execute docker using: `docker compose up --build`

For testing the project either using option 1 or 2, use the following code.

# test FastAPI
`curl -X POST "http://localhost:8000/query" -H "Content-Type: application/json" -d '{"query": "¿quien es zara?"}' `
`curl -X POST "http://localhost:8000/query" -H "Content-Type: application/json" -d '{"query": "O que Zara está fazendo?"}' `
`curl -X POST "http://localhost:8000/query" -H "Content-Type: application/json" -d '{"query": "¿who is zara"}' `

