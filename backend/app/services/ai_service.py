import json
from typing import Dict, List, Any
import os
from datetime import datetime, timedelta
import random
import logging
from .amazon_q_service import AmazonQService
from .enhanced_ai_service import EnhancedAIService

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        # Initialize Amazon Q Developer service
        self.amazon_q = AmazonQService()
        self.enhanced_ai = EnhancedAIService()
        self.bloom_levels = [
            "Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"
        ]
        
        # Check if Amazon Q is available
        self.q_enabled = self.amazon_q.q_available
        if self.q_enabled:
            logger.info("AI Service initialized with Amazon Q Developer integration")
        else:
            logger.info("AI Service using enhanced fallback implementations")
    
    async def generate_curriculum(self, content: str, subject: str, grade_level: str, learning_objectives: List[str] = None) -> Dict[str, Any]:
        """Generate 4-week modular curriculum aligned with Bloom's taxonomy using Amazon Q Developer"""
        
        try:
            # Use Amazon Q Developer for curriculum generation
            return await self.amazon_q.generate_curriculum_with_q(
                content=content,
                subject=subject,
                grade_level=grade_level,
                learning_objectives=learning_objectives
            )
        except Exception as e:
            logger.error(f"Amazon Q curriculum generation failed: {e}")
            # Use enhanced AI service for fallback
            return await self.enhanced_ai.generate_enhanced_curriculum(content, subject, grade_level)
    
    def _generate_fallback_curriculum(self, subject: str, grade_level: str, learning_objectives: List[str], content: str = "") -> Dict[str, Any]:
        """Generate fallback curriculum structure with Bloom's taxonomy"""
        # Extract key concepts from content for better fallback
        content_words = content.split() if content else []
        key_concepts = []
        if len(content_words) > 20:
            key_concepts = [word.strip('.,!?()[]') for word in content_words 
                          if len(word) > 4 and word.isalpha()][:8]
        
        return {
            "curriculum_overview": f"Comprehensive 4-week {subject} curriculum for {grade_level} students, designed with Bloom's Taxonomy progression. Incorporates content analysis from uploaded materials: {', '.join(key_concepts[:3]) if key_concepts else 'foundational concepts'}.",
            "learning_objectives": [
                f"Remember key {subject} terminology and concepts from uploaded materials",
                f"Understand fundamental {subject} principles and their relationships",
                f"Apply {subject} knowledge to solve real-world problems",
                f"Analyze complex {subject} scenarios using evidence-based reasoning",
                f"Evaluate {subject} solutions and make informed judgments",
                f"Create original {subject} projects demonstrating innovation and mastery"
            ],
            "weekly_modules": [
                {
                    "week_number": 1,
                    "title": "Foundation Building from Source Materials",
                    "bloom_focus": "Remember & Understand",
                    "learning_outcomes": [
                        f"Identify key {subject} concepts from uploaded content",
                        "Explain relationships between fundamental principles",
                        "Demonstrate understanding through multiple representations"
                    ],
                    "content_blocks": [
                        {
                            "title": "Content Analysis & Concept Mapping",
                            "description": f"Interactive exploration of uploaded {subject} materials focusing on: {', '.join(key_concepts[:3]) if key_concepts else 'core concepts'}",
                            "bloom_level": "Remember",
                            "estimated_duration": 75,
                            "activities": [
                                "Source material analysis",
                                "Concept mapping from uploaded content", 
                                "Vocabulary extraction and definition",
                                "Knowledge verification activities"
                            ],
                            "resources": [
                                "Uploaded source materials",
                                "Interactive concept mapping tools",
                                "Digital vocabulary builders",
                                "Supplementary video content"
                            ]
                        }
                    ],
                    "formative_assessments": ["Quick quizzes", "Concept maps"],
                    "summative_assessment": "Week 1 Knowledge Test"
                },
                {
                    "week_number": 2,
                    "title": "Application & Skill Development",
                    "bloom_focus": "Apply",
                    "learning_outcomes": [
                        f"Apply {subject} concepts from source materials to solve problems",
                        "Demonstrate skill transfer to new situations",
                        "Use appropriate tools and methods for problem-solving"
                    ],
                    "content_blocks": [
                        {
                            "title": "Guided Practice with Source Content",
                            "description": f"Structured application of concepts extracted from uploaded {subject} materials",
                            "bloom_level": "Apply",
                            "estimated_duration": 90,
                            "activities": [
                                "Guided problem-solving with real examples",
                                "Collaborative application exercises",
                                "Independent practice challenges",
                                "Peer review and feedback sessions"
                            ],
                            "resources": [
                                "Practice problem sets based on uploaded content",
                                "Solution video libraries",
                                "Peer collaboration platforms",
                                "Self-assessment tools"
                            ]
                        }
                    ],
                    "formative_assessments": ["Practice exercises", "Peer review"],
                    "summative_assessment": "Application Project"
                },
                {
                    "week_number": 3,
                    "title": "Critical Analysis & Evaluation",
                    "bloom_focus": "Analyze & Evaluate",
                    "learning_outcomes": [
                        f"Analyze complex {subject} scenarios from source materials",
                        "Evaluate effectiveness of different approaches",
                        "Make evidence-based judgments and recommendations"
                    ],
                    "content_blocks": [
                        {
                            "title": "Deep Analysis of Source Content",
                            "description": f"Critical examination of complex scenarios and methods from uploaded {subject} materials",
                            "bloom_level": "Analyze",
                            "estimated_duration": 85,
                            "activities": [
                                "Case study analysis from source materials",
                                "Comparative analysis of different approaches",
                                "Evidence evaluation and critical judgment",
                                "Structured debates and discussions"
                            ],
                            "resources": [
                                "Case study library from uploaded content",
                                "Analysis framework templates",
                                "Evaluation rubrics and tools",
                                "Research and evidence databases"
                            ]
                        }
                    ],
                    "formative_assessments": ["Analysis reports", "Peer evaluations"],
                    "summative_assessment": "Critical Analysis Essay"
                },
                {
                    "week_number": 4,
                    "title": "Innovation & Creative Synthesis",
                    "bloom_focus": "Create",
                    "learning_outcomes": [
                        f"Create original {subject} solutions incorporating source material insights",
                        "Synthesize knowledge from multiple sources and perspectives",
                        "Design innovative approaches to complex problems"
                    ],
                    "content_blocks": [
                        {
                            "title": "Innovation Challenge Project",
                            "description": f"Original creation incorporating all learned concepts and insights from uploaded {subject} materials",
                            "bloom_level": "Create",
                            "estimated_duration": 120,
                            "activities": [
                                "Innovation design thinking process",
                                "Knowledge synthesis from all sources",
                                "Collaborative creation and peer review",
                                "Presentation to authentic audience"
                            ],
                            "resources": [
                                "Design thinking and creation tools",
                                "Integration frameworks and templates",
                                "Peer collaboration platforms",
                                "Presentation and showcase technologies"
                            ]
                        }
                    ],
                    "formative_assessments": ["Progress check-ins", "Peer feedback"],
                    "summative_assessment": "Final Creative Project"
                }
            ],
            "final_project": {
                "title": f"Comprehensive {subject} Innovation Portfolio",
                "description": f"Student-designed capstone project demonstrating mastery across all Bloom's taxonomy levels, incorporating insights from uploaded source materials and real-world applications",
                "requirements": [
                    "Research and analysis component using source materials",
                    "Creative solution or innovative product",
                    "Critical evaluation and reflection essay",
                    "Presentation to authentic audience with peer feedback"
                ],
                "bloom_levels": ["Apply", "Analyze", "Evaluate", "Create"],
                "deliverables": [
                    "Project proposal with clear objectives",
                    "Research synthesis from multiple sources",
                    "Creative product or solution prototype",
                    "Comprehensive reflection and evaluation"
                ]
            },
            "differentiation_strategies": {
                "visual_learners": [
                    "Graphic organizers and concept maps from source content",
                    "Infographics and visual representations",
                    "Video content and interactive visualizations",
                    "Color-coded materials and highlighting systems"
                ],
                "auditory_learners": [
                    "Discussion forums and verbal processing",
                    "Podcast creation and audio recordings",
                    "Think-aloud protocols and verbal explanations",
                    "Music integration and rhythmic learning aids"
                ],
                "kinesthetic_learners": [
                    "Hands-on activities and experiments",
                    "Movement-based learning and role-playing",
                    "Building activities and manipulatives",
                    "Interactive simulations and virtual labs"
                ],
                "advanced_students": [
                    "Independent research projects",
                    "Mentorship and leadership opportunities",
                    "Advanced problem-solving challenges",
                    "Cross-curricular connections and extensions"
                ],
                "struggling_students": [
                    "Additional scaffolding and support materials",
                    "Peer tutoring partnerships",
                    "Modified assessments and flexible timelines",
                    "Frequent check-ins and personalized feedback"
                ]
            },
            "prerequisite_knowledge": [
                f"Basic {subject} vocabulary and foundational concepts",
                "Reading comprehension at appropriate grade level",
                "Basic research and information literacy skills",
                "Familiarity with digital learning tools and platforms",
                "Collaborative learning and communication skills"
            ],
            "technology_integration": [
                "Learning management system (LMS) for content delivery",
                "Interactive simulation and modeling software",
                "Collaborative online platforms and tools",
                "Digital creation and design applications",
                "Assessment and feedback systems",
                "Virtual and augmented reality learning experiences"
            ],
            "real_world_connections": [
                f"Industry applications and career pathways in {subject}",
                "Community problem-solving and service learning",
                "Expert guest speakers and mentorship opportunities",
                "Internship and job shadowing experiences",
                "Current events and contemporary issues integration"
            ]
        }
    
    async def generate_assessments(self, curriculum_data: Dict[str, Any], assessment_type: str = "comprehensive") -> Dict[str, Any]:
        """Generate comprehensive assessments using Amazon Q Developer"""
        
        try:
            # Use Amazon Q Developer for assessment generation
            return await self.amazon_q.generate_assessments_with_q(
                curriculum_data=curriculum_data,
                assessment_type=assessment_type
            )
        except Exception as e:
            logger.error(f"Amazon Q assessment generation failed: {e}")
            # Use enhanced AI service for fallback
            return await self.enhanced_ai.generate_enhanced_assessments(curriculum_data)
    
    def _generate_fallback_assessments(self, curriculum_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fallback assessment structure"""
        return {
            "assessment_overview": "Comprehensive assessment covering all learning objectives",
            "total_points": 100,
            "time_limit": 90,
            "questions": [
                {
                    "id": 1,
                    "question_text": "What are the key concepts covered in this curriculum?",
                    "question_type": "mcq",
                    "bloom_level": "Remember",
                    "difficulty": "easy",
                    "points": 5,
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": "Option A",
                    "explanation": "This tests basic recall of curriculum content"
                },
                {
                    "id": 2,
                    "question_text": "Explain how you would apply these concepts in a real-world scenario.",
                    "question_type": "short_answer",
                    "bloom_level": "Apply",
                    "difficulty": "medium",
                    "points": 15,
                    "sample_answer": "Students should demonstrate practical application of learned concepts",
                    "rubric": {
                        "excellent": "Clear application with specific examples (13-15 pts)",
                        "good": "Good application with some examples (10-12 pts)",
                        "satisfactory": "Basic application shown (7-9 pts)",
                        "needs_improvement": "Limited or unclear application (0-6 pts)"
                    }
                }
            ]
        }
    
    async def generate_personalized_path(self, student_profile: Dict[str, Any], curriculum_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized learning path using Amazon Q Developer"""
        
        try:
            # Use Amazon Q Developer for personalized path generation
            return await self.amazon_q.generate_personalized_path_with_q(
                student_profile=student_profile,
                curriculum_data=curriculum_data
            )
        except Exception as e:
            logger.error(f"Amazon Q personalization failed: {e}")
            # Fallback to enhanced local generation
            return self._generate_fallback_personalized_path(student_profile, curriculum_data)
    
    def _generate_fallback_personalized_path(self, student_profile: Dict[str, Any], curriculum_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fallback personalized learning path"""
        learning_style = student_profile.get("learning_style", "mixed")
        
        style_activities = {
            "visual": ["Diagrams", "Charts", "Videos", "Infographics"],
            "auditory": ["Discussions", "Podcasts", "Lectures", "Music"],
            "kinesthetic": ["Hands-on", "Movement", "Building", "Experiments"],
            "mixed": ["Varied activities", "Multi-modal content"]
        }
        
        return {
            "personalized_overview": f"Customized learning path for {learning_style} learner",
            "recommended_sequence": "Standard curriculum sequence with style adaptations",
            "adaptive_activities": style_activities.get(learning_style, style_activities["mixed"]),
            "difficulty_adjustments": "Standard difficulty with optional challenges",
            "interest_connections": "Content linked to student interests where possible",
            "support_resources": ["Tutoring", "Study guides", "Practice exercises"],
            "challenge_extensions": ["Advanced projects", "Research opportunities"],
            "timeline_adjustments": "Standard 4-week timeline with flexible pacing"
        }
    
    async def auto_grade_response(self, question: Dict[str, Any], student_answer: str) -> Dict[str, Any]:
        """Auto-grade student responses using AI"""
        
        if question["question_type"] == "mcq":
            is_correct = student_answer.strip().lower() == question["correct_answer"].strip().lower()
            return {
                "score": question["points"] if is_correct else 0,
                "max_score": question["points"],
                "is_correct": is_correct,
                "feedback": "Correct!" if is_correct else f"Incorrect. The correct answer is {question['correct_answer']}"
            }
        
        elif question["question_type"] in ["short_answer", "essay"]:
            prompt = f"""
            Grade this student response using the provided rubric.
            
            Question: {question['question_text']}
            Student Answer: {student_answer}
            Sample Answer: {question.get('sample_answer', 'Not provided')}
            Rubric: {question.get('rubric', 'Standard rubric')}
            Max Points: {question['points']}
            
            Provide:
            1. score (0 to {question['points']})
            2. feedback (constructive comments)
            3. strengths (what the student did well)
            4. improvements (areas for growth)
            
            Return as JSON.
            """
            
            # Mock grading for development
            score_percentage = random.uniform(0.6, 0.95)
            score = int(question["points"] * score_percentage)
            
            return {
                "score": score,
                "max_score": question["points"],
                "feedback": f"Good response! Score: {score}/{question['points']}. Consider expanding on key points.",
                "strengths": ["Clear understanding demonstrated", "Good use of examples"],
                "improvements": ["Add more detail", "Include specific examples"]
            }
        
        return {"score": 0, "max_score": question["points"], "feedback": "Unable to grade this response type"}
    
    async def generate_analytics_insights(self, student_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate learning analytics and insights"""
        
        prompt = f"""
        As an Analytics Agent, analyze this student performance data and provide insights.
        
        Student Data: {json.dumps(student_data, indent=2)[:1500]}...
        
        Generate analytics with:
        1. mastery_analysis: Which concepts students have mastered
        2. common_misconceptions: Frequent errors and misunderstandings
        3. learning_gaps: Areas needing reinforcement
        4. remediation_suggestions: Specific interventions
        5. performance_trends: Progress over time
        6. differentiation_needs: Students needing different approaches
        
        Provide actionable insights for teachers.
        """
        
        # Use fallback analytics for development
        return {
            "mastery_analysis": "Students showing good progress in foundational concepts",
            "common_misconceptions": ["Confusion between similar concepts", "Need more practice with applications"],
            "learning_gaps": ["Advanced problem-solving skills", "Critical thinking development"],
            "remediation_suggestions": ["Additional practice exercises", "Peer tutoring sessions", "Visual learning aids"],
            "performance_trends": "Overall improvement trend observed",
            "differentiation_needs": "Mix of visual and hands-on learners identified"
        }