from pydantic import BaseModel
from typing import Optional

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    mode: str
    answer: str
    sql_query: Optional[str] = None
    pdf_path: Optional[str] = None
