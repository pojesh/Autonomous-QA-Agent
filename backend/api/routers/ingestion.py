from fastapi import APIRouter, UploadFile, File, HTTPException, Header
from typing import List
from backend.services.ingestion_service import process_file
from backend.api.schemas.ingestion import IngestResponse
from backend.core.logging import logger

router = APIRouter()

@router.post("/upload", response_model=List[IngestResponse])
async def upload_documents(
    files: List[UploadFile] = File(...),
    x_session_id: str = Header(..., alias="X-Session-ID")
):
    logger.info(f"Received upload request for session: {x_session_id}")
    results = []
    for file in files:
        try:
            chunks_count = await process_file(file, x_session_id)
            results.append(IngestResponse(
                filename=file.filename,
                status="success",
                chunks_count=chunks_count,
                message="Successfully ingested"
            ))
        except Exception as e:
            logger.error(f"Failed to ingest {file.filename}: {str(e)}")
            results.append(IngestResponse(
                filename=file.filename,
                status="error",
                chunks_count=0,
                message=str(e)
            ))
    return results
