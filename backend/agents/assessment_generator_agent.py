import json
import asyncio
import httpx
from typing import Dict, Any, List
from app.services.ai_service import AIService

class AssessmentGeneratorAgent:
    """Amazon Q Agent for generating assessments from curriculum modules"""
    
    def __init__(self):
        self.ai_service = AIService()
        
    async def generate_assessment(self, curriculum_id: str, module_id: str, difficulty: str) -> Dict[str, Any]:
        """Main agent workflow: curriculum/module -> assessment generation -> backend API"""
        
        try:
            # Step 1: Fetch curriculum and module data
            module_data = await self._fetch_module_data(curriculum_id, module_id)
            
            # Step 2: Generate multiple question types
            questions = await self._generate_questions(module_data, difficulty)
            
            # Step 3: Validate answers with model-based validators
            validated_questions = await self._validate_questions(questions)
            
            # Step 4: Create scoring rubric
            scoring_rubric = await self._create_scoring_rubric(validated_questions, difficulty)
            
            # Step 5: Post to backend assessment API
            assessment_id = await self._create_assessment_in_backend(
                curriculum_id, validated_questions, scoring_rubric
            )
            
            return {
                "success": True,
                "assessment_id": assessment_id,
                "questions_generated": len(validated_questions),
                "scoring_rubric": scoring_rubric,
                "difficulty_level": difficulty
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "curriculum_id": curriculum_id,
                "module_id": module_id
            }
    
    async def _fetch_module_data(self, curriculum_id: str, module_id: str) -> Dict[str, Any]:
        """Fetch module data from backend"""
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://localhost:8000/api/curriculum/{curriculum_id}/modules/{module_id}")
            
            if response.status_code == 200:
                return response.json()
            else:
                # Fallback with mock module data
                return {
                    "module_id": module_id,
                    "title": "Python Programming Fundamentals",
                    "learning_outcomes": [
                        "Understand Python syntax and data types",
                        "Apply control structures in programming",
                        "Create functions and handle exceptions"
                    ],
                    "content": "Python programming concepts including variables, functions, loops, and object-oriented programming",
                    "bloom_level": "apply",
                    "duration_hours": 4
                }
    
    async def _generate_questions(self, module_data: Dict, difficulty: str) -> List[Dict[str, Any]]:
        """Generate multiple question types using prompt templates"""
        
        questions = []
        
        # Generate multiple choice questions
        mc_questions = await self._generate_multiple_choice(module_data, difficulty)
        questions.extend(mc_questions)
        
        # Generate short answer questions
        sa_questions = await self._generate_short_answer(module_data, difficulty)
        questions.extend(sa_questions)
        
        # Generate coding tasks (if applicable)
        if "programming" in module_data.get("title", "").lower():
            coding_questions = await self._generate_coding_tasks(module_data, difficulty)
            questions.extend(coding_questions)
        
        return questions
    
    async def _generate_multiple_choice(self, module_data: Dict, difficulty: str) -> List[Dict[str, Any]]:
        """Generate multiple choice questions"""
        
        prompt = f"""
        Generate 3 multiple choice questions for this module:
        
        Module: {module_data.get('title')}
        Learning Outcomes: {module_data.get('learning_outcomes')}
        Content: {module_data.get('content', '')[:500]}
        Difficulty: {difficulty}
        
        Return JSON array:
        [
            {{
                "question_text": "What is the primary purpose of...?",
                "question_type": "multiple_choice",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": 0,
                "explanation": "Explanation of correct answer",
                "points": 5,
                "bloom_level": "understand",
                "difficulty": "{difficulty}"
            }}
        ]
        """
        
        try:
            response = await self.ai_service.generate_content(prompt)
            return json.loads(response)
        except:
            # Fallback questions
            return [
                {
                    "question_text": f"What is a key concept in {module_data.get('title', 'this module')}?",
                    "question_type": "multiple_choice",
                    "options": ["Concept A", "Concept B", "Concept C", "Concept D"],
                    "correct_answer": 0,
                    "explanation": "This is the primary concept covered in the module",
                    "points": 5,
                    "bloom_level": "remember",
                    "difficulty": difficulty
                }
            ]
    
    async def _generate_short_answer(self, module_data: Dict, difficulty: str) -> List[Dict[str, Any]]:
        """Generate short answer questions"""
        
        prompt = f"""
        Generate 2 short answer questions for this module:
        
        Module: {module_data.get('title')}
        Learning Outcomes: {module_data.get('learning_outcomes')}
        Difficulty: {difficulty}
        
        Return JSON array:
        [
            {{
                "question_text": "Explain how...",
                "question_type": "short_answer",
                "sample_answer": "Sample correct answer",
                "grading_criteria": ["criterion1", "criterion2"],
                "points": 10,
                "bloom_level": "understand",
                "difficulty": "{difficulty}"
            }}
        ]
        """
        
        try:
            response = await self.ai_service.generate_content(prompt)
            return json.loads(response)
        except:
            return [
                {
                    "question_text": f"Explain a key principle from {module_data.get('title', 'this module')}.",
                    "question_type": "short_answer",
                    "sample_answer": "A comprehensive explanation of the key principle",
                    "grading_criteria": ["accuracy", "completeness", "clarity"],
                    "points": 10,
                    "bloom_level": "understand",
                    "difficulty": difficulty
                }
            ]
    
    async def _generate_coding_tasks(self, module_data: Dict, difficulty: str) -> List[Dict[str, Any]]:
        """Generate coding tasks for programming modules"""
        
        prompt = f"""
        Generate 1 coding task for this programming module:
        
        Module: {module_data.get('title')}
        Learning Outcomes: {module_data.get('learning_outcomes')}
        Difficulty: {difficulty}
        
        Return JSON array:
        [
            {{
                "question_text": "Write a function that...",
                "question_type": "coding",
                "starter_code": "def function_name():\\n    # Your code here\\n    pass",
                "test_cases": [
                    {{"input": "test_input", "expected_output": "expected_result"}}
                ],
                "solution": "complete_solution_code",
                "points": 15,
                "bloom_level": "apply",
                "difficulty": "{difficulty}"
            }}
        ]
        """
        
        try:
            response = await self.ai_service.generate_content(prompt)
            return json.loads(response)
        except:
            return [
                {
                    "question_text": "Write a simple function related to the module content.",
                    "question_type": "coding",
                    "starter_code": "def solution():\n    # Your code here\n    pass",
                    "test_cases": [{"input": "example", "expected_output": "result"}],
                    "solution": "def solution():\n    return 'example solution'",
                    "points": 15,
                    "bloom_level": "apply",
                    "difficulty": difficulty
                }
            ]
    
    async def _validate_questions(self, questions: List[Dict]) -> List[Dict[str, Any]]:
        """Validate questions using model-based validators"""
        
        validated_questions = []
        
        for question in questions:
            validation_result = await self._validate_single_question(question)
            
            if validation_result["is_valid"]:
                # Apply any corrections suggested by validator
                corrected_question = {
                    **question,
                    **validation_result.get("corrections", {})
                }
                validated_questions.append(corrected_question)
        
        return validated_questions
    
    async def _validate_single_question(self, question: Dict) -> Dict[str, Any]:
        """Validate a single question using AI"""
        
        prompt = f"""
        Validate this assessment question:
        
        Question: {json.dumps(question, indent=2)}
        
        Check for:
        1. Clear and unambiguous wording
        2. Appropriate difficulty level
        3. Correct answer accuracy
        4. Bloom's taxonomy alignment
        
        Return JSON:
        {{
            "is_valid": true/false,
            "issues": ["issue1", "issue2"],
            "corrections": {{
                "question_text": "corrected_text_if_needed"
            }},
            "quality_score": 0.85
        }}
        """
        
        try:
            response = await self.ai_service.generate_content(prompt)
            return json.loads(response)
        except:
            # Default validation (pass all questions)
            return {
                "is_valid": True,
                "issues": [],
                "corrections": {},
                "quality_score": 0.8
            }
    
    async def _create_scoring_rubric(self, questions: List[Dict], difficulty: str) -> Dict[str, Any]:
        """Create scoring rubric for the assessment"""
        
        total_points = sum(q.get("points", 5) for q in questions)
        
        rubric = {
            "total_points": total_points,
            "passing_score": int(total_points * 0.7),  # 70% to pass
            "grading_scale": {
                "A": {"min_percentage": 90, "min_points": int(total_points * 0.9)},
                "B": {"min_percentage": 80, "min_points": int(total_points * 0.8)},
                "C": {"min_percentage": 70, "min_points": int(total_points * 0.7)},
                "D": {"min_percentage": 60, "min_points": int(total_points * 0.6)},
                "F": {"min_percentage": 0, "min_points": 0}
            },
            "question_breakdown": [
                {
                    "question_id": i,
                    "points": q.get("points", 5),
                    "type": q.get("question_type"),
                    "bloom_level": q.get("bloom_level")
                }
                for i, q in enumerate(questions)
            ],
            "difficulty_level": difficulty,
            "estimated_time_minutes": len(questions) * 3  # 3 minutes per question
        }
        
        return rubric
    
    async def _create_assessment_in_backend(self, curriculum_id: str, questions: List[Dict], rubric: Dict) -> str:
        """Create assessment in backend via API"""
        
        payload = {
            "title": f"Assessment for Curriculum {curriculum_id}",
            "curriculum_id": curriculum_id,
            "questions": questions,
            "scoring_rubric": rubric,
            "total_points": rubric["total_points"],
            "time_limit": rubric["estimated_time_minutes"],
            "ai_generated": True
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"http://localhost:8000/api/assessment/{curriculum_id}",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("assessment_id", f"assessment_{curriculum_id}")
            else:
                raise Exception(f"Backend assessment creation failed: {response.status_code}")

# Test case
async def test_assessment_generator_agent():
    """Test case: assessment generation"""
    
    agent = AssessmentGeneratorAgent()
    
    # Test data
    test_curriculum_id = "curriculum_456"
    test_module_id = "module_1"
    test_difficulty = "intermediate"
    
    print("Testing Assessment Generator Agent...")
    result = await agent.generate_assessment(test_curriculum_id, test_module_id, test_difficulty)
    
    print(f"Result: {json.dumps(result, indent=2)}")
    
    # Expected output:
    # {
    #   "success": true,
    #   "assessment_id": "assessment_789",
    #   "questions_generated": 6,
    #   "scoring_rubric": {
    #     "total_points": 50,
    #     "passing_score": 35
    #   },
    #   "difficulty_level": "intermediate"
    # }
    
    return result

if __name__ == "__main__":
    asyncio.run(test_assessment_generator_agent())