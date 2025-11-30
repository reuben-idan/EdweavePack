import io
import logging
from typing import Optional
import PyPDF2
from docx import Document

logger = logging.getLogger(__name__)

class ContentExtractor:
    """Content extraction service for various file formats"""
    
    def extract_from_pdf(self, content: bytes) -> str:
        """Extract text from PDF content"""
        try:
            pdf_file = io.BytesIO(content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"PDF extraction error: {e}")
            return "PDF content extraction failed - using fallback processing"
    
    def extract_from_docx(self, content: bytes) -> str:
        """Extract text from DOCX content"""
        try:
            docx_file = io.BytesIO(content)
            doc = Document(docx_file)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"DOCX extraction error: {e}")
            return "DOCX content extraction failed - using fallback processing"
    
    def extract_from_text(self, content: bytes) -> str:
        """Extract text from plain text files"""
        try:
            return content.decode('utf-8')
        except Exception as e:
            logger.error(f"Text extraction error: {e}")
            return "Text content extraction failed"
    
    def analyze_content(self, text: str) -> dict:
        """Analyze extracted content for AI processing"""
        word_count = len(text.split())
        char_count = len(text)
        
        # Simple content analysis
        analysis = {
            "word_count": word_count,
            "character_count": char_count,
            "estimated_reading_time": max(1, word_count // 200),
            "content_type": self._detect_content_type(text),
            "complexity_level": self._assess_complexity(text),
            "key_topics": self._extract_key_topics(text)
        }
        
        return analysis
    
    def _detect_content_type(self, text: str) -> str:
        """Detect the type of educational content"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['algorithm', 'programming', 'code', 'function']):
            return "computer_science"
        elif any(word in text_lower for word in ['equation', 'formula', 'calculate', 'mathematics']):
            return "mathematics"
        elif any(word in text_lower for word in ['experiment', 'hypothesis', 'theory', 'science']):
            return "science"
        elif any(word in text_lower for word in ['history', 'historical', 'century', 'period']):
            return "history"
        else:
            return "general_education"
    
    def _assess_complexity(self, text: str) -> str:
        """Assess content complexity level"""
        words = text.split()
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        
        if avg_word_length < 4:
            return "elementary"
        elif avg_word_length < 5.5:
            return "intermediate"
        else:
            return "advanced"
    
    def _extract_key_topics(self, text: str) -> list:
        """Extract key topics from content"""
        # Simple keyword extraction
        words = text.lower().split()
        
        # Filter out common words and get meaningful terms
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'}
        
        meaningful_words = [word for word in words if len(word) > 4 and word not in stop_words and word.isalpha()]
        
        # Get most frequent meaningful words as topics
        word_freq = {}
        for word in meaningful_words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Return top 5 most frequent words as key topics
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:5]]