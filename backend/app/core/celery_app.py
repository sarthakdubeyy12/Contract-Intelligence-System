# backend/app/core/celery_app.py
from celery import Celery
import os
import sys

# Add the worker directory to the path (going up from backend/app/core to TechAssignment/worker)
current_dir = os.path.dirname(os.path.abspath(__file__))  # backend/app/core
backend_dir = os.path.dirname(os.path.dirname(current_dir))  # backend
project_root = os.path.dirname(backend_dir)  # TechAssignment
worker_dir = os.path.join(project_root, "worker")
sys.path.insert(0, worker_dir)

# Redis URL
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "worker",
    broker=redis_url,
    backend=redis_url,
    include=['tasks']
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_routes={
        "parse_contract": {"queue": "contracts"},
    }
)

# Import the tasks so Celery registers them
# The tasks will be imported from the worker directory due to sys.path modification above