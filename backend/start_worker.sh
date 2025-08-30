#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Start Celery worker
echo "Starting Celery worker..."
echo "Make sure Redis is running on localhost:6379"
echo "Press Ctrl+C to stop the worker"

celery -A app.core.celery_app worker --loglevel=info --queues=contracts 