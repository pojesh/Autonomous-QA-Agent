from fastapi import APIRouter, HTTPException, Header
from typing import List
from backend.services.rag_service import generate_test_cases, generate_selenium_script
from backend.api.schemas.generation import TestCaseRequest, TestCase, ScriptRequest, ScriptResponse
from backend.core.logging import logger

router = APIRouter()

@router.post("/test-cases", response_model=List[TestCase])
async def create_test_cases(
    request: TestCaseRequest,
    x_session_id: str = Header(..., alias="X-Session-ID")
):
    try:
        test_cases = await generate_test_cases(request.query, x_session_id)
        return test_cases
    except Exception as e:
        logger.error(f"Failed to generate test cases: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/script", response_model=ScriptResponse)
async def create_script(
    request: ScriptRequest,
    x_session_id: str = Header(..., alias="X-Session-ID")
):
    try:
        script = await generate_selenium_script(request.test_case, x_session_id)
        return ScriptResponse(
            script=script,
            test_id=request.test_case.get("test_id", "unknown")
        )
    except Exception as e:
        logger.error(f"Failed to generate script: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
