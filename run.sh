#!/bin/bash

echo "================================================"
echo "Starting PDF RAG Reader"
echo "================================================"
echo ""

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "🚀 Starting Ollama..."
    ollama serve &
    sleep 3
fi

echo "✅ Ollama is running"
echo ""
echo "🌐 Starting Streamlit app..."
echo "Opening browser at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop"
echo ""

streamlit run app.py
