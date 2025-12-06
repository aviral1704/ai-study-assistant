# 🚀 Quick Start Guide

Get your PDF RAG Reader running in 5 minutes!

## Step 1: Install Ollama

### macOS
```bash
brew install ollama
```

### Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Windows
Download from: https://ollama.com/download

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Or use the setup script:
```bash
chmod +x setup.sh
./setup.sh
```

## Step 3: Start Ollama

In a terminal:
```bash
ollama serve
```

## Step 4: Pull AI Model

In another terminal:
```bash
ollama pull llama2
```

## Step 5: Run the App

```bash
streamlit run app.py
```

Or use the run script:
```bash
chmod +x run.sh
./run.sh
```

## Step 6: Use the App

1. Open browser at `http://localhost:8501`
2. Upload a PDF file
3. Click "Load & Process PDF"
4. Start analyzing!

## 🎯 First Time Usage

1. **Upload a small PDF** (5-10 pages) to test
2. Try "Full Book Summary" first
3. Ask a simple question in Q&A tab
4. Explore other features

## ⚡ Quick Commands

```bash
# Install everything
./setup.sh

# Run the app
./run.sh

# Or manually
ollama serve &
streamlit run app.py
```

## 🐛 Common Issues

### "Connection refused"
```bash
# Make sure Ollama is running
ollama serve
```

### "Model not found"
```bash
# Pull the model
ollama pull llama2
```

### "Module not found"
```bash
# Install dependencies
pip install -r requirements.txt
```

## 💡 Tips

- Use **llama2** for best results
- Start with small PDFs (<20 pages)
- Wait for processing to complete
- Check Ollama is running if errors occur

## 🎉 You're Ready!

Start analyzing PDFs and earning money! 💰

For detailed documentation, see README.md
