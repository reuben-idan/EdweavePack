import yaml
import json
from typing import Dict, List, Any
from ..services.ai_service import AIService

class CurriculumArchitectAgent:
    def __init__(self):
        self.ai_service = AIService()
        with open('agents/kiro_config.yaml', 'r') as f:
            self.config = yaml.safe_load(f)
    
    async def generate_curriculum(self, content: str, level: str, subject: str) -> Dict[str, Any]:
        """Generate curriculum using Kiro + Q orchestration"""
        
        template = self.config['templates'].get(level, self.config['templates']['university'])
        pedagogy = self.config['pedagogy']
        
        prompt = f"""
        Generate a {pedagogy['module_count']}-week modular curriculum from this content, aligned to Bloom's taxonomy.
        
        Content: {content}
        Subject: {subject}
        Education Level: {level}
        
        Pedagogical Framework:
        - Bloom Levels: {template['bloom_emphasis']}
        - Activity Types: {template['activity_preference']}
        - Focus: {template['focus']}
        - Lessons per week: {pedagogy['weekly_structure']['lessons_per_week']}
        - Assessments per week: {pedagogy['weekly_structure']['assessments_per_week']}
        
        Output as JSON with this structure:
        {{
            "title": "curriculum_title",
            "description": "curriculum_description",
            "level": "{level}",
            "subject": "{subject}",
            "duration_weeks": {pedagogy['module_count']},
            "modules": [
                {{
                    "title": "module_title",
                    "week": 1,
                    "bloom_level": "apply",
                    "learning_objectives": ["objective1", "objective2"],
                    "lessons": [
                        {{
                            "title": "lesson_title",
                            "duration_minutes": 45,
                            "bloom_level": "understand",
                            "objectives": ["objective"],
                            "activities": [
                                {{
                                    "type": "lecture",
                                    "description": "activity_description",
                                    "duration_minutes": 15
                                }}
                            ],
                            "materials": ["material1"],
                            "prerequisites": ["prerequisite1"]
                        }}
                    ]
                }}
            ]
        }}
        """
        
        response = await self.ai_service.generate_content(prompt)
        return json.loads(response)
    
    async def align_to_bloom_taxonomy(self, objectives: List[str], target_level: str) -> List[Dict[str, Any]]:
        """Align learning objectives to specific Bloom's taxonomy level"""
        
        bloom_verbs = {
            'remember': ['define', 'list', 'recall', 'identify', 'name'],
            'understand': ['explain', 'describe', 'summarize', 'interpret', 'classify'],
            'apply': ['demonstrate', 'solve', 'use', 'implement', 'execute'],
            'analyze': ['compare', 'contrast', 'examine', 'categorize', 'differentiate'],
            'evaluate': ['assess', 'critique', 'judge', 'justify', 'validate'],
            'create': ['design', 'develop', 'compose', 'construct', 'formulate']
        }
        
        prompt = f"""
        Rewrite these learning objectives to align with Bloom's taxonomy level: {target_level}
        
        Use these action verbs: {bloom_verbs[target_level]}
        
        Original objectives: {objectives}
        
        Return JSON array of aligned objectives with format:
        [
            {{
                "original": "original_objective",
                "aligned": "aligned_objective",
                "bloom_level": "{target_level}",
                "action_verb": "chosen_verb"
            }}
        ]
        """
        
        response = await self.ai_service.generate_content(prompt)
        return json.loads(response)
    
    async def generate_prerequisite_map(self, modules: List[Dict]) -> Dict[str, List[str]]:
        """Generate prerequisite mapping between modules"""
        
        prompt = f"""
        Analyze these curriculum modules and create a prerequisite map.
        
        Modules: {json.dumps(modules, indent=2)}
        
        Return JSON with format:
        {{
            "module_1": ["prerequisite_module_1", "prerequisite_module_2"],
            "module_2": ["prerequisite_module_1"],
            "module_3": []
        }}
        """
        
        response = await self.ai_service.generate_content(prompt)
        return json.loads(response)