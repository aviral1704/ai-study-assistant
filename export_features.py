"""
Export and Sharing Features
- Export to multiple formats (PDF, DOCX, MD, HTML)
- Create study guides
- Generate printable materials
- Share notes
"""

from pathlib import Path
from datetime import datetime
import json

try:
    from fpdf import FPDF
    PDF_EXPORT = True
except ImportError:
    PDF_EXPORT = False

try:
    from docx import Document
    from docx.shared import Inches, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    DOCX_EXPORT = True
except ImportError:
    DOCX_EXPORT = False


class StudyMaterialExporter:
    """Export study materials in various formats."""
    
    def __init__(self):
        self.export_dir = Path("exports")
        self.export_dir.mkdir(exist_ok=True)
    
    def export_to_markdown(self, content: dict, filename: str = None) -> str:
        """Export content to Markdown format."""
        if not filename:
            filename = f"study_notes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        filepath = self.export_dir / filename
        
        md_content = f"""# Study Notes
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

"""
        
        if 'summary' in content:
            md_content += f"""## 📚 Summary

{content['summary']}

---

"""
        
        if 'key_concepts' in content:
            md_content += f"""## 🔑 Key Concepts

{content['key_concepts']}

---

"""
        
        if 'questions' in content:
            md_content += """## 🎯 Practice Questions

"""
            for i, qa in enumerate(content['questions'], 1):
                md_content += f"""### Question {i}
**Q:** {qa['question']}

**A:** {qa['answer']}

---

"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        return str(filepath)
    
    def export_to_pdf(self, content: dict, filename: str = None) -> str:
        """Export content to PDF format."""
        if not PDF_EXPORT:
            return "PDF export not available. Install: pip install fpdf2"
        
        if not filename:
            filename = f"study_notes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        filepath = self.export_dir / filename
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        
        # Title
        pdf.cell(0, 10, "Study Notes", ln=True, align='C')
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
        pdf.ln(10)
        
        # Summary
        if 'summary' in content:
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "Summary", ln=True)
            pdf.set_font("Arial", "", 11)
            pdf.multi_cell(0, 5, content['summary'])
            pdf.ln(5)
        
        # Key Concepts
        if 'key_concepts' in content:
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "Key Concepts", ln=True)
            pdf.set_font("Arial", "", 11)
            pdf.multi_cell(0, 5, content['key_concepts'])
            pdf.ln(5)
        
        # Questions
        if 'questions' in content:
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "Practice Questions", ln=True)
            
            for i, qa in enumerate(content['questions'], 1):
                pdf.set_font("Arial", "B", 11)
                pdf.cell(0, 8, f"Question {i}:", ln=True)
                pdf.set_font("Arial", "", 11)
                pdf.multi_cell(0, 5, f"Q: {qa['question']}")
                pdf.multi_cell(0, 5, f"A: {qa['answer']}")
                pdf.ln(3)
        
        pdf.output(str(filepath))
        return str(filepath)
    
    def export_to_docx(self, content: dict, filename: str = None) -> str:
        """Export content to Word document."""
        if not DOCX_EXPORT:
            return "DOCX export not available. Install: pip install python-docx"
        
        if not filename:
            filename = f"study_notes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        
        filepath = self.export_dir / filename
        
        doc = Document()
        
        # Title
        title = doc.add_heading('Study Notes', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Date
        date_para = doc.add_paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        doc.add_paragraph()
        
        # Summary
        if 'summary' in content:
            doc.add_heading('📚 Summary', 1)
            doc.add_paragraph(content['summary'])
            doc.add_paragraph()
        
        # Key Concepts
        if 'key_concepts' in content:
            doc.add_heading('🔑 Key Concepts', 1)
            doc.add_paragraph(content['key_concepts'])
            doc.add_paragraph()
        
        # Questions
        if 'questions' in content:
            doc.add_heading('🎯 Practice Questions', 1)
            
            for i, qa in enumerate(content['questions'], 1):
                doc.add_heading(f'Question {i}', 2)
                q_para = doc.add_paragraph()
                q_para.add_run('Q: ').bold = True
                q_para.add_run(qa['question'])
                
                a_para = doc.add_paragraph()
                a_para.add_run('A: ').bold = True
                a_para.add_run(qa['answer'])
                
                doc.add_paragraph()
        
        doc.save(str(filepath))
        return str(filepath)
    
    def create_flashcard_deck(self, concepts: list, filename: str = None) -> str:
        """Create printable flashcard deck."""
        if not filename:
            filename = f"flashcards_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        filepath = self.export_dir / filename
        
        content = f"""# Flashcard Deck
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Total Cards: {len(concepts)}

---

"""
        
        for i, concept in enumerate(concepts, 1):
            content += f"""## Card {i}

**Front:** {concept.get('term', 'N/A')}

**Back:** {concept.get('definition', 'N/A')}

---

"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(filepath)
    
    def create_study_schedule(self, plan: dict, filename: str = None) -> str:
        """Create printable study schedule."""
        if not filename:
            filename = f"study_schedule_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        filepath = self.export_dir / filename
        
        content = f"""# Study Schedule
Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Exam Information
- **Exam Date:** {plan.get('exam_date', 'Not set')}
- **Days Remaining:** {plan.get('days_remaining', 'N/A')}
- **Total Study Hours:** {plan.get('total_study_hours', 'N/A')}

---

## Daily Schedule

"""
        
        for day in plan.get('daily_schedule', []):
            content += f"""### {day['date']} - {day['day_name']}
**Topic:** {day['topic']}  
**Duration:** {day['duration']} hours

**Tasks:**
"""
            for task in day['tasks']:
                content += f"- {task}\n"
            
            content += "\n---\n\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(filepath)
    
    def export_progress_report(self, stats: dict, filename: str = None) -> str:
        """Export progress report."""
        if not filename:
            filename = f"progress_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = self.export_dir / filename
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'statistics': stats,
            'summary': {
                'total_study_time': f"{stats.get('total_time', 0)} minutes",
                'documents_studied': stats.get('total_documents', 0),
                'questions_answered': stats.get('total_questions', 0),
                'current_streak': f"{stats.get('streak_days', 0)} days",
                'achievements': stats.get('achievements', 0)
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        return str(filepath)
