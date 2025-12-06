#!/bin/bash

echo "📚 Downloading Test PDFs for AI Study Assistant"
echo "================================================"
echo ""

# Create test_pdfs directory
mkdir -p test_pdfs
cd test_pdfs

echo "1️⃣  Downloading AI Research Paper (Attention Is All You Need)..."
curl -L -o attention_paper.pdf "https://arxiv.org/pdf/1706.03762.pdf"
echo "✅ Downloaded: attention_paper.pdf (15 pages)"
echo ""

echo "2️⃣  Downloading Machine Learning Paper (Deep Learning)..."
curl -L -o deep_learning_nature.pdf "https://www.cs.toronto.edu/~hinton/absps/NatureDeepReview.pdf"
echo "✅ Downloaded: deep_learning_nature.pdf (9 pages)"
echo ""

echo "3️⃣  Downloading Python Tutorial..."
curl -L -o python_tutorial.pdf "https://www.tutorialspoint.com/python/python_tutorial.pdf"
echo "✅ Downloaded: python_tutorial.pdf (~300 pages)"
echo ""

echo "4️⃣  Downloading Statistics Textbook Sample..."
curl -L -o stats_sample.pdf "https://www.openintro.org/download.php?file=os4_tablet&referrer=/book/os/index.php"
echo "✅ Downloaded: stats_sample.pdf"
echo ""

echo "================================================"
echo "✅ All test PDFs downloaded!"
echo ""
echo "📁 Location: test_pdfs/"
echo ""
echo "Test PDFs:"
ls -lh
echo ""
echo "🚀 Now you can test the AI Study Assistant with these PDFs!"
echo "   Upload them at http://localhost:8501"
