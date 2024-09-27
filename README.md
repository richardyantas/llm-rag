# llm-rag

This project consist on implement a RAG system that consume data from a document `documento.pdf` and vectorize it using
chromadb and also consume it by similarities using and API implemented using FastApi.

To run the project use:

- from docker container 
`docker compose up --build`

or 
- locally without docker, this implies to use a conda environment that is executed using
`make conda-create`
then, execute`conda activate llm-rag`

for testing the scripts
`make test`

To run the api:

`uvicorn app.app.main:app --host 0.0.0.0 --port 8000 --reload`

For testing the project, use the allow code.

# test FastAPI
`curl -X POST "http://localhost:8000/query" -H "Content-Type: application/json" -d '{"query": "¿quien es zara?"}' `

