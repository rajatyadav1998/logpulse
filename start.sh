#!/bin/bash

# Run the database initialization script
echo "Running database initializations..."
python init_db.py

# Start the Uvicorn server
echo "Starting Uvicorn server..."
uvicorn main:app --host 0.0.0.0 --port 8000