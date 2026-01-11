from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ContextDoc(BaseModel):
    id: str
    text: str

class AnalysisRequest(BaseModel):
    prompt: str
    context_docs: List[ContextDoc] = []
    metadata: Dict[str, Any] = {}

class AnalysisResponse(BaseModel):
    decision: str = Field(..., description="allow | block | transform")
    risk_score: int
    risk_tags: List[str]
    sanitized_prompt: Optional[str] = None
    sanitized_context_docs: List[ContextDoc] = []
    reasons: List[Dict[str, Any]] = []

class PolicyResponse(BaseModel):
    version: str
    detectors: List[str]
    thresholds: Dict[str, int]