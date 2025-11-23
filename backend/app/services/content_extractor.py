import PyPDF2
import requests
from bs4 import BeautifulSoup
import docx
import io
from typing import Dict, List, Any
import re

class ContentExtractor:
    def __init__(self):
        pass
    
    def extract_from_pdf(self, file_content: bytes) -> Dict[str, Any]:
        """Extract text and structure from PDF"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            text = ""
            metadata = {
                "pages": len(pdf_reader.pages),
                "title": pdf_reader.metadata.get('/Title', '') if pdf_reader.metadata else '',
                "author": pdf_reader.metadata.get('/Author', '') if pdf_reader.metadata else ''
            }
            
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return {
                "content": text,
                "metadata": metadata,
                "learning_objectives": self._extract_learning_objectives(text)
            }
        except Exception as e:
            raise ValueError(f"Failed to extract PDF content: {str(e)}")
    
    def extract_from_docx(self, file_content: bytes) -> Dict[str, Any]:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(io.BytesIO(file_content))
            text = ""
            
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return {
                "content": text,
                "metadata": {"paragraphs": len(doc.paragraphs)},
                "learning_objectives": self._extract_learning_objectives(text)
            }
        except Exception as e:
            raise ValueError(f"Failed to extract DOCX content: {str(e)}")
    
    def extract_from_url(self, url: str) -> Dict[str, Any]:
        """Extract content from URL"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return {
                "content": text,
                "metadata": {
                    "url": url,
                    "title": soup.title.string if soup.title else "",
                    "length": len(text)
                },
                "learning_objectives": self._extract_learning_objectives(text)
            }
        except Exception as e:
            raise ValueError(f"Failed to extract URL content: {str(e)}")
    
    def extract_from_text(self, text: str) -> Dict[str, Any]:
        """Process plain text content"""
        return {
            "content": text,
            "metadata": {"length": len(text), "words": len(text.split())},
            "learning_objectives": self._extract_learning_objectives(text)
        }
    
    def _extract_learning_objectives(self, text: str) -> List[str]:
        """Extract potential learning objectives from text"""
        objectives = []
        
        # Look for common objective patterns
        patterns = [
            r"(?:students will|learners will|objectives?:?|goals?:?|aims?:?)\s*(.+?)(?:\n|\.)",
            r"(?:understand|learn|identify|analyze|evaluate|create|apply)\s+(.+?)(?:\n|\.)",
            r"(?:by the end|after this|upon completion).+?(?:will|should|can)\s+(.+?)(?:\n|\.)"
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            objectives.extend([match.strip() for match in matches if len(match.strip()) > 10])
        
        # Remove duplicates and limit to top 5
        unique_objectives = list(dict.fromkeys(objectives))[:5]
        
        # If no objectives found, generate generic ones based on content
        if not unique_objectives:
            if "math" in text.lower() or "equation" in text.lower():
                unique_objectives = ["Solve mathematical problems", "Apply mathematical concepts"]
            elif "science" in text.lower() or "experiment" in text.lower():
                unique_objectives = ["Understand scientific concepts", "Conduct experiments"]
            else:
                unique_objectives = ["Comprehend key concepts", "Apply learned knowledge"]
        
        return unique_objectives