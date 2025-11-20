from pydantic import BaseModel
from typing import List, Optional

class IngestResponse(BaseModel):
    filename: str
    status: str
    chunks_count: int
    message: Optional[str] = None

class IngestRequest(BaseModel):
    # This might not be used directly if we use UploadFile, but good for reference
    pass
