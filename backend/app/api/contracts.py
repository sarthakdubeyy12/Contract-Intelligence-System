# backend/app/api/contracts.py
import os
import uuid
import sys
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from celery.result import AsyncResult
from app.core.celery_app import celery_app
from typing import List, Dict, Any

# Add worker directory to path using absolute path
project_root = "/Users/sarthakdubey/TechAssignment"
worker_dir = os.path.join(project_root, "worker")
if worker_dir not in sys.path:
    sys.path.insert(0, worker_dir)

from contract_parser import parse_contract

router = APIRouter()

UPLOAD_DIR = "uploaded_contracts"
# Use absolute path for results directory
RESULTS_DIR = os.path.join(project_root, "results")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)


@router.post("/upload")
async def upload_contract(file: UploadFile = File(...)):
    """
    Upload a contract file and trigger async parsing with Celery.
    """
    # Generate unique ID for file
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

    # Save file to disk
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Trigger async Celery task using the correct task name
    task = celery_app.send_task("parse_contract", args=[file_path, file_id])

    return {"task_id": task.id, "file_id": file_id, "status": "processing"}


@router.get("/status/{task_id}")
def get_task_status(task_id: str):
    """
    Check the status and result of a Celery task.
    """
    task_result = AsyncResult(task_id, app=celery_app)

    if task_result.state == "PENDING":
        return {"task_id": task_id, "status": "pending"}
    elif task_result.state == "STARTED":
        return {"task_id": task_id, "status": "in_progress"}
    elif task_result.state == "SUCCESS":
        return {
            "task_id": task_id,
            "status": "completed",
            "result": task_result.result
        }
    elif task_result.state == "FAILURE":
        return {
            "task_id": task_id,
            "status": "failed",
            "error": str(task_result.result)
        }
    else:
        return {"task_id": task_id, "status": task_result.state}


@router.get("/{contract_id}")
def get_contract(contract_id: str):
    """
    Fetch parsed JSON data for a specific contract.
    """
    # Look for the contract result in the results folder
    result_file_path = os.path.join(RESULTS_DIR, f"{contract_id}.json")
    
    if not os.path.exists(result_file_path):
        raise HTTPException(status_code=404, detail="Contract not found or not yet processed")
    
    try:
        import json
        with open(result_file_path, 'r') as f:
            contract_data = json.load(f)
        return {
            "contract_id": contract_id,
            "data": contract_data,
            "result_file": result_file_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading contract data: {str(e)}")


@router.get("/")
def list_contracts():
    """
    List all uploaded contracts with their status.
    """
    contracts = []
    
    # Get all uploaded files
    if os.path.exists(UPLOAD_DIR):
        for filename in os.listdir(UPLOAD_DIR):
            if filename.endswith('.pdf'):
                # Extract contract_id from filename (format: {contract_id}_{original_filename})
                parts = filename.split('_', 1)
                if len(parts) == 2:
                    contract_id = parts[0]
                    original_filename = parts[1]
                    
                    # Check if result exists
                    result_file_path = os.path.join(RESULTS_DIR, f"{contract_id}.json")
                    status = "processed" if os.path.exists(result_file_path) else "pending"
                    
                    contracts.append({
                        "contract_id": contract_id,
                        "original_filename": original_filename,
                        "status": status,
                        "uploaded_at": os.path.getctime(os.path.join(UPLOAD_DIR, filename))
                    })
    
    return {
        "total_contracts": len(contracts),
        "contracts": contracts
    }


@router.get("/{contract_id}/download")
def download_contract(contract_id: str):
    """
    Download the original PDF file for a specific contract.
    """
    # Find the contract file in the uploaded_contracts directory
    contract_file = None
    if os.path.exists(UPLOAD_DIR):
        for filename in os.listdir(UPLOAD_DIR):
            if filename.startswith(f"{contract_id}_"):
                contract_file = filename
                break
    
    if not contract_file:
        raise HTTPException(status_code=404, detail="Contract file not found")
    
    file_path = os.path.join(UPLOAD_DIR, contract_file)
    
    # Return the file as a download
    return FileResponse(
        path=file_path,
        filename=contract_file,
        media_type='application/pdf'
    )