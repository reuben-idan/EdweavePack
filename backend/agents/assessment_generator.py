import json
import yaml
from typing import Dict, List, Any
from app.services.ai_service import AIService

class AssessmentGeneratorAgent:
    def __init__(self):
        self.ai_service = AIService()
        with open('agents/kiro_config.yaml', 'r') as f:
            self.config = yaml.safe_load(f)
    
    async def generate_assessment(self, module: Dict[str, Any], assessment_type: str = "mixed") -> Dict[str, Any]:
        """Generate comprehensive assessment with rubrics"""
        
        prompt = f"""
        Generate a comprehensive assessment for this curriculum module using Amazon Q Developer.
        
        Module: {json.dumps(module, indent=2)}
        Assessment Type: {assessment_type}
        
        Create questions that test different Bloom's taxonomy levels:
        - Multiple Choice (remember, understand)
        - Short Answer (understand, apply)
        - Essay/Project (analyze, evaluate, create)
        - Coding/Practical (apply, analyze, create)
        
        Output as JSON:
        {{
            "title": "assessment_title",
            "module_id": "{module.get('id', '')}",
            "bloom_level": "{module.get('bloom_level', 'apply')}",
            "duration_minutes": 60,
            "total_points": 100,
            "questions": [
                {{
                    "id": 1,
                    "type": "multiple_choice",
                    "bloom_level": "remember",
                    "question": "question_text",
                    "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
                    "correct_answer": "A",
                    "points": 10,
                    "explanation": "why_this_answer"
                }},
                {{
                    "id": 2,
                    "type": "short_answer",
                    "bloom_level": "understand",
                    "question": "question_text",
                    "sample_answer": "expected_response",
                    "points": 15,
                    "rubric": {{
                        "excellent": "criteria_for_excellent",
                        "good": "criteria_for_good",
                        "satisfactory": "criteria_for_satisfactory",
                        "needs_improvement": "criteria_for_improvement"
                    }}
                }},
                {{
                    "id": 3,
                    "type": "essay",
                    "bloom_level": "evaluate",
                    "question": "question_text",
                    "points": 25,
                    "rubric": {{
                        "content": {{
                            "excellent": "demonstrates_mastery",
                            "good": "shows_understanding",
                            "satisfactory": "basic_grasp",
                            "needs_improvement": "limited_understanding"
                        }},
                        "analysis": {{
                            "excellent": "deep_critical_thinking",
                            "good": "some_analysis",
                            "satisfactory": "basic_analysis",
                            "needs_improvement": "minimal_analysis"
                        }}
                    }}
                }}
            ],
            "rubric": {{
                "grading_scale": {{
                    "A": "90-100",
                    "B": "80-89",
                    "C": "70-79",
                    "D": "60-69",
                    "F": "0-59"
                }},
                "criteria": {{
                    "knowledge": "demonstrates_understanding_of_concepts",
                    "application": "applies_concepts_correctly",
                    "analysis": "analyzes_information_effectively",
                    "communication": "communicates_ideas_clearly"
                }}
            }}
        }}
        """
        
        response = await self.ai_service.generate_content(prompt)
        return json.loads(response)
    
    async def generate_rubric(self, question: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed rubric for specific question"""
        
        prompt = f"""
        Create a detailed rubric for this assessment question:
        
        Question: {json.dumps(question, indent=2)}
        
        Generate rubric with 4 performance levels and specific criteria.
        
        Return JSON:
        {{
            "question_id": {question.get('id')},
            "rubric": {{
                "excellent": {{
                    "points": "90-100%",
                    "criteria": "specific_criteria_for_excellent"
                }},
                "good": {{
                    "points": "80-89%",
                    "criteria": "specific_criteria_for_good"
                }},
                "satisfactory": {{
                    "points": "70-79%",
                    "criteria": "specific_criteria_for_satisfactory"
                }},
                "needs_improvement": {{
                    "points": "0-69%",
                    "criteria": "specific_criteria_for_improvement"
                }}
            }}
        }}
        """
        
        response = await self.ai_service.generate_content(prompt)
        return json.loads(response)
    
    async def calibrate_difficulty(self, questions: List[Dict], target_difficulty: str) -> List[Dict]:
        """Calibrate question difficulty based on target level"""
        
        prompt = f"""
        Adjust these assessment questions to match target difficulty: {target_difficulty}
        
        Questions: {json.dumps(questions, indent=2)}
        
        Difficulty Levels:
        - beginner: Simple recall and basic understanding
        - intermediate: Application and analysis
        - advanced: Evaluation and creation
        
        Return modified questions with adjusted complexity, vocabulary, and cognitive load.
        """
        
        response = await self.ai_service.generate_content(prompt)
        return json.loads(response)
    
    async def generate_question_bank(self, topic: str, bloom_level: str, count: int = 10) -> List[Dict]:
        """Generate question bank for specific topic and Bloom level"""
        
        prompt = f"""
        Generate {count} assessment questions for topic: {topic}
        Bloom's Taxonomy Level: {bloom_level}
        
        Mix question types: multiple choice, short answer, essay, practical
        
        Return JSON array of questions with format:
        [
            {{
                "type": "question_type",
                "bloom_level": "{bloom_level}",
                "question": "question_text",
                "difficulty": "beginner|intermediate|advanced",
                "estimated_time": "minutes",
                "points": "suggested_points"
            }}
        ]
        """
        
        response = await self.ai_service.generate_content(prompt)
        return json.loads(response)