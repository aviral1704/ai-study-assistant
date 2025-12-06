"""
Streamlit Web App for PDF RAG Reader
Beautiful, user-friendly interface for PDF analysis
"""

import streamlit as st
import os
from pathlib import Path
from pdf_rag_reader import PDFRAGReader
import tempfile

# Page config
st.set_page_config(
    page_title="PDF RAG Reader & Summarizer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Beautiful, Modern Design
st.markdown("""
<style>
    /* Main Theme Colors */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --dark-bg: #1e293b;
        --light-bg: #f8fafc;
    }
    
    /* Headers */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        padding: 1rem 0;
    }
    
    .sub-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e293b;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #6366f1;
    }
    
    /* Info Boxes */
    .info-box {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        border-left: 5px solid #6366f1;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    
    .info-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .info-box h3 {
        color: #6366f1;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .success-box {
        background: linear-gradient(135deg, #10b98115 0%, #059669 15 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        border-left: 5px solid #10b981;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #f59e0b15 0%, #d9770615 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        border-left: 5px solid #f59e0b;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border-radius: 0.5rem;
        padding: 0.75rem 2rem;
        border: none;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: #f8fafc;
        padding: 1rem;
        border-radius: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        color: #64748b;
        border: 2px solid transparent;
        transition: all 0.3s;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: #6366f1;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea15 0%, #764ba215 100%);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #f8fafc;
        border-radius: 0.5rem;
        font-weight: 600;
        color: #1e293b;
    }
    
    /* Progress bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Text areas and inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 0.5rem;
        border: 2px solid #e2e8f0;
        transition: border-color 0.3s;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    /* Cards */
    .element-container {
        transition: transform 0.2s;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #6366f1;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'reader' not in st.session_state:
    st.session_state.reader = None
if 'pdf_loaded' not in st.session_state:
    st.session_state.pdf_loaded = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Header
st.markdown('<div class="main-header">📚 AI Study Assistant</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #7f8c8d;">Free AI-Powered PDF Analysis for Students • Handles 5000+ Pages</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1rem; color: #95a5a6;">Get detailed summaries, study questions, and comprehensive analysis of any PDF</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # File upload
    uploaded_file = st.file_uploader("Upload PDF", type=['pdf'])
    
    # Model selection
    model_name = st.selectbox(
        "Select AI Model",
        ["llama2", "mistral", "llama3", "phi", "gemma"],
        help="Choose the Ollama model to use"
    )
    
    # Advanced settings
    with st.expander("Advanced Settings"):
        chunk_size = st.slider("Chunk Size", 500, 2000, 1000, 100)
        chunk_overlap = st.slider("Chunk Overlap", 50, 500, 200, 50)
    
    # Load PDF button
    if uploaded_file and st.button("🚀 Load & Process PDF", type="primary"):
        with st.spinner("Processing PDF... This may take a minute..."):
            try:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                # Initialize reader
                st.session_state.reader = PDFRAGReader(
                    pdf_path=tmp_path,
                    model_name=model_name,
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap
                )
                st.session_state.pdf_loaded = True
                st.session_state.chat_history = []
                
                st.success("✅ PDF loaded successfully!")
                
            except Exception as e:
                st.error(f"❌ Error loading PDF: {str(e)}")
    
    # Document info
    if st.session_state.pdf_loaded and st.session_state.reader:
        st.markdown("---")
        st.subheader("📊 Document Info")
        info = st.session_state.reader.get_document_info()
        st.write(f"**Pages:** {info['total_pages']}")
        st.write(f"**Chunks:** {info['total_chunks']}")
        st.write(f"**Model:** {info['model']}")

# Main content
if not st.session_state.pdf_loaded:
    # Welcome screen
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="info-box">
            <h3>📖 Comprehensive Summaries</h3>
            <p>Get detailed, study-focused summaries of entire books, chapters, or specific pages. Perfect for exam prep!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h3>🎯 Study Questions & Practice Exams</h3>
            <p>Auto-generate practice questions, flashcards, and full practice exams from any PDF</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-box">
            <h3>💡 Concept Explanations</h3>
            <p>Get detailed explanations of any concept, compare ideas, and build comprehensive study guides</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div class="warning-box">
        <h3>🚀 Getting Started</h3>
        <ol>
            <li>Upload a PDF file using the sidebar</li>
            <li>Select your preferred AI model (llama2 recommended)</li>
            <li>Click "Load & Process PDF"</li>
            <li>Start analyzing your document!</li>
        </ol>
        <p><strong>Note:</strong> Make sure Ollama is installed and running on your system.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    ### 💡 Features for Students
    - **📖 Detailed Summaries**: Comprehensive book, chapter, and page summaries optimized for studying
    - **🎯 Study Questions**: Generate practice questions with detailed answers (easy, medium, hard)
    - **📝 Practice Exams**: Create full practice exams with multiple question types
    - **🔑 Key Concepts**: Extract and explain important terms with examples
    - **📚 Study Guides**: Generate complete study guides for exam preparation
    - **💡 Concept Explanations**: Get detailed explanations of any concept from the document
    - **🔄 Compare Concepts**: Side-by-side comparisons to understand differences
    - **❓ Smart Q&A**: Ask anything and get detailed answers with source citations
    - **💬 Chat Mode**: Natural conversation about your document
    - **⚡ Handles Large PDFs**: Process documents up to 5000+ pages
    - **🆓 100% Free**: No subscriptions, no limits, completely free for students
    """)

else:
    # Main interface with tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📖 Summaries", 
        "❓ Q&A", 
        "🎯 Study Questions", 
        "� StudCy Tools",
        "💬 Chat"
    ])
    
    with tab1:
        st.markdown('<div class="sub-header">Document Summaries</div>', unsafe_allow_html=True)
        
        summary_type = st.radio(
            "Select Summary Type",
            ["Full Book", "Chapter", "Single Page", "Page Range"],
            horizontal=True
        )
        
        if summary_type == "Full Book":
            # Customization options
            col1, col2 = st.columns(2)
            with col1:
                detail_level = st.select_slider(
                    "Detail Level",
                    options=["Brief", "Standard", "Comprehensive", "Very Detailed"],
                    value="Comprehensive"
                )
            with col2:
                focus_area = st.multiselect(
                    "Focus On",
                    ["Key Concepts", "Examples", "Arguments", "Applications", "Historical Context"],
                    default=["Key Concepts", "Arguments"]
                )
            
            if st.button("📚 Generate Full Book Summary", type="primary", use_container_width=True):
                with st.spinner("🤖 AI is analyzing your document... This may take 1-2 minutes..."):
                    try:
                        summary = st.session_state.reader.get_book_summary()
                        
                        st.markdown('<div class="success-box">', unsafe_allow_html=True)
                        st.markdown("### 📚 Complete Book Summary")
                        st.markdown("---")
                        st.write(summary)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Download button
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.download_button(
                                label="📥 Download as TXT",
                                data=summary,
                                file_name="book_summary.txt",
                                mime="text/plain",
                                use_container_width=True
                            )
                        with col2:
                            st.download_button(
                                label="📄 Download as MD",
                                data=f"# Book Summary\n\n{summary}",
                                file_name="book_summary.md",
                                mime="text/markdown",
                                use_container_width=True
                            )
                        with col3:
                            if st.button("🔄 Regenerate", use_container_width=True):
                                st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        st.info("💡 Tip: Make sure Ollama is running and the model is downloaded.")
        
        elif summary_type == "Chapter":
            chapter_num = st.number_input("Chapter Number", min_value=1, value=1)
            if st.button("Generate Chapter Summary", type="primary"):
                with st.spinner(f"Generating summary for Chapter {chapter_num}..."):
                    try:
                        summary = st.session_state.reader.get_chapter_summary(chapter_num)
                        st.markdown('<div class="success-box">', unsafe_allow_html=True)
                        st.markdown(f"### 📑 Chapter {chapter_num} Summary")
                        st.write(summary)
                        st.markdown('</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        elif summary_type == "Single Page":
            info = st.session_state.reader.get_document_info()
            page_num = st.number_input("Page Number", min_value=1, max_value=info['total_pages'], value=1)
            if st.button("Generate Page Summary", type="primary"):
                with st.spinner(f"Generating summary for page {page_num}..."):
                    try:
                        summary = st.session_state.reader.get_page_summary(page_num)
                        st.markdown('<div class="success-box">', unsafe_allow_html=True)
                        st.markdown(f"### 📄 Page {page_num} Summary")
                        st.write(summary)
                        st.markdown('</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        else:  # Page Range
            info = st.session_state.reader.get_document_info()
            col1, col2 = st.columns(2)
            with col1:
                start_page = st.number_input("Start Page", min_value=1, max_value=info['total_pages'], value=1)
            with col2:
                end_page = st.number_input("End Page", min_value=1, max_value=info['total_pages'], value=min(10, info['total_pages']))
            
            if st.button("Generate Page Range Summary", type="primary"):
                with st.spinner(f"Generating summary for pages {start_page}-{end_page}..."):
                    try:
                        summary = st.session_state.reader.get_page_range_summary(start_page, end_page)
                        st.markdown('<div class="success-box">', unsafe_allow_html=True)
                        st.markdown(f"### 📄 Pages {start_page}-{end_page} Summary")
                        st.write(summary)
                        st.markdown('</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    with tab2:
        st.markdown('<div class="sub-header">🎯 Smart Q&A System</div>', unsafe_allow_html=True)
        
        # Quick question templates
        st.markdown("**💡 Quick Questions:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📖 What's the main idea?", use_container_width=True):
                st.session_state.quick_question = "What is the main idea or central theme of this document?"
        with col2:
            if st.button("🔑 Key concepts?", use_container_width=True):
                st.session_state.quick_question = "What are the most important concepts I need to understand?"
        with col3:
            if st.button("📝 Exam tips?", use_container_width=True):
                st.session_state.quick_question = "What are the most important points for exam preparation?"
        
        # Question input
        question = st.text_area(
            "💬 Ask anything about your document:",
            value=st.session_state.get('quick_question', ''),
            height=120,
            placeholder="Example: Explain the difference between supervised and unsupervised learning..."
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            show_sources = st.checkbox("📚 Show source pages", value=True)
        with col2:
            answer_style = st.selectbox("Style", ["Detailed", "Concise", "ELI5"])
        
        if st.button("🚀 Get Answer", type="primary", use_container_width=True) and question:
            with st.spinner("🤖 AI is thinking..."):
                try:
                    # Clear quick question
                    if 'quick_question' in st.session_state:
                        del st.session_state.quick_question
                    
                    result = st.session_state.reader.ask_question(question, show_sources)
                    
                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    st.markdown("### 💡 Answer")
                    st.markdown("---")
                    st.write(result['answer'])
                    
                    if result['sources']:
                        st.markdown("---")
                        st.markdown("### 📚 Source References")
                        cols = st.columns(len(result['sources'][:4]))
                        for idx, src in enumerate(result['sources'][:4]):
                            with cols[idx]:
                                st.metric("Page", src['page'])
                        
                        with st.expander("📄 View Source Content"):
                            for src in result['sources']:
                                st.markdown(f"**Page {src['page']}:**")
                                st.text(src['content_preview'])
                                st.markdown("---")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.download_button(
                            "💾 Save Answer",
                            data=f"Q: {question}\n\nA: {result['answer']}",
                            file_name="qa_answer.txt",
                            use_container_width=True
                        )
                    with col2:
                        if st.button("🔄 Ask Follow-up", use_container_width=True):
                            st.session_state.follow_up = question
                    with col3:
                        if st.button("📋 Copy to Chat", use_container_width=True):
                            st.info("Answer copied to chat history!")
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("💡 Tip: Try rephrasing your question or check if Ollama is running.")
    
    with tab3:
        st.markdown('<div class="sub-header">🎯 Study Questions & Practice Exams</div>', unsafe_allow_html=True)
        
        # Study mode selector
        study_mode = st.radio(
            "Choose Study Mode:",
            ["📝 Practice Questions", "🎯 Practice Exam", "🎴 Flashcards", "⚡ Quick Quiz"],
            horizontal=True
        )
        
        if study_mode == "📝 Practice Questions":
            col1, col2, col3 = st.columns(3)
            with col1:
                num_questions = st.slider("Number of questions", 5, 30, 10)
            with col2:
                difficulty = st.selectbox("Difficulty", ["mixed", "easy", "medium", "hard"])
            with col3:
                question_type = st.selectbox("Type", ["All Types", "Conceptual", "Application", "Analysis"])
            
            if st.button("🚀 Generate Study Questions", type="primary", use_container_width=True):
                with st.spinner("🤖 Creating personalized study questions..."):
                    try:
                        qa_pairs = st.session_state.reader.generate_qa_pairs(num_questions, difficulty)
                        
                        if qa_pairs:
                            st.success(f"✅ Generated {len(qa_pairs)} high-quality questions!")
                            
                            # Progress tracker
                            if 'answered_questions' not in st.session_state:
                                st.session_state.answered_questions = set()
                            
                            progress = len(st.session_state.answered_questions) / len(qa_pairs)
                            st.progress(progress, text=f"Progress: {len(st.session_state.answered_questions)}/{len(qa_pairs)} answered")
                            
                            for i, pair in enumerate(qa_pairs, 1):
                                is_answered = i in st.session_state.answered_questions
                                icon = "✅" if is_answered else "❓"
                                
                                with st.expander(f"{icon} Question {i}: {pair['question']}", expanded=not is_answered):
                                    # Show/Hide answer toggle
                                    show_answer = st.checkbox(f"Show Answer", key=f"show_{i}")
                                    
                                    if show_answer:
                                        st.markdown("**📝 Detailed Answer:**")
                                        st.info(pair['answer'])
                                        
                                        if st.button(f"✓ Mark as Understood", key=f"mark_{i}"):
                                            st.session_state.answered_questions.add(i)
                                            st.rerun()
                                    
                                    st.markdown("---")
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        if st.button("💡 Get Hint", key=f"hint_{i}"):
                                            st.write("Think about the key concepts and their relationships...")
                                    with col2:
                                        if st.button("📚 Related Concepts", key=f"related_{i}"):
                                            st.write("This relates to the main themes discussed in the document...")
                            
                            # Download all questions
                            all_qa = "\n\n".join([f"Q{i}: {pair['question']}\n\nA: {pair['answer']}" for i, pair in enumerate(qa_pairs, 1)])
                            st.download_button(
                                "📥 Download All Questions",
                                data=all_qa,
                                file_name="study_questions.txt",
                                use_container_width=True
                            )
                        else:
                            st.warning("No questions generated. Try again.")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        
        elif study_mode == "🎯 Practice Exam":
            col1, col2 = st.columns(2)
            with col1:
                exam_questions = st.number_input("Number of questions", 10, 50, 20, 5)
            with col2:
                exam_time = st.number_input("Time limit (minutes)", 15, 180, 60, 15)
            
            include_types = st.multiselect(
                "Question Types",
                ["Multiple Choice", "Short Answer", "Essay", "True/False"],
                default=["Multiple Choice", "Short Answer"]
            )
            
            if st.button("📝 Generate Practice Exam", type="primary", use_container_width=True):
                with st.spinner("🎓 Creating your personalized practice exam..."):
                    try:
                        exam = st.session_state.reader.get_practice_exam(exam_questions)
                        
                        st.markdown('<div class="success-box">', unsafe_allow_html=True)
                        st.markdown(f"### 📝 Practice Exam ({exam_time} minutes)")
                        st.markdown("---")
                        st.write(exam['exam'])
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.download_button(
                                "📥 Download Exam",
                                data=exam['exam'],
                                file_name="practice_exam.txt",
                                use_container_width=True
                            )
                        with col2:
                            if st.button("⏱️ Start Timer", use_container_width=True):
                                st.info(f"Timer started! You have {exam_time} minutes.")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        
        elif study_mode == "🎴 Flashcards":
            st.info("🎴 Flashcard mode - Perfect for memorization!")
            
            if st.button("Generate Flashcards", type="primary", use_container_width=True):
                with st.spinner("Creating flashcards..."):
                    try:
                        concepts = st.session_state.reader.get_key_concepts()
                        st.success("✅ Flashcards ready!")
                        st.write(concepts)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        else:  # Quick Quiz
            st.info("⚡ Quick Quiz - Test your knowledge in 5 minutes!")
            
            if st.button("Start Quick Quiz", type="primary", use_container_width=True):
                with st.spinner("Preparing quiz..."):
                    try:
                        qa_pairs = st.session_state.reader.generate_qa_pairs(5, "mixed")
                        st.success("✅ Quiz ready! Answer all 5 questions.")
                        
                        for i, pair in enumerate(qa_pairs, 1):
                            st.markdown(f"**Question {i}:** {pair['question']}")
                            user_answer = st.text_area(f"Your answer:", key=f"quiz_{i}", height=100)
                            
                            if st.button(f"Check Answer", key=f"check_{i}"):
                                st.info(f"**Correct Answer:** {pair['answer']}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    with tab4:
        st.markdown('<div class="sub-header">Study Tools & Concept Explorer</div>', unsafe_allow_html=True)
        
        tool_option = st.radio(
            "Select Study Tool",
            ["Key Concepts Glossary", "Complete Study Guide", "Explain a Concept", "Compare Concepts"],
            horizontal=True
        )
        
        if tool_option == "Key Concepts Glossary":
            if st.button("Extract Key Concepts", type="primary"):
                with st.spinner("Extracting comprehensive key concepts..."):
                    try:
                        concepts = st.session_state.reader.get_key_concepts()
                        st.markdown('<div class="success-box">', unsafe_allow_html=True)
                        st.markdown("### 🔑 Key Concepts & Definitions")
                        st.write(concepts)
                        st.markdown('</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        elif tool_option == "Complete Study Guide":
            if st.button("Generate Study Guide", type="primary"):
                with st.spinner("Creating comprehensive study guide... This may take a few minutes..."):
                    try:
                        guide = st.session_state.reader.generate_study_guide()
                        st.markdown('<div class="success-box">', unsafe_allow_html=True)
                        st.markdown("### 📚 Complete Study Guide")
                        st.write(guide['study_guide'])
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Download button
                        st.download_button(
                            label="📥 Download Study Guide",
                            data=guide['study_guide'],
                            file_name="study_guide.txt",
                            mime="text/plain"
                        )
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        elif tool_option == "Explain a Concept":
            concept = st.text_input("Enter concept to explain:", placeholder="e.g., photosynthesis, supply and demand")
            if st.button("Get Detailed Explanation", type="primary") and concept:
                with st.spinner(f"Generating detailed explanation of '{concept}'..."):
                    try:
                        explanation = st.session_state.reader.explain_concept(concept)
                        st.markdown('<div class="success-box">', unsafe_allow_html=True)
                        st.markdown(f"### 💡 Understanding: {concept}")
                        st.write(explanation)
                        st.markdown('</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        else:  # Compare Concepts
            col1, col2 = st.columns(2)
            with col1:
                concept1 = st.text_input("First concept:", placeholder="e.g., mitosis")
            with col2:
                concept2 = st.text_input("Second concept:", placeholder="e.g., meiosis")
            
            if st.button("Compare Concepts", type="primary") and concept1 and concept2:
                with st.spinner(f"Comparing '{concept1}' and '{concept2}'..."):
                    try:
                        comparison = st.session_state.reader.compare_concepts(concept1, concept2)
                        st.markdown('<div class="success-box">', unsafe_allow_html=True)
                        st.markdown(f"### 🔄 Comparison: {concept1} vs {concept2}")
                        st.write(comparison)
                        st.markdown('</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    with tab5:
        st.markdown('<div class="sub-header">Chat with Your PDF</div>', unsafe_allow_html=True)
        
        # Display chat history
        for i, chat in enumerate(st.session_state.chat_history):
            with st.chat_message("user"):
                st.write(chat['question'])
            with st.chat_message("assistant"):
                st.write(chat['answer'])
        
        # Chat input
        user_question = st.chat_input("Ask anything about your PDF...")
        
        if user_question:
            # Add to chat history
            with st.chat_message("user"):
                st.write(user_question)
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        result = st.session_state.reader.ask_question(user_question, show_sources=False)
                        st.write(result['answer'])
                        
                        # Save to history
                        st.session_state.chat_history.append({
                            'question': user_question,
                            'answer': result['answer']
                        })
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; padding: 2rem;">
    <p><strong>100% Free AI Study Assistant for Students</strong></p>
    <p>Built with ❤️ using LangChain, Streamlit & Ollama • Runs completely on your computer</p>
    <p>No data collection • No tracking • Complete privacy</p>
    <p style="font-size: 0.9rem; margin-top: 1rem;">For best results, use llama2 or mistral models • Handles PDFs up to 5000+ pages</p>
</div>
""", unsafe_allow_html=True)
