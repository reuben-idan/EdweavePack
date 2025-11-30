import boto3
import json
from typing import Dict, List, Any, Optional
import logging
import asyncio

logger = logging.getLogger(__name__)

class QAssistantService:
    """Amazon Q Apps integration for in-app AI assistance"""
    
    def __init__(self, region: str = "us-east-1"):
        self.region = region
        self.bedrock = boto3.client('bedrock-runtime', region_name=region)
        
        # Q Assistant contexts for different user roles
        self.contexts = {
            "teacher": {
                "role": "AI Teaching Assistant",
                "expertise": ["curriculum design", "assessment creation", "student analytics", "pedagogical strategies"],
                "capabilities": ["content generation", "grading assistance", "learning insights", "differentiation strategies"]
            },
            "student": {
                "role": "AI Learning Companion", 
                "expertise": ["concept explanation", "study strategies", "progress tracking", "motivation"],
                "capabilities": ["tutoring", "practice questions", "study planning", "learning tips"]
            },
            "curriculum_creator": {
                "role": "AI Curriculum Specialist",
                "expertise": ["standards alignment", "content organization", "quality assurance", "accessibility"],
                "capabilities": ["content analysis", "structure optimization", "compliance checking", "enhancement suggestions"]
            }
        }
    
    async def chat_with_q(self, user_role: str, message: str, context: Dict = None) -> Dict[str, Any]:
        """Main Q Assistant chat interface"""
        
        assistant_context = self.contexts.get(user_role, self.contexts["teacher"])
        
        # Build context-aware prompt
        system_prompt = f"""
        You are {assistant_context['role']} for EdweavePack, an AI-powered educational platform.
        
        Your expertise includes: {', '.join(assistant_context['expertise'])}
        Your capabilities: {', '.join(assistant_context['capabilities'])}
        
        Current context: {json.dumps(context or {}, indent=2) if context else 'No specific context'}
        
        Provide helpful, accurate, and actionable responses. Be encouraging and educational.
        Keep responses concise but comprehensive. Always consider the user's role and needs.
        """
        
        full_prompt = f"{system_prompt}\n\nUser: {message}\n\nAssistant:"
        
        try:
            response = self.bedrock.invoke_model(
                modelId="anthropic.claude-3-sonnet-20240229-v1:0",
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 2000,
                    "messages": [
                        {"role": "user", "content": full_prompt}
                    ]
                })
            )
            
            result = json.loads(response['body'].read())
            assistant_response = result['content'][0]['text']
            
            return {
                "response": assistant_response,
                "role": assistant_context['role'],
                "suggestions": await self._generate_follow_up_suggestions(user_role, message, assistant_response),
                "actions": await self._suggest_actions(user_role, message, context)
            }
            
        except Exception as e:
            logger.error(f"Q Assistant chat failed: {e}")
            return {
                "response": "I'm having trouble processing your request right now. Please try again.",
                "error": str(e)
            }
    
    async def get_teaching_suggestions(self, curriculum_data: Dict, student_performance: List[Dict] = None) -> Dict[str, Any]:
        """Generate teaching suggestions based on curriculum and performance data"""
        
        prompt = f"""
        As an AI Teaching Assistant, analyze this curriculum and student performance data to provide teaching suggestions.
        
        Curriculum: {json.dumps(curriculum_data, indent=2)[:1500]}
        Student Performance: {json.dumps(student_performance or [], indent=2)[:1000]}
        
        Provide:
        1. Teaching strategies for this content
        2. Differentiation recommendations
        3. Assessment suggestions
        4. Technology integration ideas
        5. Common misconceptions to address
        6. Extension activities for advanced learners
        
        Return as structured JSON with actionable recommendations.
        """
        
        try:
            response = self.bedrock.invoke_model(
                modelId="anthropic.claude-3-sonnet-20240229-v1:0",
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 2500,
                    "messages": [{"role": "user", "content": prompt}]
                })
            )
            
            result = json.loads(response['body'].read())
            suggestions_text = result['content'][0]['text']
            
            try:
                suggestions = json.loads(suggestions_text)
                return suggestions
            except:
                return {
                    "teaching_strategies": suggestions_text[:500],
                    "differentiation": "Provide multiple learning modalities",
                    "assessment": "Use formative and summative assessments",
                    "technology": "Integrate interactive tools",
                    "misconceptions": "Address common errors proactively",
                    "extensions": "Offer challenge activities"
                }
                
        except Exception as e:
            logger.error(f"Teaching suggestions failed: {e}")
            return {"error": str(e)}
    
    async def explain_concept(self, concept: str, grade_level: str, learning_style: str = "mixed") -> Dict[str, Any]:
        """Explain concepts in student-friendly language"""
        
        prompt = f"""
        As an AI Learning Companion, explain this concept to a {grade_level} student with {learning_style} learning preferences.
        
        Concept: {concept}
        
        Provide:
        1. Simple, clear explanation
        2. Real-world examples
        3. Visual/auditory/kinesthetic elements (based on learning style)
        4. Practice questions
        5. Memory aids or mnemonics
        6. Common mistakes to avoid
        
        Make it engaging and age-appropriate.
        """
        
        try:
            response = self.bedrock.invoke_model(
                modelId="anthropic.claude-3-sonnet-20240229-v1:0",
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 2000,
                    "messages": [{"role": "user", "content": prompt}]
                })
            )
            
            result = json.loads(response['body'].read())
            explanation = result['content'][0]['text']
            
            return {
                "explanation": explanation,
                "concept": concept,
                "grade_level": grade_level,
                "learning_style": learning_style,
                "follow_up_questions": await self._generate_practice_questions(concept, grade_level)
            }
            
        except Exception as e:
            logger.error(f"Concept explanation failed: {e}")
            return {"error": str(e)}
    
    async def generate_study_plan(self, student_goals: List[str], available_time: int, current_level: str) -> Dict[str, Any]:
        """Generate personalized study plans"""
        
        prompt = f"""
        Create a personalized study plan for a student with these parameters:
        
        Goals: {', '.join(student_goals)}
        Available time per week: {available_time} hours
        Current level: {current_level}
        
        Create a structured plan with:
        1. Weekly schedule breakdown
        2. Daily study activities
        3. Progress milestones
        4. Review sessions
        5. Assessment checkpoints
        6. Motivation strategies
        
        Return as JSON with detailed schedule.
        """
        
        try:
            response = self.bedrock.invoke_model(
                modelId="anthropic.claude-3-sonnet-20240229-v1:0",
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 2500,
                    "messages": [{"role": "user", "content": prompt}]
                })
            )
            
            result = json.loads(response['body'].read())
            plan_text = result['content'][0]['text']
            
            try:
                study_plan = json.loads(plan_text)
                return study_plan
            except:
                return {
                    "weekly_schedule": plan_text[:1000],
                    "daily_activities": "Structured learning activities",
                    "milestones": "Weekly progress checkpoints",
                    "review_sessions": "Regular review and practice",
                    "assessments": "Self-assessment opportunities"
                }
                
        except Exception as e:
            logger.error(f"Study plan generation failed: {e}")
            return {"error": str(e)}
    
    async def analyze_curriculum_quality(self, curriculum_content: Dict) -> Dict[str, Any]:
        """Analyze curriculum quality and provide improvement suggestions"""
        
        prompt = f"""
        As an AI Curriculum Specialist, analyze this curriculum for quality and compliance.
        
        Curriculum: {json.dumps(curriculum_content, indent=2)[:2000]}
        
        Evaluate:
        1. Standards alignment
        2. Learning objective clarity
        3. Assessment alignment
        4. Differentiation provisions
        5. Technology integration
        6. Accessibility considerations
        7. Scope and sequence logic
        
        Provide specific improvement recommendations.
        """
        
        try:
            response = self.bedrock.invoke_model(
                modelId="anthropic.claude-3-sonnet-20240229-v1:0",
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 2500,
                    "messages": [{"role": "user", "content": prompt}]
                })
            )
            
            result = json.loads(response['body'].read())
            analysis_text = result['content'][0]['text']
            
            try:
                analysis = json.loads(analysis_text)
                return analysis
            except:
                return {
                    "overall_quality": "Good foundation with areas for improvement",
                    "standards_alignment": "Partially aligned, needs review",
                    "recommendations": analysis_text[:1000],
                    "priority_improvements": ["Clarify learning objectives", "Add differentiation strategies"]
                }
                
        except Exception as e:
            logger.error(f"Curriculum analysis failed: {e}")
            return {"error": str(e)}
    
    async def _generate_follow_up_suggestions(self, user_role: str, original_message: str, response: str) -> List[str]:
        """Generate contextual follow-up suggestions"""
        
        suggestions_map = {
            "teacher": [
                "How can I differentiate this for struggling learners?",
                "What assessment strategies would work best?",
                "Can you suggest technology tools for this topic?",
                "How do I address common misconceptions?"
            ],
            "student": [
                "Can you explain this concept differently?",
                "What are some practice problems I can try?",
                "How does this connect to real life?",
                "What should I study next?"
            ],
            "curriculum_creator": [
                "How can I improve the alignment with standards?",
                "What accessibility features should I add?",
                "Can you suggest better assessment methods?",
                "How can I make this more engaging?"
            ]
        }
        
        return suggestions_map.get(user_role, suggestions_map["teacher"])[:3]
    
    async def _suggest_actions(self, user_role: str, message: str, context: Dict = None) -> List[Dict]:
        """Suggest actionable next steps"""
        
        actions_map = {
            "teacher": [
                {"action": "create_assessment", "label": "Create Assessment", "icon": "quiz"},
                {"action": "view_analytics", "label": "View Student Analytics", "icon": "chart"},
                {"action": "generate_content", "label": "Generate Content", "icon": "create"}
            ],
            "student": [
                {"action": "practice_quiz", "label": "Take Practice Quiz", "icon": "quiz"},
                {"action": "study_plan", "label": "Update Study Plan", "icon": "calendar"},
                {"action": "ask_question", "label": "Ask Another Question", "icon": "help"}
            ],
            "curriculum_creator": [
                {"action": "analyze_content", "label": "Analyze Content", "icon": "analyze"},
                {"action": "check_alignment", "label": "Check Standards Alignment", "icon": "check"},
                {"action": "improve_accessibility", "label": "Improve Accessibility", "icon": "accessibility"}
            ]
        }
        
        return actions_map.get(user_role, actions_map["teacher"])[:2]
    
    async def _generate_practice_questions(self, concept: str, grade_level: str) -> List[str]:
        """Generate practice questions for concept reinforcement"""
        
        return [
            f"Can you give me an example of {concept} in everyday life?",
            f"What would happen if we changed this aspect of {concept}?",
            f"How does {concept} relate to what we learned before?"
        ]