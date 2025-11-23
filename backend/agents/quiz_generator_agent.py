import json
import random
from typing import Dict, Any, List

class QuizGeneratorAgent:
    """AI agent for generating personalized quizzes"""
    
    def __init__(self):
        self.question_templates = self._load_question_templates()
        
    def generate_quiz(self, quiz_params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI-powered quiz based on parameters"""
        
        topic = quiz_params["topic"]
        difficulty = quiz_params["difficulty"]
        question_count = quiz_params.get("question_count", 10)
        question_types = quiz_params.get("question_types", ["mcq", "short_answer"])
        
        # Generate questions
        questions = self._generate_questions(
            topic, difficulty, question_count, question_types
        )
        
        # Calculate time limit
        time_limit = self._calculate_time_limit(questions)
        
        return {
            "title": f"{topic} Quiz",
            "description": f"Test your knowledge of {topic} concepts",
            "questions": questions,
            "time_limit": time_limit,
            "total_points": sum(q.get("points", 5) for q in questions),
            "difficulty": difficulty
        }
    
    def _generate_questions(self, topic: str, difficulty: str, 
                          count: int, types: List[str]) -> List[Dict[str, Any]]:
        """Generate questions for the quiz"""
        
        questions = []
        
        # Determine question distribution
        mcq_count = int(count * 0.7) if "mcq" in types else 0
        short_count = count - mcq_count if "short_answer" in types else 0
        
        # Generate MCQs
        for i in range(mcq_count):
            question = self._generate_mcq(topic, difficulty)
            questions.append(question)
        
        # Generate short answer questions
        for i in range(short_count):
            question = self._generate_short_answer(topic, difficulty)
            questions.append(question)
        
        # Shuffle questions
        random.shuffle(questions)
        
        return questions
    
    def _generate_mcq(self, topic: str, difficulty: str) -> Dict[str, Any]:
        """Generate multiple choice question"""
        
        # Topic-specific question templates
        templates = self.question_templates.get(topic.lower(), {})
        mcq_templates = templates.get("mcq", [])
        
        if not mcq_templates:
            # Fallback generic questions
            mcq_templates = self._get_generic_mcq_templates(topic)
        
        # Select template based on difficulty
        template = self._select_template_by_difficulty(mcq_templates, difficulty)
        
        return {
            "type": "mcq",
            "question": template["question"],
            "options": template["options"],
            "correct": template["correct"],
            "explanation": template["explanation"],
            "points": self._get_points_by_difficulty(difficulty),
            "difficulty": difficulty
        }
    
    def _generate_short_answer(self, topic: str, difficulty: str) -> Dict[str, Any]:
        """Generate short answer question"""
        
        templates = self.question_templates.get(topic.lower(), {})
        short_templates = templates.get("short_answer", [])
        
        if not short_templates:
            short_templates = self._get_generic_short_templates(topic)
        
        template = self._select_template_by_difficulty(short_templates, difficulty)
        
        return {
            "type": "short_answer",
            "question": template["question"],
            "correct": template["correct"],
            "explanation": template["explanation"],
            "points": self._get_points_by_difficulty(difficulty) + 2,
            "difficulty": difficulty
        }
    
    def _load_question_templates(self) -> Dict[str, Any]:
        """Load question templates for different topics"""
        
        return {
            "linear equations": {
                "mcq": [
                    {
                        "question": "Solve for x: 2x + 5 = 13",
                        "options": ["x = 3", "x = 4", "x = 5", "x = 6"],
                        "correct": 1,
                        "explanation": "Subtract 5 from both sides: 2x = 8, then divide by 2: x = 4",
                        "difficulty": "beginner"
                    },
                    {
                        "question": "What is the slope of the line y = 3x - 2?",
                        "options": ["3", "-2", "1", "0"],
                        "correct": 0,
                        "explanation": "In the form y = mx + b, the coefficient of x (3) is the slope",
                        "difficulty": "beginner"
                    }
                ],
                "short_answer": [
                    {
                        "question": "Find the y-intercept of the equation y = -2x + 7",
                        "correct": "7",
                        "explanation": "The y-intercept is the constant term when x = 0, which is 7",
                        "difficulty": "beginner"
                    }
                ]
            },
            "quadratic functions": {
                "mcq": [
                    {
                        "question": "What is the vertex form of a quadratic function?",
                        "options": ["y = ax² + bx + c", "y = a(x - h)² + k", "y = a(x + h)² - k", "y = ax + b"],
                        "correct": 1,
                        "explanation": "Vertex form is y = a(x - h)² + k where (h, k) is the vertex",
                        "difficulty": "intermediate"
                    }
                ],
                "short_answer": [
                    {
                        "question": "Find the vertex of y = x² - 4x + 3",
                        "correct": "(2, -1)",
                        "explanation": "Complete the square or use h = -b/2a = 4/2 = 2, then k = f(2) = -1",
                        "difficulty": "intermediate"
                    }
                ]
            },
            "physics motion": {
                "mcq": [
                    {
                        "question": "What is the SI unit of acceleration?",
                        "options": ["m/s", "m/s²", "kg⋅m/s", "N"],
                        "correct": 1,
                        "explanation": "Acceleration is change in velocity over time, so units are m/s²",
                        "difficulty": "beginner"
                    }
                ],
                "short_answer": [
                    {
                        "question": "Calculate the acceleration of an object that goes from 0 to 20 m/s in 4 seconds",
                        "correct": "5 m/s²",
                        "explanation": "a = (v_f - v_i)/t = (20 - 0)/4 = 5 m/s²",
                        "difficulty": "intermediate"
                    }
                ]
            }
        }
    
    def _get_generic_mcq_templates(self, topic: str) -> List[Dict[str, Any]]:
        """Generate generic MCQ templates for unknown topics"""
        
        return [
            {
                "question": f"Which of the following is a key concept in {topic}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct": 0,
                "explanation": f"This tests basic knowledge of {topic}",
                "difficulty": "beginner"
            },
            {
                "question": f"What is the most important application of {topic}?",
                "options": ["Application A", "Application B", "Application C", "Application D"],
                "correct": 1,
                "explanation": f"This explores practical uses of {topic}",
                "difficulty": "intermediate"
            }
        ]
    
    def _get_generic_short_templates(self, topic: str) -> List[Dict[str, Any]]:
        """Generate generic short answer templates"""
        
        return [
            {
                "question": f"Define {topic} in your own words",
                "correct": f"A fundamental concept in mathematics/science",
                "explanation": f"This tests understanding of {topic} definition",
                "difficulty": "beginner"
            },
            {
                "question": f"Explain how {topic} is used in real-world applications",
                "correct": f"Used in various practical scenarios",
                "explanation": f"This tests application knowledge of {topic}",
                "difficulty": "intermediate"
            }
        ]
    
    def _select_template_by_difficulty(self, templates: List[Dict], difficulty: str) -> Dict[str, Any]:
        """Select appropriate template based on difficulty"""
        
        # Filter by difficulty if available
        filtered = [t for t in templates if t.get("difficulty") == difficulty]
        
        if filtered:
            return random.choice(filtered)
        else:
            return random.choice(templates) if templates else {}
    
    def _get_points_by_difficulty(self, difficulty: str) -> int:
        """Get points based on difficulty level"""
        
        points_map = {
            "beginner": 3,
            "intermediate": 5,
            "advanced": 8
        }
        
        return points_map.get(difficulty, 5)
    
    def _calculate_time_limit(self, questions: List[Dict[str, Any]]) -> int:
        """Calculate appropriate time limit for quiz"""
        
        base_time_per_question = {
            "mcq": 1.5,  # 1.5 minutes per MCQ
            "short_answer": 3.0  # 3 minutes per short answer
        }
        
        total_time = 0
        for question in questions:
            q_type = question.get("type", "mcq")
            total_time += base_time_per_question.get(q_type, 2.0)
        
        # Add buffer time (20% extra)
        total_time *= 1.2
        
        # Round to nearest 5 minutes
        return max(10, int(total_time / 5) * 5)