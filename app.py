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

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
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
            if st.button("Generate Full Book Summary", type="primary"):
                with st.spinner("Generating summary..."):
                    try:
                        summary = st.session_state.reader.get_book_summary()
                        st.markdown('<div class="success-box">', unsafe_allow_html=True)
                        st.markdown("### 📚 Full Book Summary")
                        st.write(summary)
                        st.markdown('</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
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
        st.markdown('<div class="sub-header">Ask Questions</div>', unsafe_allow_html=True)
        
        question = st.text_area("Enter your question about the document:", height=100)
        show_sources = st.checkbox("Show source pages", value=True)
        
        if st.button("Get Answer", type="primary") and question:
            with st.spinner("Finding answer..."):
                try:
                    result = st.session_state.reader.ask_question(question, show_sources)
                    
                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    st.markdown("### 💡 Answer")
                    st.write(result['answer'])
                    
                    if result['sources']:
                        st.markdown("### 📚 Sources")
                        for src in result['sources']:
                            with st.expander(f"Page {src['page']}"):
                                st.write(src['content_preview'])
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with tab3:
        st.markdown('<div class="sub-header">Study Questions & Practice</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            num_questions = st.slider("Number of questions", 5, 30, 10)
        with col2:
            difficulty = st.selectbox("Difficulty Level", ["mixed", "easy", "medium", "hard"])
        
        if st.button("Generate Study Questions", type="primary"):
            with st.spinner("Generating comprehensive study questions..."):
                try:
                    qa_pairs = st.session_state.reader.generate_qa_pairs(num_questions, difficulty)
                    
                    if qa_pairs:
                        st.success(f"✅ Generated {len(qa_pairs)} questions!")
                        for i, pair in enumerate(qa_pairs, 1):
                            with st.expander(f"❓ Question {i}: {pair['question']}", expanded=False):
                                st.markdown("**📝 Answer:**")
                                st.write(pair['answer'])
                                st.markdown("---")
                    else:
                        st.warning("No Q&A pairs generated. Try again.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        st.markdown("---")
        st.subheader("🎯 Practice Exam Generator")
        
        exam_questions = st.number_input("Number of exam questions", 10, 50, 20, 5)
        if st.button("Generate Practice Exam", type="secondary"):
            with st.spinner("Creating practice exam..."):
                try:
                    exam = st.session_state.reader.get_practice_exam(exam_questions)
                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    st.markdown("### 📝 Practice Exam")
                    st.write(exam['exam'])
                    st.markdown('</div>', unsafe_allow_html=True)
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
