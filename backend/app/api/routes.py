from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.models.schemas import QueryRequest
from app.services.orchestrator import process_user_query

router = APIRouter()


@router.post("/generate-report")
def generate_report(request: QueryRequest):
    try:
        result = process_user_query(request.question)
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return result


@router.get("/reports/{filename}")
def download_report(filename: str):
    report_path = Path(filename).name
    path = Path(report_path)

    if not path.exists():
        raise HTTPException(status_code=404, detail="Report not found")

    return FileResponse(
        path=path,
        media_type="application/pdf",
        filename=report_path,
    )
