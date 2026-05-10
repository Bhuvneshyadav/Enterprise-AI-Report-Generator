from app.rag.retrieval import retrieve_metadata
from app.sql_engine.generator import generate_answer, generate_sql, regenerate_sql_with_feedback
from app.sql_engine.validator import validate_sql
from app.sql_engine.executor import execute_query
from app.reports.pdf_generator import generate_pdf


REPORT_KEYWORDS = [
    "generate report",
    "create report",
    "make report",
    "build report",
    "report pdf",
    "pdf report",
    "generate pdf",
    "create pdf",
    "make pdf",
    "download pdf",
]


def process_user_query(question: str):

    metadata = retrieve_metadata(question)

    if not should_generate_report(question):
        answer = generate_answer(question, metadata)

        return {
            "mode": "chat",
            "answer": answer,
            "metadata": metadata,
            "sql_query": None,
            "pdf_path": None,
        }

    sql_query, df = generate_and_execute_report_query(question, metadata)

    pdf_path = generate_pdf(df)

    return {
        "mode": "report",
        "answer": "PDF report generated successfully.",
        "sql_query": sql_query,
        "pdf_path": pdf_path
    }


def should_generate_report(question: str):
    normalized_question = question.lower()
    return any(keyword in normalized_question for keyword in REPORT_KEYWORDS)


def generate_and_execute_report_query(question: str, metadata: list):
    sql_query = get_known_report_query(question) or generate_sql(question, metadata)
    last_error = None

    for _ in range(3):
        try:
            validate_sql(sql_query, metadata)
            return sql_query, execute_query(sql_query)
        except Exception as error:
            last_error = error
            sql_query = regenerate_sql_with_feedback(
                question,
                metadata,
                sql_query,
                str(error),
            )

    raise Exception(
        "Could not generate a valid report query from the available schema. "
        f"Last error: {last_error}"
    )


def get_known_report_query(question: str):
    normalized_question = question.lower()

    if "revenue" in normalized_question and "region" in normalized_question:
        return (
            "SELECT region, SUM(revenue) AS total_revenue "
            "FROM sales "
            "GROUP BY region "
            "ORDER BY total_revenue DESC"
        )

    return None
