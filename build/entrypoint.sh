#!/bin/bash

# Run the FastAPI server
uvicorn main:app --host 0.0.0.0 --port 8080

exit 0