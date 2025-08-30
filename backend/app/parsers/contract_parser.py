# backend/app/parsers/contract_parser.py
import time
from celery import shared_task

@shared_task(name="parse_contract_task")
def parse_contract_task(file_path: str, file_id: str):
    """
    Dummy contract parser task.
    Simulates parsing a contract file and extracting key metadata.
    """

    # Simulate processing time
    time.sleep(5)

    # Dummy structured result (replace with real parsing later)
    parsed_result = {
        "file_id": file_id,
        "file_path": file_path,
        "status": "parsed",
        "extracted_fields": {
            "party_a": "Alice Johnson",
            "party_b": "Tech Solutions Pvt Ltd",
            "effective_date": "2025-01-01",
            "expiry_date": "2026-01-01",
            "contract_value": "₹10,00,000"
        }
    }

    return parsed_result