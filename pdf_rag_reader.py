"""
Advanced PDF RAG Reader - Optimized for Large Documents & Student Learning
Handles 5000+ page PDFs with detailed, study-focused summaries
Now with Real-Time Web Search Integration for Enhanced Context
"""

import os
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import hashlib
import pickle
import warnings
warnings.filterwarnings('ignore')

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document

# Real-time search imports
try:
    from duckduckgo_search import DDGS
    SEARCH_AVAILABLE = True
except ImportError:
    SEARCH_AVAILABLE = False
    print("⚠️  Web search not available. Install: pip install duckduckgo-search")

try:
    import wikipedia
    WIKIPEDIA_AVAILABLE = True
except ImportError:
    WIKIPEDIA_AVAILABLE = False
    print("⚠️  Wikipedia search not available. Install: pip install wikipedia")


class PDFRAGReader:
    """
    Advanced PDF reader optimized for large documents and detailed student-focused analysis.
    Handles 5000+ pages with intelligent chunking and comprehensive summaries.
    """
    
    def __init__(
        self,
        pdf_path: str,
        model_name: str = "llama2",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        chunk_size: int = 1500,  # Larger chunks for better context
        chunk_overlap: int = 300,  # More overlap to preserve context
        use_cache: bool = True
    ):
        """
        Initialize the PDF RAG Reader with optimizations for large documents.
        
        Args:
            pdf_path: Path to the PDF file
            model_name: Ollama model name (llama2, mistral, etc.)
            embedding_model: HuggingFace embedding model
            chunk_size: Size of text chunks (larger for better context)
            chunk_overlap: Overlap between chunks (more for continuity)
            use_cache: Cache embeddings for faster reloading
        """
        self.pdf_path = pdf_path
        self.model_name = model_name
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.use_cache = use_cache
        
        # Create cache directory
        self.cache_dir = Path(".cache")
        self.cache_dir.mkdir(exist_ok=True)
        
        print(f"📚 Loading PDF: {pdf_path}")
        
        # Load PDF with progress
        self.loader = PyPDFLoader(pdf_path)
        self.pages = self.loader.load()
        
        print(f"✅ Loaded {len(self.pages)} pages")
        
        # Check cache
        cache_key = self._get_cache_key()
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        
        if use_cache and cache_file.exists():
            print("⚡ Loading from cache...")
            self._load_from_cache(cache_file)
        else:
            # Initialize embeddings
            print("🔧 Initializing embeddings (this may take a few minutes for large PDFs)...")
            self.embeddings = HuggingFaceEmbeddings(
                model_name=embedding_model,
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'batch_size': 32, 'show_progress_bar': True}
            )
            
            # Split documents with optimized settings
            print("✂️  Splitting documents into chunks...")
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                length_function=len,
                separators=["\n\n", "\n", ". ", " ", ""]  # Better splitting
            )
            self.chunks = self.text_splitter.split_documents(self.pages)
            print(f"✅ Created {len(self.chunks)} chunks")
            
            # Create vector store with batching for large documents
            print("🗄️  Creating vector database (this may take a few minutes)...")
            self.vectorstore = FAISS.from_documents(
                documents=self.chunks,
                embedding=self.embeddings
            )
            
            # Save to cache
            if use_cache:
                print("💾 Saving to cache for faster future loading...")
                self._save_to_cache(cache_file)
        
        # Initialize LLM with streaming for better UX
        print(f"🤖 Initializing {model_name} model...")
        self.llm = OllamaLLM(
            model=model_name,
            temperature=0.3,  # Lower for more factual responses
            num_ctx=4096,  # Larger context window
        )
        
        # Create retrieval chain with more chunks for detailed answers
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_type="mmr",  # Maximum Marginal Relevance for diversity
                search_kwargs={"k": 8, "fetch_k": 20}  # More chunks for detailed answers
            ),
            return_source_documents=True
        )
        
        print("✅ PDF RAG Reader initialized and ready!\n")
    
    def _get_cache_key(self) -> str:
        """Generate cache key based on PDF content and settings."""
        with open(self.pdf_path, 'rb') as f:
            pdf_hash = hashlib.md5(f.read()).hexdigest()
        settings = f"{self.chunk_size}_{self.chunk_overlap}"
        return f"{pdf_hash}_{settings}"
    
    def _save_to_cache(self, cache_file: Path):
        """Save processed data to cache."""
        cache_data = {
            'chunks': self.chunks,
            'vectorstore': self.vectorstore,
            'embeddings': self.embeddings
        }
        with open(cache_file, 'wb') as f:
            pickle.dump(cache_data, f)
    
    def _load_from_cache(self, cache_file: Path):
        """Load processed data from cache."""
        with open(cache_file, 'rb') as f:
            cache_data = pickle.load(f)
        self.chunks = cache_data['chunks']
        self.vectorstore = cache_data['vectorstore']
        self.embeddings = cache_data['embeddings']
        print(f"✅ Loaded {len(self.chunks)} chunks from cache")
    
    def get_book_summary(self) -> str:
        """Generate a comprehensive, student-focused summary of the entire document."""
        print("📖 Generating comprehensive book summary...\n")
        
        prompt = """You are an expert educator helping students understand this document deeply. 
        Provide a COMPREHENSIVE and DETAILED summary that includes:

        1. OVERVIEW (2-3 paragraphs):
           - What is this document about?
           - Who is the intended audience?
           - What is the main purpose or thesis?

        2. KEY THEMES & CONCEPTS (detailed list):
           - List and explain 5-10 major themes
           - For each theme, provide context and significance
           - Explain how themes interconnect

        3. MAIN ARGUMENTS & IDEAS (detailed):
           - What are the central arguments presented?
           - What evidence or examples support these arguments?
           - What conclusions are drawn?

        4. IMPORTANT TAKEAWAYS (for students):
           - What should students remember most?
           - What are the practical applications?
           - How does this connect to broader topics?

        5. STRUCTURE & ORGANIZATION:
           - How is the document organized?
           - What are the major sections?
           - How do sections build on each other?

        Be thorough, clear, and educational. Use examples from the text. 
        This summary should help students deeply understand the material for exams and essays.
        Aim for 800-1200 words of detailed, valuable content."""
        
        result = self.qa_chain({"query": prompt})
        return result['result']
    
    def get_chapter_summary(self, chapter_number: int) -> str:
        """
        Generate detailed, study-focused summary for a specific chapter.
        
        Args:
            chapter_number: Chapter number to summarize
        """
        print(f"📑 Generating detailed summary for Chapter {chapter_number}...\n")
        
        prompt = f"""You are helping a student study Chapter {chapter_number}. Provide a DETAILED and COMPREHENSIVE summary:

        1. CHAPTER OVERVIEW:
           - What is the main focus of this chapter?
           - What questions does it answer?
           - Why is this chapter important?

        2. KEY CONCEPTS & DEFINITIONS (detailed):
           - List all important terms and concepts
           - Provide clear definitions and explanations
           - Give examples for each concept

        3. MAIN ARGUMENTS & POINTS:
           - What are the primary arguments made?
           - What evidence or data supports these points?
           - What examples or case studies are used?

        4. IMPORTANT DETAILS:
           - What specific facts, figures, or dates are mentioned?
           - What processes or methods are explained?
           - What theories or models are introduced?

        5. CONNECTIONS:
           - How does this chapter relate to previous chapters?
           - What themes continue or develop?
           - How does it set up future chapters?

        6. STUDY POINTS (for exams):
           - What are the most testable concepts?
           - What should students memorize?
           - What requires deeper understanding?

        Be extremely detailed and thorough. Include specific examples and quotes when relevant.
        This should be comprehensive enough for exam preparation. Aim for 600-900 words."""
        
        result = self.qa_chain({"query": prompt})
        return result['result']
    
    def get_page_summary(self, page_number: int) -> str:
        """
        Get summary of a specific page.
        
        Args:
            page_number: Page number (1-indexed)
        """
        if page_number < 1 or page_number > len(self.pages):
            return f"Error: Page {page_number} does not exist. Document has {len(self.pages)} pages."
        
        page_content = self.pages[page_number - 1].page_content
        
        print(f"📄 Summarizing page {page_number}...\n")
        
        prompt = f"""Summarize the following page content in 2-3 paragraphs:

{page_content}

Focus on the main ideas and key information."""
        
        result = self.qa_chain({"query": prompt})
        return result['result']
    
    def get_page_range_summary(self, start_page: int, end_page: int) -> str:
        """
        Get summary of a range of pages.
        
        Args:
            start_page: Starting page number (1-indexed)
            end_page: Ending page number (1-indexed)
        """
        if start_page < 1 or end_page > len(self.pages) or start_page > end_page:
            return f"Error: Invalid page range. Document has {len(self.pages)} pages."
        
        print(f"📄 Summarizing pages {start_page}-{end_page}...\n")
        
        prompt = f"""Provide a comprehensive summary of pages {start_page} to {end_page}, including:
        1. Main topics discussed
        2. Key arguments or points
        3. Important details or examples
        4. Overall flow and structure
        
        Be thorough and well-organized."""
        
        result = self.qa_chain({"query": prompt})
        return result['result']
    
    def ask_question(self, question: str, show_sources: bool = True) -> Dict:
        """
        Ask a question about the document.
        
        Args:
            question: Question to ask
            show_sources: Whether to show source pages
            
        Returns:
            Dictionary with answer and source information
        """
        print(f"❓ Question: {question}\n")
        
        result = self.qa_chain({"query": question})
        
        response = {
            'answer': result['result'],
            'sources': []
        }
        
        if show_sources and 'source_documents' in result:
            for doc in result['source_documents']:
                page_num = doc.metadata.get('page', 'Unknown')
                response['sources'].append({
                    'page': page_num + 1 if isinstance(page_num, int) else page_num,
                    'content_preview': doc.page_content[:200] + "..."
                })
        
        return response
    
    def generate_qa_pairs(self, num_questions: int = 10, difficulty: str = "mixed") -> List[Dict[str, str]]:
        """
        Generate comprehensive Q&A pairs optimized for studying and exam prep.
        
        Args:
            num_questions: Number of Q&A pairs to generate
            difficulty: "easy", "medium", "hard", or "mixed"
        """
        print(f"🎯 Generating {num_questions} detailed study questions...\n")
        
        difficulty_guide = {
            "easy": "Focus on definitions, basic concepts, and recall questions.",
            "medium": "Focus on understanding, application, and explanation questions.",
            "hard": "Focus on analysis, synthesis, evaluation, and critical thinking questions.",
            "mixed": "Include a mix of easy (recall), medium (understanding), and hard (analysis) questions."
        }
        
        prompt = f"""You are creating a comprehensive study guide. Generate {num_questions} high-quality questions and detailed answers.

        DIFFICULTY LEVEL: {difficulty}
        {difficulty_guide.get(difficulty, difficulty_guide["mixed"])}

        For each question:
        - Make it specific and clear
        - Cover different topics from the document
        - Include various question types (what, why, how, compare, analyze)
        - Provide DETAILED, COMPREHENSIVE answers (3-5 sentences minimum)
        - Include examples or evidence from the text
        - Explain WHY the answer is correct

        Format EXACTLY as:
        Q: [Clear, specific question]
        A: [Detailed, comprehensive answer with examples and explanations]

        Cover these question types:
        - Definitions and concepts
        - Main ideas and themes
        - Cause and effect
        - Comparisons and contrasts
        - Applications and examples
        - Critical analysis

        Make these questions valuable for exam preparation and deep understanding."""
        
        result = self.qa_chain({"query": prompt})
        
        # Parse the result into Q&A pairs with better handling
        qa_pairs = []
        lines = result['result'].split('\n')
        current_q = None
        current_a = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('Q:') or line.startswith('Question'):
                if current_q and current_a:
                    qa_pairs.append({
                        'question': current_q,
                        'answer': ' '.join(current_a).strip()
                    })
                current_q = line.split(':', 1)[1].strip() if ':' in line else line
                current_a = []
            elif line.startswith('A:') or line.startswith('Answer'):
                answer_text = line.split(':', 1)[1].strip() if ':' in line else line
                current_a.append(answer_text)
            elif current_q and line:  # Continue answer
                current_a.append(line)
        
        # Add the last pair
        if current_q and current_a:
            qa_pairs.append({
                'question': current_q,
                'answer': ' '.join(current_a).strip()
            })
        
        return qa_pairs[:num_questions]  # Ensure we return requested number
    
    def get_key_concepts(self) -> str:
        """Extract comprehensive key concepts optimized for student learning."""
        print("🔑 Extracting key concepts and definitions...\n")
        
        prompt = """You are creating a comprehensive study glossary. Extract and explain the 15-25 most important concepts, terms, and ideas.

        For EACH concept provide:
        1. TERM/CONCEPT NAME (bold or clear)
        2. CLEAR DEFINITION (2-3 sentences)
        3. CONTEXT: Why is this important? How is it used?
        4. EXAMPLE: Provide a concrete example or application
        5. CONNECTIONS: How does it relate to other concepts?

        Categories to cover:
        - Key terminology and definitions
        - Main theories or frameworks
        - Important people or contributors
        - Critical processes or methods
        - Central arguments or ideas
        - Significant data or findings

        Format clearly with headers and bullet points.
        Make this a valuable study resource that students can use for exam prep.
        Be thorough and educational - this is a primary study tool."""
        
        result = self.qa_chain({"query": prompt})
        return result['result']
    
    def generate_study_guide(self) -> Dict[str, str]:
        """Generate a comprehensive study guide for the entire document."""
        print("📝 Generating comprehensive study guide...\n")
        
        prompt = """Create a COMPLETE STUDY GUIDE for this document. This should be comprehensive enough for exam preparation.

        Include:

        1. DOCUMENT OVERVIEW (3-4 paragraphs)
           - Main topic and scope
           - Key objectives
           - Target audience and purpose

        2. MAJOR THEMES (5-8 themes)
           - List each theme
           - Explain significance
           - Provide examples

        3. KEY CONCEPTS GLOSSARY (15-20 terms)
           - Term: Definition
           - Include context and examples

        4. MAIN ARGUMENTS & EVIDENCE
           - What are the primary claims?
           - What evidence supports them?
           - What are the conclusions?

        5. IMPORTANT FACTS & FIGURES
           - Key statistics
           - Important dates
           - Significant data points

        6. CRITICAL ANALYSIS POINTS
           - Strengths of the arguments
           - Limitations or criticisms
           - Alternative perspectives

        7. EXAM PREPARATION TIPS
           - Most testable concepts
           - Common question types
           - What to memorize vs understand

        Be extremely thorough and detailed. This is a primary study resource."""
        
        result = self.qa_chain({"query": prompt})
        return {
            'study_guide': result['result'],
            'sources': [doc.metadata.get('page', 'Unknown') for doc in result.get('source_documents', [])]
        }
    
    def get_practice_exam(self, num_questions: int = 20) -> Dict:
        """Generate a practice exam with multiple question types."""
        print(f"📝 Generating practice exam with {num_questions} questions...\n")
        
        prompt = f"""Create a PRACTICE EXAM with {num_questions} questions to test comprehensive understanding.

        Include these question types:
        
        1. MULTIPLE CHOICE (30%): 
           - Question with 4 options (A, B, C, D)
           - Mark correct answer
           - Explain why it's correct

        2. SHORT ANSWER (30%):
           - Questions requiring 2-3 sentence responses
           - Provide model answers

        3. ESSAY/ANALYSIS (20%):
           - Questions requiring detailed analysis
           - Provide comprehensive answer guidelines

        4. TRUE/FALSE (20%):
           - Statements to evaluate
           - Explain why true or false

        Format clearly with:
        - Question number
        - Question type
        - The question
        - Answer/explanation

        Cover all major topics from the document.
        Make questions challenging but fair.
        This should thoroughly test student understanding."""
        
        result = self.qa_chain({"query": prompt})
        return {
            'exam': result['result'],
            'num_questions': num_questions
        }
    
    def explain_concept(self, concept: str) -> str:
        """Get detailed explanation of a specific concept for studying."""
        print(f"💡 Explaining concept: {concept}...\n")
        
        prompt = f"""Provide a COMPREHENSIVE, STUDENT-FRIENDLY explanation of: {concept}

        Include:

        1. SIMPLE DEFINITION (1-2 sentences)
           - Explain in plain language
           - What is it in simple terms?

        2. DETAILED EXPLANATION (2-3 paragraphs)
           - Provide thorough context
           - Explain all components
           - Describe how it works

        3. WHY IT MATTERS
           - Why is this concept important?
           - What problems does it solve?
           - What is its significance?

        4. EXAMPLES (2-3 concrete examples)
           - Real-world applications
           - Specific instances from the text
           - Analogies if helpful

        5. COMMON MISCONCEPTIONS
           - What do students often get wrong?
           - What should they avoid?

        6. CONNECTIONS
           - How does this relate to other concepts?
           - What builds on this?
           - What does this build on?

        7. STUDY TIPS
           - How to remember this
           - What to focus on for exams
           - Key points to memorize

        Make this explanation thorough, clear, and perfect for studying."""
        
        result = self.qa_chain({"query": prompt})
        return result['result']
    
    def compare_concepts(self, concept1: str, concept2: str) -> str:
        """Compare and contrast two concepts for deeper understanding."""
        print(f"🔄 Comparing {concept1} vs {concept2}...\n")
        
        prompt = f"""Provide a DETAILED COMPARISON of these two concepts: "{concept1}" and "{concept2}"

        Structure your comparison:

        1. BRIEF DEFINITIONS
           - {concept1}: [definition]
           - {concept2}: [definition]

        2. SIMILARITIES (3-5 points)
           - What do they have in common?
           - Shared characteristics
           - Similar applications

        3. DIFFERENCES (3-5 points)
           - How are they different?
           - Contrasting features
           - Different uses or contexts

        4. WHEN TO USE EACH
           - When is {concept1} more appropriate?
           - When is {concept2} more appropriate?
           - Decision criteria

        5. RELATIONSHIP
           - How do they relate to each other?
           - Do they complement or compete?
           - Can they be used together?

        6. EXAMPLES
           - Example of {concept1} in action
           - Example of {concept2} in action
           - Comparative example

        7. EXAM TIPS
           - How to distinguish them on tests
           - Common comparison questions
           - What to remember

        Be thorough and educational. Help students deeply understand both concepts."""
        
        result = self.qa_chain({"query": prompt})
        return result['result']
    
    def web_search(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """Search the web for additional context and information."""
        if not SEARCH_AVAILABLE:
            return [{"title": "Search Unavailable", "snippet": "Install duckduckgo-search to enable web search"}]
        
        try:
            print(f"🌐 Searching web for: {query}")
            ddgs = DDGS()
            results = []
            
            for r in ddgs.text(query, max_results=num_results):
                results.append({
                    'title': r.get('title', 'No title'),
                    'snippet': r.get('body', 'No description'),
                    'url': r.get('href', '')
                })
            
            return results
        except Exception as e:
            print(f"Web search error: {e}")
            return [{"title": "Search Error", "snippet": str(e)}]
    
    def get_wikipedia_context(self, topic: str) -> str:
        """Get Wikipedia summary for additional context."""
        if not WIKIPEDIA_AVAILABLE:
            return "Wikipedia not available. Install: pip install wikipedia"
        
        try:
            print(f"📚 Fetching Wikipedia context for: {topic}")
            summary = wikipedia.summary(topic, sentences=5, auto_suggest=True)
            return summary
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Multiple topics found. Please be more specific: {', '.join(e.options[:5])}"
        except wikipedia.exceptions.PageError:
            return f"No Wikipedia page found for '{topic}'"
        except Exception as e:
            return f"Wikipedia error: {str(e)}"
    
    def ask_with_web_context(self, question: str, use_web: bool = True, show_sources: bool = True) -> Dict:
        """
        Answer questions using both PDF content and real-time web search for enhanced context.
        
        Args:
            question: Question to ask
            use_web: Whether to include web search results
            show_sources: Whether to show source pages
            
        Returns:
            Dictionary with answer, sources, and web context
        """
        print(f"❓ Question with web context: {question}\n")
        
        # Get answer from PDF
        pdf_result = self.ask_question(question, show_sources)
        
        web_context = ""
        web_results = []
        
        if use_web and SEARCH_AVAILABLE:
            # Search web for additional context
            web_results = self.web_search(question, num_results=3)
            
            if web_results:
                web_context = "\n\nADDITIONAL WEB CONTEXT:\n"
                for i, result in enumerate(web_results, 1):
                    web_context += f"\n{i}. {result['title']}\n   {result['snippet']}\n"
        
        # Enhance answer with web context
        if web_context:
            enhanced_prompt = f"""Based on the document content and the following additional web context, provide a comprehensive answer:

DOCUMENT ANSWER:
{pdf_result['answer']}

{web_context}

Synthesize both sources to provide the most complete, accurate, and up-to-date answer. 
Mention if the web context adds new information or confirms the document content."""
            
            try:
                enhanced_result = self.qa_chain({"query": enhanced_prompt})
                final_answer = enhanced_result['result']
            except:
                final_answer = pdf_result['answer'] + "\n\n" + web_context
        else:
            final_answer = pdf_result['answer']
        
        return {
            'answer': final_answer,
            'sources': pdf_result.get('sources', []),
            'web_results': web_results,
            'has_web_context': bool(web_context)
        }
    
    def get_current_knowledge(self, topic: str) -> str:
        """Get current, real-time knowledge about a topic to supplement PDF content."""
        print(f"🌍 Fetching current knowledge about: {topic}\n")
        
        # Get Wikipedia context
        wiki_context = self.get_wikipedia_context(topic)
        
        # Get web search results
        web_results = self.web_search(f"latest information about {topic}", num_results=3)
        
        # Combine contexts
        combined_context = f"""CURRENT KNOWLEDGE ABOUT: {topic}

WIKIPEDIA SUMMARY:
{wiki_context}

RECENT WEB INFORMATION:
"""
        
        for i, result in enumerate(web_results, 1):
            combined_context += f"\n{i}. {result['title']}\n   {result['snippet']}\n"
        
        # Ask LLM to synthesize
        prompt = f"""Based on the following current information, provide a comprehensive, up-to-date explanation:

{combined_context}

Provide a clear, educational summary that:
1. Explains the current understanding of this topic
2. Highlights recent developments or discoveries
3. Connects to practical applications
4. Is accurate and well-sourced

Make this helpful for students who want the most current information."""
        
        try:
            result = self.qa_chain({"query": prompt})
            return result['result']
        except:
            return combined_context
    
    def get_document_info(self) -> Dict:
        """Get basic information about the document."""
        return {
            'total_pages': len(self.pages),
            'total_chunks': len(self.chunks),
            'chunk_size': self.chunk_size,
            'chunk_overlap': self.chunk_overlap,
            'model': self.model_name,
            'file_path': self.pdf_path
        }


def main():
    """Example usage of PDF RAG Reader."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python pdf_rag_reader.py <path_to_pdf>")
        print("\nExample: python pdf_rag_reader.py my_book.pdf")
        return
    
    pdf_path = sys.argv[1]
    
    if not os.path.exists(pdf_path):
        print(f"❌ Error: File '{pdf_path}' not found!")
        return
    
    # Initialize reader
    reader = PDFRAGReader(
        pdf_path=pdf_path,
        model_name="llama2",
        chunk_size=1000,
        chunk_overlap=200
    )
    
    # Show document info
    info = reader.get_document_info()
    print("\n📊 Document Information:")
    print(f"  Total Pages: {info['total_pages']}")
    print(f"  Total Chunks: {info['total_chunks']}")
    print(f"  Model: {info['model']}\n")


if __name__ == "__main__":
    main()
