import json
from urllib import request
from app.config import settings


def ask_ollama(messages: list, temperature: float = 0.2):
    payload = {
        "model": settings.OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
        "options": {"temperature": temperature},
    }

    req = request.Request(
        f"{settings.OLLAMA_HOST.rstrip('/')}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with request.urlopen(req, timeout=120) as response:
        data = json.loads(response.read().decode("utf-8"))

    return data["message"]["content"].strip()


def generate_sql(question: str, metadata_context: list):
    schema_rules = build_schema_rules(metadata_context)
    prompt = f"""
You are an enterprise SQL assistant.

Use ONLY the database schema below. Do not invent tables or columns.
If the requested report cannot be created from this schema, return:
SELECT 'Requested report cannot be generated from available schema' AS message;

Available schema:
{schema_rules}

Generate ONLY one safe MySQL SELECT query.
Return tabular report data with column aliases.
Do not use CONCAT, GROUP_CONCAT, or string-building expressions.
Do not include Markdown, code fences, explanations, or comments.

User Question:
{question}
"""

    return clean_sql(
        ask_ollama(
            [
                {"role": "system", "content": "Generate safe SQL queries."},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )
    )


def regenerate_sql_with_feedback(question: str, metadata_context: list, previous_sql: str, feedback: str):
    schema_rules = build_schema_rules(metadata_context)
    prompt = f"""
The previous SQL was invalid:
{previous_sql}

Problem:
{feedback}

Use ONLY this schema:
{schema_rules}

Generate a corrected MySQL SELECT query only.
Return tabular report data with column aliases.
Do not use CONCAT, GROUP_CONCAT, or string-building expressions.
Do not include Markdown, code fences, explanations, or comments.

User Question:
{question}
"""

    return clean_sql(
        ask_ollama(
            [
                {"role": "system", "content": "Correct invalid SQL using only the provided schema."},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )
    )


def build_schema_rules(metadata_context: list):
    lines = []

    for item in metadata_context:
        try:
            metadata = json.loads(item) if isinstance(item, str) else item
        except json.JSONDecodeError:
            lines.append(str(item))
            continue

        table = metadata.get("table")
        columns = metadata.get("columns", {})
        column_names = ", ".join(columns.keys())
        lines.append(f"table: {table}; columns: {column_names}")

    return "\n".join(lines)


def generate_answer(question: str, metadata_context: list):
    prompt = f"""
You are an enterprise data assistant.

Use the schema metadata below when the question is about available data,
tables, columns, or possible reports. If the user asks for a PDF report,
do not generate SQL here; tell them to ask explicitly for a report.

Metadata:
{metadata_context}

User Question:
{question}
"""

    return ask_ollama(
        [
            {
                "role": "system",
                "content": "Answer clearly and concisely. Do not claim a PDF was generated unless one was requested.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )


def clean_sql(content: str):
    sql = content.strip()

    if sql.startswith("```"):
        lines = sql.splitlines()
        if lines:
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        sql = "\n".join(lines).strip()

    return sql
