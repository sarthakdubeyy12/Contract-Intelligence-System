from fastapi import APIRouter, HTTPException
from app.services.scoring_service import ContractScoringService

router = APIRouter(prefix="/contracts", tags=["Contracts"])

scoring_service = ContractScoringService()

@router.post("/score")
def score_contract(payload: dict):
    """
    API endpoint to score a parsed contract.
    Expects JSON like:
    {
        "clauses": ["termination", "confidentiality", "payment_terms"]
    }
    """
    try:
        result = scoring_service.score_contract(payload)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))