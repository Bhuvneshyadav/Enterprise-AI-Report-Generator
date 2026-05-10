import pandas as pd
from sqlalchemy import text
from app.database.mysql import engine


def execute_query(query: str):
    with engine.connect() as conn:
        result = conn.execute(text(query))
        rows = result.fetchall()
        columns = result.keys()

    df = pd.DataFrame(rows, columns=columns)

    return df