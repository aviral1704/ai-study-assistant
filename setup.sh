#!/bin/bash

echo "================================================"
echo "PDF RAG Reader - Setup Script"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama is not installed."
    echo ""
    echo "Please install Ollama:"
    echo "  macOS: brew install ollama"
    echo "  Linux: curl -fsSL https://ollama.com/install.sh | sh"
    echo "  Windows: Download from https://ollama.com/download"
    echo ""
    read -p "Press Enter after installing Ollama..."
fi

echo "✅ Ollama found"
echo ""

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "🤖 Pulling AI model (llama2)..."
echo "This may take a few minutes..."
ollama pull llama2

if [ $? -eq 0 ]; then
    echo "✅ Model downloaded successfully"
else
    echo "⚠️  Failed to download model. You can try manually: ollama pull llama2"
fi

echo ""
echo "================================================"
echo "✅ Setup Complete!"
echo "================================================"
echo ""
echo "To start the app:"
echo "  1. Make sure Ollama is running: ollama serve"
echo "  2. Run the app: streamlit run app.py"
echo ""
echo "The app will open in your browser at http://localhost:8501"
echo ""
