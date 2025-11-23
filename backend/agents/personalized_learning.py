import json
import yaml
from typing import Dict, List, Any
from ..services.ai_service import AIService

class PersonalizedLearningAgent:
    def __init__(self):
        self.ai_service = AIService()
        with open('agents/kiro_config.yaml', 'r') as f:
            self.config = yaml.safe_load(f)
    
    async def generate_learning_path(self, student_profile: Dict[str, Any], curriculum: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized learning path based on student profile"""
        
        prompt = f"""
        Create a personalized learning path for this student using the curriculum.
        
        Student Profile: {json.dumps(student_profile, indent=2)}
        Curriculum: {json.dumps(curriculum, indent=2)}
        
        Consider:
        - Learning style preferences
        - Current skill level
        - Performance history
        - Time availability
        - Learning goals
        
        Output JSON:
        {{
            "student_id": "{student_profile.get('id')}",
            "path_id": "generated_path_id",
            "estimated_duration": "weeks",
            "difficulty_level": "beginner|intermediate|advanced",
            "learning_style": "visual|auditory|kinesthetic|mixed",
            "modules": [
                {{
                    "module_id": "module_1",
                    "sequence": 1,
                    "estimated_hours": 8,
                    "prerequisites_met": true,
                    "difficulty_adjustment": "standard|simplified|enhanced",
                    "recommended_activities": ["activity1", "activity2"],
                    "skip_if_mastered": false,
                    "additional_resources": ["resource1"]
                }}
            ],
            "milestones": [
                {{
                    "week": 2,
                    "checkpoint": "module_1_completion",
                    "assessment_required": true,
                    "mastery_threshold": 80
                }}
            ],
            "adaptations": {{
                "content_format": "text|video|interactive",
                "pace": "self_paced|structured|accelerated",
                "support_level": "minimal|moderate|high"
            }}
        }}
        """
        
        response = await self.ai_service.generate_content(prompt)
        return json.loads(response)
    
    async def adapt_content_difficulty(self, content: Dict[str, Any], student_performance: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt content difficulty based on student performance"""
        
        prompt = f"""
        Adapt this content based on student performance data.
        
        Content: {json.dumps(content, indent=2)}
        Performance: {json.dumps(student_performance, indent=2)}
        
        Performance Analysis:
        - Average Score: {student_performance.get('average_score', 0)}%
        - Struggle Areas: {student_performance.get('struggle_areas', [])}
        - Strong Areas: {student_performance.get('strong_areas', [])}
        - Learning Velocity: {student_performance.get('learning_velocity', 'normal')}
        
        Adaptation Rules:
        - If avg_score < 60%: Simplify content, add scaffolding
        - If avg_score > 85%: Add challenge activities, accelerate pace
        - If struggle_areas identified: Provide remediation
        
        Return adapted content with same structure but modified difficulty.
        """
        
        response = await self.ai_service.generate_content(prompt)
        return json.loads(response)
    
    async def recommend_next_activities(self, student_id: str, current_progress: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recommend next learning activities based on progress"""
        
        prompt = f"""
        Recommend next learning activities for student based on current progress.
        
        Student ID: {student_id}
        Current Progress: {json.dumps(current_progress, indent=2)}
        
        Consider:
        - Completed modules and scores
        - Time spent on activities
        - Identified knowledge gaps
        - Learning preferences
        - Upcoming deadlines
        
        Return JSON array:
        [
            {{
                "activity_type": "review|practice|assessment|project",
                "title": "activity_title",
                "description": "what_student_will_do",
                "estimated_time": "minutes",
                "priority": "high|medium|low",
                "reason": "why_recommended",
                "resources": ["resource1", "resource2"],
                "success_criteria": "how_to_measure_completion"
            }}
        ]
        """
        
        response = await self.ai_service.generate_content(prompt)
        return json.loads(response)
    
    async def generate_remediation_plan(self, student_id: str, weak_areas: List[str]) -> Dict[str, Any]:
        """Generate remediation plan for identified weak areas"""
        
        prompt = f"""
        Create a remediation plan for student's weak areas.
        
        Student ID: {student_id}
        Weak Areas: {weak_areas}
        
        For each weak area, provide:
        - Root cause analysis
        - Targeted interventions
        - Practice activities
        - Assessment checkpoints
        - Timeline for improvement
        
        Return JSON:
        {{
            "student_id": "{student_id}",
            "remediation_plan": {{
                "weak_area_1": {{
                    "root_causes": ["cause1", "cause2"],
                    "interventions": [
                        {{
                            "type": "review|practice|tutoring",
                            "description": "intervention_description",
                            "duration": "time_needed",
                            "resources": ["resource1"]
                        }}
                    ],
                    "checkpoints": [
                        {{
                            "week": 1,
                            "assessment": "checkpoint_assessment",
                            "target_score": 75
                        }}
                    ]
                }}
            }},
            "overall_timeline": "weeks_to_completion",
            "success_metrics": ["metric1", "metric2"]
        }}
        """
        
        response = await self.ai_service.generate_content(prompt)
        return json.loads(response)
    
    async def optimize_learning_sequence(self, modules: List[Dict], student_profile: Dict) -> List[Dict]:
        """Optimize module sequence based on student profile"""
        
        prompt = f"""
        Optimize the learning sequence of these modules for this student.
        
        Modules: {json.dumps(modules, indent=2)}
        Student Profile: {json.dumps(student_profile, indent=2)}
        
        Consider:
        - Prerequisites and dependencies
        - Student's prior knowledge
        - Learning style preferences
        - Available time constraints
        - Motivation and engagement factors
        
        Return optimized sequence with rationale for changes.
        """
        
        response = await self.ai_service.generate_content(prompt)
        return json.loads(response)