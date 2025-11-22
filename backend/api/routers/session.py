import os
import shutil
from fastapi import APIRouter, HTTPException, Header
from backend.services.ingestion_service import get_vector_store
from backend.core.logging import logger

router = APIRouter()

@router.delete("/cleanup")
async def cleanup_session(x_session_id: str = Header(..., alias="X-Session-ID")):
    logger.info(f"Cleaning up session: {x_session_id}")
    try:
        # 1. Drop Milvus Collection
        collection_name = f"session_{x_session_id}"
        vector_store = get_vector_store(collection_name=collection_name)
        
        if vector_store.col:
            vector_store.col.drop()
            logger.info(f"Dropped collection: {collection_name}")
        else:
            logger.warning(f"Collection {collection_name} not found or already dropped")
            
        # 2. Delete Session Files
        session_dir = os.path.join("backend", "sessions", x_session_id)
        if os.path.exists(session_dir):
            shutil.rmtree(session_dir)
            logger.info(f"Deleted session directory: {session_dir}")
            
        return {"status": "success", "message": f"Session {x_session_id} cleaned up"}
            
    except Exception as e:
        logger.error(f"Failed to cleanup session {x_session_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
