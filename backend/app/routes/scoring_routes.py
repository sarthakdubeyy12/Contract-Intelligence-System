# backend/app/routes/scoring_routes.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict

router = APIRouter()

# Input model for scoring/gap analysis
class ContractAnalysisRequest(BaseModel):
    contract_text: str
    required_clauses: List[str]

# Output model
class ContractAnalysisResponse(BaseModel):
    score: float
    missing_clauses: List[str]
    details: Dict[str, bool]

@router.post("/analyze", response_model=ContractAnalysisResponse)
def analyze_contract(request: ContractAnalysisRequest):
    """
    Perform scoring + gap analysis on a contract.
    """
    # Simple scoring logic
    text = request.contract_text.lower()
    required = [c.lower() for c in request.required_clauses]

    found = {clause: (clause in text) for clause in required}
    missing = [clause for clause, present in found.items() if not present]

    score = (len(required) - len(missing)) / len(required) * 100 if required else 0

    return {
        "score": round(score, 2),
        "missing_clauses": missing,
        "details": found
    }