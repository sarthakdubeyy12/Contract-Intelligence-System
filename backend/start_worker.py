#!/usr/bin/env python3
"""
Script to start a Celery worker locally for development.
Run this in a separate terminal while your FastAPI server is running.
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.celery_app import celery_app

if __name__ == "__main__":
    print("Starting Celery worker...")
    print("Make sure Redis is running on localhost:6379")
    print("Press Ctrl+C to stop the worker")
    
    # Start the worker
    celery_app.worker_main([
        'worker',
        '--loglevel=info',
        '--queues=contracts',
        '--hostname=worker1@localhost'
    ]) 