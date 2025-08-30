# backend/test_parse_contract.py
import sys
import os

# Add app and worker folders to sys.path so imports work
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(base_dir, "app"))
sys.path.append(os.path.join(base_dir, "worker"))

from app.core.celery_app import celery_app as app  # import Celery app

# Path to your sample contract PDF
contract_path = "/Users/sarthakdubey/TechAssignment/sample_contract.pdf"
contract_name = "sample_contract"

# Send task to Celery
result = app.send_task("parse_contract", args=[contract_path, contract_name])

print("Task sent, waiting for result...")

# Get the result (with timeout in seconds)
try:
    output = result.get(timeout=60)  # increase timeout if parsing is slow
    print("Result:", output)
except Exception as e:
    print("Error getting task result:", e)