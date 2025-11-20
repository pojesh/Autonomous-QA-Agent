from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class TestCaseRequest(BaseModel):
    query: str

class TestCase(BaseModel):
    test_id: str
    feature: str
    test_scenario: str
    expected_result: str
    test_type: str
    grounded_in: str

class ScriptRequest(BaseModel):
    test_case: Dict[str, Any]

class ScriptResponse(BaseModel):
    script: str
    test_id: str
