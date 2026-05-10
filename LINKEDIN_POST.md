# LinkedIn Post

I built an Enterprise AI Report Generator: a local GenAI application that turns natural-language business questions into answers and downloadable PDF reports.

The idea was simple:

What if a business user could ask:

"Generate a PDF report showing total revenue by region"

and the system could automatically:

- retrieve the right database schema using RAG
- understand the request with a local LLM
- generate safe SQL
- validate that only SELECT queries are allowed
- execute the query against MySQL
- produce a PDF report
- show the generated SQL for transparency

The stack:

- FastAPI for the backend
- Ollama for local LLM inference
- Llama 3.2 for chat and SQL generation
- Nomic Embed Text for embeddings
- Qdrant as the vector database
- MySQL for structured enterprise data
- ReportLab for PDF generation
- HTML, CSS, and JavaScript for the frontend
- Docker Compose for running the full stack locally

One design choice I focused on was separating normal chat from report generation. The assistant answers metadata and business-data questions normally, but it only creates SQL and a PDF when the user explicitly asks for a report. That keeps the workflow more predictable and safer.

I also added a SQL validation layer to block destructive statements like DELETE, DROP, UPDATE, INSERT, ALTER, and TRUNCATE. For this prototype, report queries are limited to SELECT statements.

This project helped me connect several important GenAI engineering patterns:

- RAG over structured metadata
- local model orchestration
- text-to-SQL generation
- SQL safety checks
- enterprise reporting automation
- full-stack Dockerized deployment

This is still a prototype, but the foundation can be extended with authentication, read-only database users, report history, charts, CSV/Excel export, and stronger SQL parsing.

GitHub repository:
[Add your repository link here]

#GenAI #ArtificialIntelligence #FastAPI #Ollama #RAG #Qdrant #MySQL #Python #Docker #TextToSQL #AIEngineering #MachineLearning
