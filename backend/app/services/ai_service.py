import json
from typing import Dict, List, Any
import openai
import os

class AIService:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def generate_curriculum(self, content: str, subject: str, grade_level: str) -> Dict[str, Any]:
        """Generate structured curriculum from source content using Amazon Q Developer concepts"""
        
        prompt = f"""
        As an AI curriculum designer, analyze the following content and create a structured curriculum for {subject} at {grade_level} level.
        
        Content: {content[:2000]}...
        
        Generate a JSON response with:
        1. curriculum_overview: Brief description
        2. learning_objectives: List of 3-5 key objectives
        3. learning_paths: Array of 3-4 sequential learning modules with:
           - title
           - description
           - content_outline
           - estimated_duration (minutes)
           - activities
        4. assessments: Array of 2-3 assessments with:
           - title
           - type (quiz/test/assignment)
           - questions (5-10 per assessment)
        
        Focus on practical, engaging content appropriate for the grade level.
        """
        
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            # Fallback curriculum structure
            return {
                "curriculum_overview": f"AI-generated curriculum for {subject} - {grade_level}",
                "learning_objectives": [
                    "Understand core concepts",
                    "Apply knowledge practically",
                    "Develop critical thinking"
                ],
                "learning_paths": [
                    {
                        "title": "Introduction",
                        "description": "Foundation concepts",
                        "content_outline": ["Basic principles", "Key terminology"],
                        "estimated_duration": 45,
                        "activities": ["Reading", "Discussion"]
                    }
                ],
                "assessments": [
                    {
                        "title": "Knowledge Check",
                        "type": "quiz",
                        "questions": [
                            {
                                "question": "What is the main concept?",
                                "type": "multiple_choice",
                                "options": ["A", "B", "C", "D"],
                                "correct_answer": "A"
                            }
                        ]
                    }
                ]
            }
    
    async def generate_adaptive_path(self, student_performance: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate adaptive learning path based on student performance"""
        # Simplified adaptive logic for MVP
        if student_performance.get("average_score", 0) < 70:
            return [
                {"type": "review", "content": "Review fundamental concepts"},
                {"type": "practice", "content": "Additional practice exercises"}
            ]
        else:
            return [
                {"type": "advance", "content": "Advanced topics"},
                {"type": "project", "content": "Capstone project"}
            ]