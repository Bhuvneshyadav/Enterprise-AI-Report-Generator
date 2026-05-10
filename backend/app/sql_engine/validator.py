import json
import re

FORBIDDEN = [
    "DELETE",
    "DROP",
    "UPDATE",
    "INSERT",
    "ALTER",
    "TRUNCATE"
]

BAD_REPORT_PATTERNS = [
    "CONCAT(",
    "GROUP_CONCAT(",
]


def validate_sql(query: str, metadata_context: list | None = None):
    upper_query = query.upper()

    for keyword in FORBIDDEN:
        if keyword in upper_query:
            raise Exception(f"Forbidden SQL detected: {keyword}")

    if not upper_query.strip().startswith("SELECT"):
        raise Exception("Only SELECT queries are allowed")

    for pattern in BAD_REPORT_PATTERNS:
        if pattern in upper_query:
            raise Exception(
                f"Report SQL should return tabular columns. Avoid {pattern.rstrip('(')}."
            )

    if metadata_context:
        allowed_tables = extract_allowed_tables(metadata_context)
        referenced_tables = extract_referenced_tables(query)
        unknown_tables = referenced_tables - allowed_tables

        if unknown_tables:
            allowed = ", ".join(sorted(allowed_tables))
            unknown = ", ".join(sorted(unknown_tables))
            raise Exception(
                f"Unknown table(s): {unknown}. Allowed tables are: {allowed}"
            )

    return True


def extract_allowed_tables(metadata_context: list):
    tables = set()

    for item in metadata_context:
        try:
            metadata = json.loads(item) if isinstance(item, str) else item
        except json.JSONDecodeError:
            continue

        table = metadata.get("table")
        if table:
            tables.add(table.lower())

    return tables


def extract_referenced_tables(query: str):
    matches = re.findall(r"\b(?:FROM|JOIN)\s+`?([a-zA-Z_][a-zA-Z0-9_]*)`?", query, re.IGNORECASE)
    return {match.lower() for match in matches}
