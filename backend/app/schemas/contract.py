# backend/app/schemas/contract.py
from pydantic import BaseModel

class ContractResponse(BaseModel):
    task_id: str
    status: str