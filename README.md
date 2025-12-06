# 🎓 AI Study Assistant - The Ultimate PDF Learning Companion

> **Transform any PDF into your personal AI tutor. Study smarter, learn faster, ace your exams.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)

## 🌟 What Makes This Special?

This isn't just another PDF reader. It's a **complete AI-powered learning system** that:

- 📚 **Handles MASSIVE PDFs** - Process textbooks up to 5000+ pages
- 🤖 **Real-Time Web Search** - Combines PDF content with current web knowledge
- 🎯 **Personalized Learning** - Adapts to your study style and tracks progress
- 🗣️ **Voice Interaction** - Ask questions and listen to summaries hands-free
- 📊 **Progress Tracking** - Monitor your learning journey with detailed analytics
- 🎴 **Smart Flashcards** - Spaced repetition for optimal memorization
- 📝 **Practice Exams** - Auto-generate realistic practice tests
- 💾 **Export Everything** - Save notes in PDF, DOCX, Markdown formats
- 🔒 **100% Private** - Everything runs locally on your computer
- 🆓 **Completely Free** - No subscriptions, no limits, forever

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Ollama (AI Engine)

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Download from [ollama.com/download](https://ollama.com/download)

### Step 2: Download AI Model

```bash
ollama pull llama2
```

This downloads the AI model (about 3.8GB). Do this once.

### Step 3: Clone & Install

```bash
# Clone the repository
git clone https://github.com/aviral1704/ai-study-assistant.git
cd ai-study-assistant

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Run the App

```bash
# Start Ollama (in one terminal)
ollama serve

# Start the app (in another terminal)
streamlit run app.py
```

**That's it!** Open your browser at `http://localhost:8501` 🎉

## 📖 Complete Installation Guide

### Prerequisites

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **8GB RAM minimum** (16GB recommended for large PDFs)
- **5GB free disk space** (for AI models and cache)
- **Internet connection** (for initial setup and web search features)

### Detailed Installation Steps

#### 1. Install Python (if not already installed)

**Check if Python is installed:**
```bash
python3 --version
```

If not installed:
- **macOS**: `brew install python3`
- **Linux**: `sudo apt-get install python3 python3-pip`
- **Windows**: Download from [python.org](https://www.python.org/downloads/)

#### 2. Install Ollama

Ollama runs the AI models locally on your computer.

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
1. Download installer from [ollama.com/download](https://ollama.com/download)
2. Run the installer
3. Restart your computer

**Verify installation:**
```bash
ollama --version
```

#### 3. Download AI Models

```bash
# Recommended: llama2 (best accuracy)
ollama pull llama2

# Alternative: mistral (faster)
ollama pull mistral

# Lightweight: phi (for older computers)
ollama pull phi
```

**Model Comparison:**
| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| llama2 | 3.8GB | Medium | Excellent | Detailed studying |
| mistral | 4.1GB | Fast | Very Good | Quick reviews |
| phi | 1.6GB | Very Fast | Good | Older computers |

#### 4. Clone Repository

```bash
git clone https://github.com/aviral1704/ai-study-assistant.git
cd ai-study-assistant
```

#### 5. Install Python Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**If you encounter errors:**
```bash
# Update pip first
pip install --upgrade pip

# Install dependencies one by one
pip install streamlit langchain langchain-community langchain-ollama
pip install pypdf faiss-cpu sentence-transformers torch transformers
pip install duckduckgo-search wikipedia
```

#### 6. Start the Application

**Option A: Using Scripts (Easiest)**
```bash
# Make scripts executable
chmod +x setup.sh run.sh

# Run setup (first time only)
./setup.sh

# Start the app
./run.sh
```

**Option B: Manual Start**
```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start Streamlit
streamlit run app.py
```

**Option C: Background Mode**
```bash
# Start Ollama in background
ollama serve &

# Start Streamlit
streamlit run app.py --server.headless true
```

## 🎯 How to Use

### First Time Setup

1. **Open the app** at `http://localhost:8501`
2. **Upload a PDF** using the sidebar
3. **Select AI model** (llama2 recommended)
4. **Click "Load & Process PDF"**
5. **Wait 1-5 minutes** (depending on PDF size)
6. **Start studying!**

### Features Guide

#### 📚 Summaries

**Full Book Summary:**
- Get comprehensive 800-1200 word overview
- Includes themes, arguments, and key takeaways
- Perfect for understanding the big picture

**Chapter Summaries:**
- Detailed 600-900 word analysis per chapter
- Key concepts with definitions
- Study points for exams

**Page Summaries:**
- Analyze specific pages or ranges
- Quick reviews of sections
- Focused studying

**How to use:**
1. Go to "Summaries" tab
2. Choose summary type
3. Customize detail level
4. Click "Generate"
5. Download as TXT, MD, or PDF

#### ❓ Smart Q&A

**Ask Anything:**
- Type any question about your PDF
- Get detailed answers with examples
- See source page citations

**Quick Questions:**
- "What's the main idea?"
- "Key concepts?"
- "Exam tips?"

**Web-Enhanced Answers:**
- Combines PDF content with real-time web search
- Gets current information
- Provides comprehensive context

**How to use:**
1. Go to "Q&A" tab
2. Type your question
3. Choose answer style (Detailed/Concise/ELI5)
4. Enable "Show sources" for citations
5. Click "Get Answer"

#### 🎯 Study Questions & Practice

**Practice Questions:**
- Generate 5-30 questions with detailed answers
- Choose difficulty: Easy, Medium, Hard, Mixed
- Track which questions you've mastered
- Get hints and related concepts

**Practice Exams:**
- Full exams with multiple question types
- Multiple choice, short answer, essay, true/false
- Set time limits
- Realistic exam simulation

**Flashcards:**
- Auto-generate flashcards from key concepts
- Spaced repetition for optimal learning
- Track mastery progress

**Quick Quiz:**
- 5-minute knowledge tests
- Instant feedback
- Perfect for quick reviews

**How to use:**
1. Go to "Study Questions" tab
2. Choose study mode
3. Set number of questions and difficulty
4. Click "Generate"
5. Practice and track progress

#### 📚 Study Tools

**Key Concepts Glossary:**
- Extract 15-25 important terms
- Detailed definitions with examples
- Context and connections
- Perfect for flashcards

**Complete Study Guide:**
- Comprehensive exam prep guide
- All major themes and concepts
- Important facts and figures
- Exam preparation tips
- Downloadable

**Explain Any Concept:**
- Get detailed explanations of specific topics
- Simple definitions + thorough explanations
- Real-world examples
- Common misconceptions
- Study tips

**Compare Concepts:**
- Side-by-side comparisons
- Similarities and differences
- When to use each
- Exam tips for distinguishing

**How to use:**
1. Go to "Study Tools" tab
2. Choose tool type
3. Enter concept names (if needed)
4. Click "Generate"
5. Download or save

#### 💬 Chat Mode

**Natural Conversation:**
- Chat naturally about your PDF
- Ask follow-up questions
- Build on previous answers
- Like having a tutor

**Chat History:**
- See all previous Q&A
- Reference earlier discussions
- Export conversations

**How to use:**
1. Go to "Chat" tab
2. Type your message
3. Get instant responses
4. Continue the conversation

### Advanced Features

#### 🌐 Real-Time Web Search

Enable web search to get:
- Current information
- Latest research
- Additional context
- Verified facts

**How to enable:**
- Check "Use web search" in Q&A tab
- Answers will include web context
- See web sources alongside PDF sources

#### 📊 Progress Tracking

Track your learning journey:
- Study time
- Questions answered
- Concepts mastered
- Study streak
- Achievements

**View progress:**
- Sidebar shows current stats
- Dashboard tab for detailed analytics
- Export progress reports

#### 🗣️ Voice Features (Optional)

**Text-to-Speech:**
- Listen to summaries
- Hands-free studying
- Perfect for commuting

**Speech-to-Text:**
- Ask questions by voice
- No typing needed
- Accessibility feature

**How to enable:**
```bash
pip install gtts SpeechRecognition pyaudio
```

#### 💾 Export & Share

**Export Formats:**
- **Markdown (.md)** - For note-taking apps
- **PDF (.pdf)** - For printing
- **Word (.docx)** - For editing
- **Text (.txt)** - Universal format

**What you can export:**
- Summaries
- Study guides
- Q&A sessions
- Flashcards
- Progress reports
- Study schedules

**How to export:**
1. Generate content
2. Click "Download" button
3. Choose format
4. Save to your computer

## 🔧 Configuration & Customization

### Change AI Model

In the sidebar:
1. Select different model from dropdown
2. Reload PDF with new model
3. Compare results

### Adjust Processing Settings

**For faster processing:**
- Reduce chunk size (500-800)
- Use fewer retrieval chunks (k=4)
- Use lighter model (phi)

**For better accuracy:**
- Increase chunk size (1500-2000)
- Use more retrieval chunks (k=8)
- Use better model (llama2)

**Edit in `pdf_rag_reader.py`:**
```python
chunk_size=1500,  # Adjust this
chunk_overlap=300,  # And this
```

### Customize Prompts

Edit prompts in `pdf_rag_reader.py` to change:
- Summary style
- Question types
- Answer format
- Detail level

### Enable/Disable Features

**Disable web search:**
```python
use_web=False  # in ask_with_web_context()
```

**Disable caching:**
```python
use_cache=False  # in PDFRAGReader init
```

## 📊 System Requirements

### Minimum Requirements
- **CPU:** 4-core processor
- **RAM:** 8GB
- **Storage:** 10GB free space
- **OS:** Windows 10+, macOS 10.15+, Linux (Ubuntu 20.04+)
- **Internet:** Required for setup and web search

### Recommended Requirements
- **CPU:** 8-core processor or better
- **RAM:** 16GB or more
- **Storage:** 20GB+ free space (SSD preferred)
- **GPU:** Optional (speeds up processing)
- **Internet:** Broadband for faster downloads

### Performance Expectations

**Processing Times:**
| PDF Size | First Load | Cached Load | Summary | Q&A |
|----------|-----------|-------------|---------|-----|
| 50 pages | 1-2 min | Instant | 30s | 5s |
| 200 pages | 3-5 min | Instant | 45s | 5s |
| 500 pages | 8-12 min | Instant | 60s | 5s |
| 1000+ pages | 15-25 min | Instant | 90s | 5s |
| 5000+ pages | 1-2 hours | Instant | 2min | 5s |

**Note:** First load creates embeddings (slow). Subsequent loads use cache (instant).

## 🐛 Troubleshooting

### Common Issues

#### "Connection refused" error
**Problem:** Ollama is not running

**Solution:**
```bash
# Start Ollama
ollama serve
```

#### "Model not found" error
**Problem:** AI model not downloaded

**Solution:**
```bash
# Download model
ollama pull llama2
```

#### "Module not found" error
**Problem:** Dependencies not installed

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

#### App is very slow
**Problem:** Large PDF or insufficient resources

**Solutions:**
- Use smaller PDFs for testing
- Try faster model (phi or mistral)
- Reduce chunk size in settings
- Close other applications
- Upgrade RAM if possible

#### Out of memory error
**Problem:** PDF too large for available RAM

**Solutions:**
- Use smaller PDFs (<500 pages)
- Try lighter model (phi)
- Reduce chunk size
- Close other applications
- Process in sections

#### Poor quality answers
**Problem:** Wrong model or settings

**Solutions:**
- Use llama2 or mistral (better quality)
- Increase chunk size for more context
- Ask more specific questions
- Check if PDF text extracted correctly
- Enable web search for additional context

#### Web search not working
**Problem:** Missing dependencies

**Solution:**
```bash
pip install duckduckgo-search wikipedia
```

#### Voice features not working
**Problem:** Missing audio dependencies

**Solution:**
```bash
# macOS
brew install portaudio
pip install pyaudio gtts SpeechRecognition

# Linux
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio gtts SpeechRecognition

# Windows
pip install pyaudio gtts SpeechRecognition
```

### Getting Help

1. **Check logs:** Look at terminal output for error messages
2. **Test with small PDF:** Verify app works with simple document
3. **Update dependencies:** `pip install --upgrade -r requirements.txt`
4. **Restart everything:** Close app, restart Ollama, restart app
5. **Check system resources:** Ensure enough RAM and disk space

## 🚀 Deployment Options

### Local Deployment (Recommended)

**Advantages:**
- Complete privacy
- No internet required (after setup)
- Unlimited usage
- Fast performance

**Follow installation guide above**

### Network Deployment (Share with others)

**Run on local network:**
```bash
streamlit run app.py --server.address 0.0.0.0
```

Access from other devices: `http://YOUR_IP:8501`

### Cloud Deployment (Advanced)

**Deploy to cloud for remote access:**

**Option 1: Streamlit Cloud (Free)**
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Deploy

**Note:** Requires cloud-compatible AI model (not Ollama)

**Option 2: Docker**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

```bash
docker build -t ai-study-assistant .
docker run -p 8501:8501 ai-study-assistant
```

**Option 3: VPS (DigitalOcean, AWS, etc.)**
1. Rent a VPS with 16GB+ RAM
2. Install dependencies
3. Run app with systemd service
4. Set up nginx reverse proxy
5. Enable HTTPS with Let's Encrypt

## 📚 Usage Examples

### Example 1: Studying for Biology Exam

```bash
# 1. Upload biology textbook (500 pages)
# 2. Get chapter summaries for chapters 1-10
# 3. Generate 20 practice questions (mixed difficulty)
# 4. Extract key concepts → create flashcards
# 5. Take practice exam
# 6. Ask questions about confusing topics
# 7. Export study guide as PDF
```

**Time saved:** 20+ hours of manual note-taking

### Example 2: Understanding Research Paper

```bash
# 1. Upload paper (30 pages)
# 2. Get full summary
# 3. Ask "What is the main hypothesis?"
# 4. Ask "What methodology was used?"
# 5. Extract key concepts
# 6. Compare concepts (e.g., "control vs experimental")
# 7. Enable web search for latest research
```

**Time saved:** 3-4 hours of reading and research

### Example 3: Exam Preparation

```bash
# 1. Upload course materials (multiple PDFs)
# 2. Create study schedule (exam in 2 weeks)
# 3. Generate daily study questions
# 4. Use spaced repetition flashcards
# 5. Take practice exams weekly
# 6. Track progress and weak areas
# 7. Focus on weak areas last week
```

**Result:** Comprehensive exam preparation

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Test thoroughly**
5. **Commit:** `git commit -m 'Add amazing feature'`
6. **Push:** `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Areas for Contribution

- 🌍 Multi-language support
- 📱 Mobile app version
- 🎨 UI/UX improvements
- 🔧 New features
- 📝 Documentation
- 🐛 Bug fixes
- 🧪 Tests

## 📄 License

MIT License - Free for everyone, forever!

See [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built with amazing open-source technologies:

- **LangChain** - RAG framework
- **FAISS** - Vector database
- **HuggingFace** - Embeddings
- **Ollama** - Local LLM
- **Streamlit** - Web interface
- **PyPDF** - PDF processing

## 💪 Support the Project

If this tool helps you:

- ⭐ **Star the repository**
- 📢 **Share with other students**
- 🐛 **Report bugs or suggest features**
- 🤝 **Contribute improvements**
- 💬 **Spread the word**

## 📞 Contact & Support

- **GitHub Issues:** [Report bugs or request features](https://github.com/aviral1704/ai-study-assistant/issues)
- **Discussions:** [Ask questions or share ideas](https://github.com/aviral1704/ai-study-assistant/discussions)

## 🎯 Roadmap

### Coming Soon
- [ ] Mobile app (iOS & Android)
- [ ] Collaborative study sessions
- [ ] Integration with note-taking apps
- [ ] More AI models support
- [ ] Video lecture analysis
- [ ] Handwriting recognition
- [ ] Multi-document comparison
- [ ] Study group features

### Future Plans
- [ ] Browser extension
- [ ] API for developers
- [ ] Plugin system
- [ ] Advanced analytics
- [ ] Gamification
- [ ] Social features

---

**Made with ❤️ for students everywhere**

**Study smarter, not harder. Your success is our mission.** 🎓✨

**100% Free • 100% Private • 100% Powerful**

---

## ⚡ Quick Links

- [Installation Guide](#-complete-installation-guide)
- [How to Use](#-how-to-use)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

*Last updated: December 2024*
