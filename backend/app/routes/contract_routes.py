from fastapi import APIRouter, UploadFile, File
import tempfile
import shutil
from app.services.parsing_service import parse_contract_pdf

router = APIRouter()

@router.post("/parse-pdf")
async def parse_pdf_contract(file: UploadFile = File(...)):
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    # Run parsing
    result = parse_contract_pdf(tmp_path)

    return {"status": "success", "data": result}