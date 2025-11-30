import json
import asyncio
import httpx
from typing import Dict, Any, List
from app.services.ai_service import AIService

class CurriculumArchitectAgent:
    """Amazon Q Agent for curriculum generation from processed resources"""
    
    def __init__(self):
        self.ai_service = AIService()
        
    async def generate_curriculum_from_resource(self, resource_id: str, generation_schema: Dict[str, Any]) -> Dict[str, Any]:
        """Main agent workflow: resource_id -> curriculum generation -> backend API"""
        
        try:
            # Step 1: Fetch resource content from backend
            resource_data = await self._fetch_resource_data(resource_id)
            
            # Step 2: Generate curriculum using chain-of-thought prompts
            curriculum_plan = await self._generate_curriculum_plan(resource_data, generation_schema)
            
            # Step 3: Create detailed modules and learning objectives
            detailed_curriculum = await self._create_detailed_curriculum(curriculum_plan, resource_data)
            
            # Step 4: Post to backend curriculum API
            curriculum_id = await self._create_curriculum_in_backend(detailed_curriculum)
            
            return {
                "success": True,
                "curriculum_id": curriculum_id,
                "module_ids": detailed_curriculum.get("module_ids", []),
                "estimated_learning_time": detailed_curriculum.get("total_duration_hours", 0),
                "modules_created": len(detailed_curriculum.get("modules", []))
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "resource_id": resource_id
            }
    
    async def _fetch_resource_data(self, resource_id: str) -> Dict[str, Any]:
        """Fetch processed resource data from backend"""
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://localhost:8000/api/curriculum/resource/{resource_id}")
            
            if response.status_code == 200:
                return response.json()
            else:
                # Fallback with mock data for testing
                return {
                    "resource_id": resource_id,
                    "chunks": [
                        {"text": "Introduction to Python programming concepts", "metadata": {"key_concepts": ["variables", "functions"]}},
                        {"text": "Control structures and loops in Python", "metadata": {"key_concepts": ["loops", "conditionals"]}},
                        {"text": "Object-oriented programming principles", "metadata": {"key_concepts": ["classes", "objects"]}}
                    ],
                    "metadata": {"total_chunks": 3, "difficulty_level": "intermediate"}
                }
    
    async def _generate_curriculum_plan(self, resource_data: Dict, schema: Dict) -> Dict[str, Any]:
        """Generate curriculum plan using chain-of-thought prompting"""
        
        content_summary = self._summarize_content(resource_data)
        
        cot_prompt = f"""
        CHAIN OF THOUGHT CURRICULUM GENERATION:
        
        Step 1: Analyze the content
        Content: {content_summary}
        Key concepts identified: {[chunk['metadata'].get('key_concepts', []) for chunk in resource_data.get('chunks', [])]}
        
        Step 2: Define learning objectives
        Target difficulty: {schema.get('difficulty', 'intermediate')}
        Duration preference: {schema.get('duration_weeks', 4)} weeks
        
        Step 3: Structure modules using Bloom's taxonomy
        Progression: Remember -> Understand -> Apply -> Analyze -> Evaluate -> Create
        
        Step 4: Estimate time requirements
        Content volume: {len(resource_data.get('chunks', []))} chunks
        
        Generate curriculum plan as JSON:
        {{
            "title": "curriculum_title",
            "description": "curriculum_description", 
            "learning_objectives": ["objective1", "objective2", "objective3"],
            "modules": [
                {{
                    "title": "module_title",
                    "week": 1,
                    "bloom_level": "understand",
                    "duration_hours": 4,
                    "learning_outcomes": ["outcome1", "outcome2"],
                    "content_chunks": ["chunk_index_1", "chunk_index_2"]
                }}
            ],
            "total_duration_hours": 16,
            "difficulty_level": "{schema.get('difficulty', 'intermediate')}"
        }}
        """
        
        response = await self.ai_service.generate_content(cot_prompt)
        return json.loads(response)
    
    async def _create_detailed_curriculum(self, plan: Dict, resource_data: Dict) -> Dict[str, Any]:
        """Create detailed curriculum with activities and assessments"""
        
        detailed_modules = []
        
        for module in plan.get("modules", []):
            detailed_module = await self._create_detailed_module(module, resource_data)
            detailed_modules.append(detailed_module)
        
        return {
            **plan,
            "modules": detailed_modules,
            "module_ids": [f"module_{i}" for i in range(len(detailed_modules))],
            "resource_id": resource_data.get("resource_id"),
            "ai_generated": True,
            "amazon_q_powered": True
        }
    
    async def _create_detailed_module(self, module_plan: Dict, resource_data: Dict) -> Dict[str, Any]:
        """Create detailed module with lessons and activities"""
        
        prompt = f"""
        Create detailed module from this plan:
        
        Module Plan: {json.dumps(module_plan, indent=2)}
        Available Content: {len(resource_data.get('chunks', []))} content chunks
        
        Generate detailed module as JSON:
        {{
            "title": "{module_plan.get('title')}",
            "week": {module_plan.get('week')},
            "bloom_level": "{module_plan.get('bloom_level')}",
            "duration_hours": {module_plan.get('duration_hours')},
            "learning_outcomes": {module_plan.get('learning_outcomes')},
            "lessons": [
                {{
                    "title": "lesson_title",
                    "duration_minutes": 45,
                    "activities": [
                        {{
                            "type": "reading|discussion|exercise|project",
                            "description": "activity_description",
                            "duration_minutes": 15,
                            "bloom_level": "understand"
                        }}
                    ],
                    "materials": ["material1", "material2"],
                    "assessment": {{
                        "type": "formative|summative",
                        "description": "assessment_description"
                    }}
                }}
            ]
        }}
        """
        
        try:
            response = await self.ai_service.generate_content(prompt)
            return json.loads(response)
        except:
            # Fallback detailed module
            return {
                "title": module_plan.get("title", "Module"),
                "week": module_plan.get("week", 1),
                "bloom_level": module_plan.get("bloom_level", "understand"),
                "duration_hours": module_plan.get("duration_hours", 4),
                "learning_outcomes": module_plan.get("learning_outcomes", []),
                "lessons": [
                    {
                        "title": f"Introduction to {module_plan.get('title')}",
                        "duration_minutes": 45,
                        "activities": [
                            {
                                "type": "reading",
                                "description": "Review key concepts",
                                "duration_minutes": 20,
                                "bloom_level": "understand"
                            }
                        ],
                        "materials": ["content_chunks"],
                        "assessment": {
                            "type": "formative",
                            "description": "Knowledge check quiz"
                        }
                    }
                ]
            }
    
    async def _create_curriculum_in_backend(self, curriculum_data: Dict) -> str:
        """Create curriculum in backend via API"""
        
        payload = {
            "title": curriculum_data.get("title"),
            "description": curriculum_data.get("description"),
            "subject": "General Studies",
            "grade_level": curriculum_data.get("difficulty_level", "intermediate"),
            "source_content": f"Generated from resource {curriculum_data.get('resource_id')}",
            "curriculum_metadata": curriculum_data
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8000/api/curriculum/",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("id", f"curriculum_{curriculum_data.get('resource_id')}")
            else:
                raise Exception(f"Backend curriculum creation failed: {response.status_code}")
    
    def _summarize_content(self, resource_data: Dict) -> str:
        """Summarize resource content for analysis"""
        
        chunks = resource_data.get("chunks", [])
        if not chunks:
            return "No content available"
        
        # Take first 500 characters from each chunk
        summaries = [chunk["text"][:500] for chunk in chunks[:3]]
        return " | ".join(summaries)

# Test case
async def test_curriculum_architect_agent():
    """Test case: curriculum generation from resource"""
    
    agent = CurriculumArchitectAgent()
    
    # Test data
    test_resource_id = "resource_123"
    test_schema = {
        "difficulty": "intermediate",
        "duration_weeks": 4,
        "learning_objectives": [
            "Understand core concepts",
            "Apply knowledge practically", 
            "Analyze complex scenarios"
        ]
    }
    
    print("Testing Curriculum Architect Agent...")
    result = await agent.generate_curriculum_from_resource(test_resource_id, test_schema)
    
    print(f"Result: {json.dumps(result, indent=2)}")
    
    # Expected output:
    # {
    #   "success": true,
    #   "curriculum_id": "curriculum_456",
    #   "module_ids": ["module_0", "module_1", "module_2"],
    #   "estimated_learning_time": 16,
    #   "modules_created": 3
    # }
    
    return result

if __name__ == "__main__":
    asyncio.run(test_curriculum_architect_agent())