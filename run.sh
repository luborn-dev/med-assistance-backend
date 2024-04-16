#!/bin/bash

echo "Starting FastAPI server..."
uvicorn app.main:app --reload
