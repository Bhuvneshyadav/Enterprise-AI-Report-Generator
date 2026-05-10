# Enterprise AI Report Generator

An end-to-end enterprise data assistant that lets users ask natural-language business questions, retrieve relevant schema context with RAG, generate safe SQL for report requests, execute it against MySQL, and download the result as a PDF report.

The project is designed as a local, containerized GenAI application using Ollama, Qdrant, FastAPI, MySQL, and a lightweight web frontend.

## Features

- Natural-language chat interface for enterprise data questions
- Retrieval-Augmented Generation over schema metadata using Qdrant
- Local LLM inference with Ollama
- SQL generation for explicit report/PDF requests
- SQL safety validation that allows only `SELECT` queries
- MySQL-backed sample business data
- PDF report generation with tabular results
- Docker Compose setup for the full stack
- Simple frontend for asking questions and downloading generated reports

## Demo Flow

1. Ask a metadata question:

```text
What tables and columns are available?
```

2. Ask for a report:

```text
Generate a PDF report showing total revenue by region
```

3. The backend retrieves schema context, generates or selects a safe SQL query, executes it, creates `report.pdf`, and returns a download link.

## Architecture

```text
Frontend
  |
  | POST /generate-report
  v
FastAPI Backend
  |
  |-- RAG retrieval from Qdrant
  |-- Ollama chat and SQL generation
  |-- SQL validation
  |-- MySQL query execution
  |-- PDF generation with ReportLab
  v
Downloadable PDF Report
```

## Tech Stack

| Layer | Technology |
| --- | --- |
| Frontend | HTML, CSS, JavaScript, Nginx |
| Backend API | FastAPI, Uvicorn, Pydantic |
| LLM Runtime | Ollama |
| Chat Model | `llama3.2:latest` |
| Embedding Model | `nomic-embed-text` |
| Vector Database | Qdrant |
| SQL Database | MySQL 8 |
| ORM/SQL Access | SQLAlchemy, PyMySQL |
| Data Handling | Pandas |
| PDF Generation | ReportLab |
| Deployment | Docker Compose |

## Project Structure

```text
enterprise-ai-report-generator/
  backend/
    app/
      api/
        routes.py
      database/
        mysql.py
      models/
        schemas.py
      rag/
        embeddings.py
        ingestion.py
        retrieval.py
      reports/
        pdf_generator.py
      services/
        orchestrator.py
      sql_engine/
        executor.py
        generator.py
        validator.py
      config.py
      main.py
    ingest.py
    requirements.txt
    Dockerfile
  frontend/
    index.html
    app.js
    styles.css
    Dockerfile
  metadata/
    sales_schema.json
  mysql/
    init/
      01_schema.sql
  docker-compose.yml
  .env
  Readme.md
```

## How It Works

### 1. Metadata Retrieval

The backend stores schema metadata from `metadata/sales_schema.json` in Qdrant using Ollama embeddings.

When a user asks a question, the app retrieves the most relevant schema context and also merges it with the canonical metadata file so the model has reliable table and column information.

### 2. Chat Mode

For normal questions, the assistant answers using the retrieved metadata.

Example:

```text
What data can I ask about?
```

The response is returned as a chat answer without generating SQL or a PDF.

### 3. Report Mode

If the user explicitly asks for a report or PDF, the orchestrator switches to report mode.

Report trigger examples include:

- `generate report`
- `create report`
- `pdf report`
- `generate pdf`
- `download pdf`

The app then generates SQL, validates it, executes it against MySQL, and creates a PDF.

### 4. SQL Safety

The SQL validator blocks destructive operations such as:

- `DELETE`
- `DROP`
- `UPDATE`
- `INSERT`
- `ALTER`
- `TRUNCATE`

Only `SELECT` queries are allowed.

## Sample Data

The MySQL container is initialized with two tables:

### `sales`

| Column | Description |
| --- | --- |
| `id` | Primary key |
| `region` | Sales region |
| `product` | Product name |
| `revenue` | Revenue amount |
| `sale_date` | Date of sale |

### `employees`

| Column | Description |
| --- | --- |
| `id` | Primary key |
| `department` | Employee department |
| `salary` | Employee salary |

## Prerequisites

Install the following:

- Docker
- Docker Compose

No external AI API key is required because the project runs local models through Ollama.

## Environment Variables

Create a `.env` file in the project root:

```env
OLLAMA_HOST=http://ollama:11434
OLLAMA_MODEL=llama3.2:latest
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
OLLAMA_EMBEDDING_DIMENSIONS=768
MYSQL_URL=mysql+pymysql://root:password@mysql:3306/companydb
QDRANT_HOST=qdrant
QDRANT_PORT=6333
METADATA_FILE=/metadata/sales_schema.json
```

## Run Locally With Docker

From the project root, start the full stack:

```bash
docker compose up --build
```

Docker Compose starts:

- Frontend on `http://localhost:3000`
- Backend on `http://localhost:8000`
- Ollama on `http://localhost:11434`
- Qdrant on `http://localhost:6333`
- MySQL on `localhost:3306`

During startup, the `ollama-init` service pulls:

- `llama3.2:latest`
- `nomic-embed-text:latest`

The first run can take a while because model downloads are large.

## Using the App

Open the frontend:

```text
http://localhost:3000
```

Try these prompts:

```text
What tables and columns are available?
```

```text
What reports can be generated from this data?
```

```text
Generate a PDF report showing total revenue by region
```

When a report is generated, the UI displays the SQL query and an `Open PDF` link.

## API Endpoints

### Health Check

```http
GET /
```

Response:

```json
{
  "message": "AI Report Generator Running"
}
```

### Generate Chat Answer or Report

```http
POST /generate-report
Content-Type: application/json
```

Request:

```json
{
  "question": "Generate a PDF report showing total revenue by region"
}
```

Report response:

```json
{
  "mode": "report",
  "answer": "PDF report generated successfully.",
  "sql_query": "SELECT region, SUM(revenue) AS total_revenue FROM sales GROUP BY region ORDER BY total_revenue DESC",
  "pdf_path": "report.pdf"
}
```

Chat response:

```json
{
  "mode": "chat",
  "answer": "The available tables are sales and employees...",
  "metadata": [],
  "sql_query": null,
  "pdf_path": null
}
```

### Download Report

```http
GET /reports/{filename}
```

Example:

```text
http://localhost:8000/reports/report.pdf
```

## Manual Backend Setup

Docker Compose is the recommended setup. For manual backend development:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You still need Ollama, Qdrant, and MySQL running, and your `.env` values must point to those services.

## Manual Metadata Ingestion

The app automatically ensures the Qdrant metadata collection exists during retrieval. You can also ingest manually:

```bash
cd backend
python ingest.py
```

## Example Generated SQL

For:

```text
Generate a PDF report showing total revenue by region
```

The app uses:

```sql
SELECT region, SUM(revenue) AS total_revenue
FROM sales
GROUP BY region
ORDER BY total_revenue DESC
```

## Troubleshooting

### Ollama model download is slow

The first run downloads local models. Keep Docker running until `ollama-init` completes.

### Backend returns a model connection error

Check that `OLLAMA_HOST` is correct.

Inside Docker Compose, use:

```env
OLLAMA_HOST=http://ollama:11434
```

For a backend running directly on your host machine, use something like:

```env
OLLAMA_HOST=http://localhost:11434
```

### MySQL connection fails

Make sure the MySQL container is healthy:

```bash
docker compose ps
```

The default connection string is:

```env
MYSQL_URL=mysql+pymysql://root:password@mysql:3306/companydb
```

### Qdrant collection mismatch

If you change the embedding model or embedding dimensions, restart the services so the metadata collection can be recreated.

```bash
docker compose down
docker compose up --build
```

## Roadmap

- Add authentication and role-based access control
- Support multiple enterprise datasets
- Improve PDF formatting with charts and summaries
- Add report history and persistent storage
- Add export options such as CSV and Excel
- Add stronger SQL parsing and column-level validation
- Add automated tests for API, SQL validation, and report generation

## Security Notes

This project is a local prototype. Before using it with production data:

- Add authentication
- Restrict database privileges to read-only access
- Store generated reports securely
- Add audit logging
- Validate generated SQL with a production-grade parser
- Avoid exposing internal schema metadata to unauthorized users

## License

This project is available for learning, experimentation, and portfolio use. Add a license file before publishing if you want to define reuse terms clearly.

## Author

Built as a GenAI full-stack project demonstrating local LLMs, RAG, SQL generation, and automated enterprise reporting.
