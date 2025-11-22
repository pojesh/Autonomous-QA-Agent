#!/bin/bash

echo "Starting Backend..."
# Run backend in a new terminal window
gnome-terminal -- bash -c "uvicorn backend.main:app --reload --port 8000; exec bash"

echo "Starting Frontend..."
# Run frontend in the current terminal
streamlit run frontend/app.py
