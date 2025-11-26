import json
import boto3
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
from botocore.exceptions import ClientError, NoCredentialsError
import os
from .credential_manager import CredentialManager

logger = logging.getLogger(__name__)

class AmazonQService:
    """
    Amazon Q Developer Integration Service for EdweavePack
    
    Provides AI-powered curriculum generation, assessment creation,
    and personalized learning path generation using Amazon Bedrock
    and Q Developer capabilities.
    """
    
    def __init__(self):
        self.model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
        
        # Get credentials using credential manager
        creds = CredentialManager.get_aws_credentials()
        
        if creds and CredentialManager.test_credentials():
            try:
                self.bedrock_client = boto3.client('bedrock-runtime', **creds)
                self.q_available = True
                logger.info("Amazon Q Developer service initialized successfully")
            except Exception as e:
                logger.warning(f"Amazon Q initialization failed: {e}")
                self.q_available = False
                self.bedrock_client = None
        else:
            logger.warning("No valid AWS credentials found, using fallback mode")
            self.q_available = False
            self.bedrock_client = None
    
    async def invoke_q_developer(self, prompt: str, max_tokens: int = 4000) -> str:
        """Invoke Amazon Q Developer via Bedrock"""
        if not self.q_available:
            raise Exception("Amazon Q Developer not available")
        
        try:
            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "top_p": 0.9
            })
            
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=body,
                contentType='application/json'
            )
            
            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']
            
        except Exception as e:
            logger.error(f"Amazon Q invocation failed: {e}")
            raise
    
    async def generate_curriculum_with_q(self, content: str, subject: str, grade_level: str, learning_objectives: List[str] = None) -> Dict[str, Any]:
        """Generate comprehensive curriculum using Amazon Q Developer"""
        
        objectives_text = "\n".join(learning_objectives) if learning_objectives else "General learning objectives"
        
        prompt = f"""
        As Amazon Q Developer's AI Curriculum Architect, create a world-class 4-week modular curriculum for {subject} at {grade_level} level.
        
        SOURCE CONTENT ANALYSIS:
        {content[:3000]}...
        
        LEARNING OBJECTIVES:
        {objectives_text}
        
        CURRICULUM REQUIREMENTS:
        1. Align with Bloom's Taxonomy progression (Remember → Understand → Apply → Analyze → Evaluate → Create)
        2. Include differentiated instruction for multiple learning styles
        3. Integrate formative and summative assessments
        4. Provide scaffolded learning experiences
        5. Include real-world applications and project-based learning
        
        Generate a comprehensive JSON curriculum with this exact structure:
        {{
            "curriculum_overview": "Detailed description of the curriculum's pedagogical approach and goals",
            "learning_objectives": [
                "SMART objective 1 (Remember level)",
                "SMART objective 2 (Understand level)", 
                "SMART objective 3 (Apply level)",
                "SMART objective 4 (Analyze level)",
                "SMART objective 5 (Evaluate level)",
                "SMART objective 6 (Create level)"
            ],
            "prerequisite_knowledge": ["Required prior knowledge", "Essential skills"],
            "weekly_modules": [
                {{
                    "week_number": 1,
                    "title": "Foundation Building",
                    "bloom_focus": "Remember & Understand",
                    "learning_outcomes": ["Specific weekly outcomes"],
                    "content_blocks": [
                        {{
                            "title": "Content block title",
                            "description": "Detailed description",
                            "bloom_level": "Remember",
                            "estimated_duration": 60,
                            "activities": [
                                {{
                                    "type": "lecture",
                                    "title": "Activity title",
                                    "description": "Activity description",
                                    "duration": 20,
                                    "materials": ["Required materials"],
                                    "differentiation": {{
                                        "visual": "Visual learning adaptation",
                                        "auditory": "Auditory learning adaptation", 
                                        "kinesthetic": "Hands-on adaptation"
                                    }}
                                }}
                            ],
                            "resources": ["Textbook chapters", "Online resources", "Videos"],
                            "assessment_checkpoints": ["Quick formative checks"]
                        }}
                    ],
                    "formative_assessments": [
                        {{
                            "type": "quiz",
                            "title": "Knowledge check",
                            "bloom_level": "Remember",
                            "questions": 5
                        }}
                    ],
                    "summative_assessment": {{
                        "title": "Week 1 Assessment",
                        "type": "mixed",
                        "bloom_levels": ["Remember", "Understand"],
                        "points": 100
                    }}
                }}
            ],
            "final_project": {{
                "title": "Capstone project title",
                "description": "Comprehensive project description",
                "bloom_levels": ["Apply", "Analyze", "Evaluate", "Create"],
                "deliverables": ["Project components"],
                "rubric": {{
                    "criteria": ["Assessment criteria"],
                    "levels": ["Excellent", "Good", "Satisfactory", "Needs Improvement"]
                }}
            }},
            "differentiation_strategies": {{
                "visual_learners": ["Specific strategies for visual learners"],
                "auditory_learners": ["Specific strategies for auditory learners"],
                "kinesthetic_learners": ["Specific strategies for kinesthetic learners"],
                "advanced_students": ["Challenge activities"],
                "struggling_students": ["Support strategies"]
            }},
            "technology_integration": ["Educational technology tools and platforms"],
            "real_world_connections": ["Industry applications", "Career connections"]
        }}
        
        Ensure the curriculum is pedagogically sound, engaging, and aligned with modern educational best practices.
        """
        
        try:
            if self.q_available:
                response = await self.invoke_q_developer(prompt)
                # Extract JSON from response
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                if json_start != -1 and json_end != -1:
                    curriculum_json = response[json_start:json_end]
                    return json.loads(curriculum_json)
                else:
                    raise ValueError("No valid JSON found in Q Developer response")
            else:
                # Enhanced fallback with better structure
                return self._generate_enhanced_fallback_curriculum(subject, grade_level, learning_objectives, content)
                
        except Exception as e:
            logger.error(f"Q Developer curriculum generation failed: {e}")
            return self._generate_enhanced_fallback_curriculum(subject, grade_level, learning_objectives, content)
    
    async def generate_assessments_with_q(self, curriculum_data: Dict[str, Any], assessment_type: str = "comprehensive") -> Dict[str, Any]:
        """Generate comprehensive assessments using Amazon Q Developer"""
        
        prompt = f"""
        As Amazon Q Developer's Assessment Generator, create a comprehensive assessment suite for this curriculum:
        
        CURRICULUM CONTEXT:
        {json.dumps(curriculum_data, indent=2)[:2000]}...
        
        ASSESSMENT REQUIREMENTS:
        - Assessment Type: {assessment_type}
        - Include all Bloom's taxonomy levels
        - Provide detailed rubrics for subjective questions
        - Include adaptive difficulty progression
        - Support multiple question formats
        
        Generate a JSON assessment with this structure:
        {{
            "assessment_overview": {{
                "title": "Assessment title",
                "description": "Comprehensive assessment description",
                "total_points": 100,
                "time_limit_minutes": 90,
                "bloom_distribution": {{
                    "remember": 20,
                    "understand": 20,
                    "apply": 25,
                    "analyze": 15,
                    "evaluate": 10,
                    "create": 10
                }}
            }},
            "question_bank": [
                {{
                    "id": 1,
                    "question_text": "Question text here",
                    "question_type": "multiple_choice",
                    "bloom_level": "remember",
                    "difficulty": "easy",
                    "points": 5,
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": "Option A",
                    "explanation": "Detailed explanation of why this is correct",
                    "learning_objective": "Related learning objective",
                    "tags": ["topic1", "concept2"]
                }},
                {{
                    "id": 2,
                    "question_text": "Analyze the following scenario...",
                    "question_type": "short_answer",
                    "bloom_level": "analyze",
                    "difficulty": "medium",
                    "points": 15,
                    "sample_answer": "Expected response elements",
                    "rubric": {{
                        "excellent": {{
                            "description": "Demonstrates comprehensive analysis",
                            "points": "13-15"
                        }},
                        "good": {{
                            "description": "Shows good analytical thinking",
                            "points": "10-12"
                        }},
                        "satisfactory": {{
                            "description": "Basic analysis present",
                            "points": "7-9"
                        }},
                        "needs_improvement": {{
                            "description": "Limited or unclear analysis",
                            "points": "0-6"
                        }}
                    }},
                    "keywords": ["key concept 1", "key concept 2"]
                }},
                {{
                    "id": 3,
                    "question_text": "Create a solution for...",
                    "question_type": "project",
                    "bloom_level": "create",
                    "difficulty": "hard",
                    "points": 25,
                    "requirements": ["Requirement 1", "Requirement 2"],
                    "deliverables": ["Deliverable 1", "Deliverable 2"],
                    "rubric": {{
                        "creativity": {{
                            "weight": 30,
                            "levels": ["Highly creative", "Creative", "Somewhat creative", "Not creative"]
                        }},
                        "technical_accuracy": {{
                            "weight": 40,
                            "levels": ["Highly accurate", "Accurate", "Mostly accurate", "Inaccurate"]
                        }},
                        "presentation": {{
                            "weight": 30,
                            "levels": ["Excellent", "Good", "Satisfactory", "Poor"]
                        }}
                    }}
                }}
            ],
            "adaptive_pathways": {{
                "high_performers": ["Challenge question IDs"],
                "average_performers": ["Standard question IDs"],
                "struggling_learners": ["Support question IDs with hints"]
            }},
            "feedback_templates": {{
                "correct": "Excellent work! You demonstrated...",
                "partially_correct": "Good effort! Consider...",
                "incorrect": "Let's review this concept..."
            }}
        }}
        """
        
        try:
            if self.q_available:
                response = await self.invoke_q_developer(prompt)
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                if json_start != -1 and json_end != -1:
                    assessment_json = response[json_start:json_end]
                    return json.loads(assessment_json)
                else:
                    raise ValueError("No valid JSON found in Q Developer response")
            else:
                return self._generate_enhanced_fallback_assessments(curriculum_data)
                
        except Exception as e:
            logger.error(f"Q Developer assessment generation failed: {e}")
            return self._generate_enhanced_fallback_assessments(curriculum_data)
    
    async def generate_personalized_path_with_q(self, student_profile: Dict[str, Any], curriculum_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized learning path using Amazon Q Developer"""
        
        prompt = f"""
        As Amazon Q Developer's Personalized Learning Agent, create an adaptive learning path for this student:
        
        STUDENT PROFILE:
        {json.dumps(student_profile, indent=2)}
        
        CURRICULUM CONTEXT:
        {json.dumps(curriculum_data, indent=2)[:1500]}...
        
        Generate a personalized learning path JSON:
        {{
            "personalization_overview": {{
                "student_id": "{student_profile.get('id', 'unknown')}",
                "learning_style": "{student_profile.get('learning_style', 'mixed')}",
                "current_level": "assessed_level",
                "target_level": "desired_level",
                "estimated_completion": "time_estimate"
            }},
            "adaptive_sequence": [
                {{
                    "module_id": 1,
                    "title": "Personalized module title",
                    "difficulty_adjustment": "standard|easier|harder",
                    "learning_style_adaptations": {{
                        "primary_modality": "visual|auditory|kinesthetic",
                        "activities": ["Adapted activities"],
                        "resources": ["Personalized resources"]
                    }},
                    "pacing": {{
                        "recommended_hours": 8,
                        "flexibility": "high|medium|low",
                        "checkpoints": ["Progress markers"]
                    }}
                }}
            ],
            "support_strategies": {{
                "strengths": ["Identified student strengths"],
                "growth_areas": ["Areas needing development"],
                "interventions": ["Specific support strategies"],
                "enrichment": ["Advanced opportunities"]
            }},
            "progress_monitoring": {{
                "milestones": ["Key progress indicators"],
                "assessment_frequency": "weekly|bi-weekly|monthly",
                "feedback_mechanisms": ["How progress is communicated"]
            }}
        }}
        """
        
        try:
            if self.q_available:
                response = await self.invoke_q_developer(prompt)
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                if json_start != -1 and json_end != -1:
                    path_json = response[json_start:json_end]
                    return json.loads(path_json)
                else:
                    raise ValueError("No valid JSON found in Q Developer response")
            else:
                return self._generate_enhanced_fallback_personalized_path(student_profile, curriculum_data)
                
        except Exception as e:
            logger.error(f"Q Developer personalization failed: {e}")
            return self._generate_enhanced_fallback_personalized_path(student_profile, curriculum_data)
    
    def _generate_enhanced_fallback_curriculum(self, subject: str, grade_level: str, learning_objectives: List[str], content: str) -> Dict[str, Any]:
        """Enhanced fallback curriculum with better pedagogical structure"""
        
        # Extract key concepts from content
        content_words = content.split() if content else []
        key_concepts = []
        if len(content_words) > 20:
            # Simple keyword extraction - take meaningful words
            key_concepts = [word.strip('.,!?()[]') for word in content_words 
                          if len(word) > 4 and word.isalpha()][:10]
        
        return {
            "curriculum_overview": f"Comprehensive 4-week {subject} curriculum for {grade_level} students, designed with Bloom's Taxonomy progression and evidence-based pedagogical practices. Incorporates content analysis from uploaded materials to ensure relevance and alignment.",
            "learning_objectives": [
                f"Remember and recall key {subject} terminology and foundational concepts",
                f"Understand fundamental principles and relationships in {subject}",
                f"Apply {subject} knowledge to solve real-world problems and scenarios",
                f"Analyze complex {subject} situations and break them into components",
                f"Evaluate {subject} solutions and make informed judgments",
                f"Create original {subject} projects demonstrating mastery and innovation"
            ],
            "prerequisite_knowledge": [
                f"Basic {subject} vocabulary and concepts",
                "Reading comprehension at grade level",
                "Basic research and study skills",
                "Familiarity with digital learning tools"
            ],
            "weekly_modules": [
                {
                    "week_number": 1,
                    "title": "Foundation Building & Knowledge Acquisition",
                    "bloom_focus": "Remember & Understand",
                    "learning_outcomes": [
                        f"Identify and define key {subject} concepts from source materials",
                        "Explain relationships between fundamental principles",
                        "Demonstrate understanding through multiple representations"
                    ],
                    "content_blocks": [
                        {
                            "title": "Content Analysis & Concept Mapping",
                            "description": f"Interactive exploration of uploaded {subject} materials with concept identification",
                            "bloom_level": "Remember",
                            "estimated_duration": 75,
                            "activities": [
                                {
                                    "type": "content_analysis",
                                    "title": "Source Material Exploration",
                                    "description": f"Guided analysis of uploaded content focusing on: {', '.join(key_concepts[:5]) if key_concepts else 'core concepts'}",
                                    "duration": 30,
                                    "materials": ["Uploaded content", "Concept mapping tools"],
                                    "differentiation": {
                                        "visual": "Mind maps and infographics",
                                        "auditory": "Discussion and verbal explanation",
                                        "kinesthetic": "Interactive sorting activities"
                                    }
                                },
                                {
                                    "type": "vocabulary_building",
                                    "title": "Key Terms & Definitions",
                                    "description": "Building foundational vocabulary from source materials",
                                    "duration": 25,
                                    "materials": ["Digital flashcards", "Glossary creation tools"],
                                    "differentiation": {
                                        "visual": "Visual vocabulary cards with images",
                                        "auditory": "Pronunciation guides and audio definitions",
                                        "kinesthetic": "Physical card sorting and matching"
                                    }
                                },
                                {
                                    "type": "knowledge_check",
                                    "title": "Understanding Verification",
                                    "description": "Quick assessment of concept comprehension",
                                    "duration": 20,
                                    "materials": ["Online quiz platform", "Peer discussion"],
                                    "differentiation": {
                                        "visual": "Image-based questions",
                                        "auditory": "Verbal explanations",
                                        "kinesthetic": "Interactive demonstrations"
                                    }
                                }
                            ],
                            "resources": [
                                "Uploaded source materials",
                                "Supplementary readings",
                                "Educational videos",
                                "Interactive simulations"
                            ],
                            "assessment_checkpoints": [
                                "Concept map completion",
                                "Vocabulary quiz (80% accuracy)",
                                "Peer explanation activity"
                            ]
                        }
                    ],
                    "formative_assessments": [
                        {
                            "type": "concept_check",
                            "title": "Foundation Knowledge Quiz",
                            "bloom_level": "Remember",
                            "questions": 10
                        },
                        {
                            "type": "discussion",
                            "title": "Concept Explanation Forum",
                            "bloom_level": "Understand",
                            "questions": 3
                        }
                    ],
                    "summative_assessment": {
                        "title": "Week 1: Foundation Mastery Assessment",
                        "type": "mixed",
                        "bloom_levels": ["Remember", "Understand"],
                        "points": 100
                    }
                },
                {
                    "week_number": 2,
                    "title": "Application & Skill Development",
                    "bloom_focus": "Apply",
                    "learning_outcomes": [
                        f"Apply {subject} concepts to solve structured problems",
                        "Demonstrate skill transfer to new situations",
                        "Use appropriate tools and methods for problem-solving"
                    ],
                    "content_blocks": [
                        {
                            "title": "Guided Practice & Application",
                            "description": "Structured application of concepts from uploaded materials",
                            "bloom_level": "Apply",
                            "estimated_duration": 90,
                            "activities": [
                                {
                                    "type": "guided_practice",
                                    "title": "Step-by-Step Problem Solving",
                                    "description": "Scaffolded practice with real examples from source content",
                                    "duration": 40,
                                    "materials": ["Practice problem sets", "Solution templates"],
                                    "differentiation": {
                                        "visual": "Flowcharts and visual guides",
                                        "auditory": "Think-aloud protocols",
                                        "kinesthetic": "Hands-on manipulation"
                                    }
                                },
                                {
                                    "type": "collaborative_work",
                                    "title": "Peer Problem-Solving",
                                    "description": "Team-based application activities",
                                    "duration": 30,
                                    "materials": ["Group worksheets", "Digital collaboration tools"],
                                    "differentiation": {
                                        "visual": "Shared visual workspaces",
                                        "auditory": "Verbal collaboration protocols",
                                        "kinesthetic": "Physical group activities"
                                    }
                                },
                                {
                                    "type": "independent_practice",
                                    "title": "Solo Application Challenge",
                                    "description": "Individual application of learned concepts",
                                    "duration": 20,
                                    "materials": ["Individual practice sets", "Self-check tools"],
                                    "differentiation": {
                                        "visual": "Visual problem formats",
                                        "auditory": "Audio instructions",
                                        "kinesthetic": "Interactive problem interfaces"
                                    }
                                }
                            ],
                            "resources": [
                                "Practice problem databases",
                                "Solution video libraries",
                                "Peer collaboration platforms",
                                "Self-assessment tools"
                            ],
                            "assessment_checkpoints": [
                                "Guided practice completion (85% accuracy)",
                                "Peer collaboration evaluation",
                                "Independent practice success rate"
                            ]
                        }
                    ],
                    "formative_assessments": [
                        {
                            "type": "practice_set",
                            "title": "Application Skills Check",
                            "bloom_level": "Apply",
                            "questions": 8
                        }
                    ],
                    "summative_assessment": {
                        "title": "Week 2: Application Mastery Project",
                        "type": "project",
                        "bloom_levels": ["Apply"],
                        "points": 100
                    }
                },
                {
                    "week_number": 3,
                    "title": "Analysis & Critical Thinking",
                    "bloom_focus": "Analyze & Evaluate",
                    "learning_outcomes": [
                        f"Analyze complex {subject} scenarios and identify patterns",
                        "Evaluate the effectiveness of different approaches",
                        "Make evidence-based judgments and recommendations"
                    ],
                    "content_blocks": [
                        {
                            "title": "Critical Analysis Workshop",
                            "description": "Deep analysis of complex scenarios from source materials",
                            "bloom_level": "Analyze",
                            "estimated_duration": 85,
                            "activities": [
                                {
                                    "type": "case_study",
                                    "title": "Complex Scenario Analysis",
                                    "description": "Multi-faceted analysis of real-world applications",
                                    "duration": 35,
                                    "materials": ["Case study materials", "Analysis frameworks"],
                                    "differentiation": {
                                        "visual": "Graphic organizers and charts",
                                        "auditory": "Discussion and debate",
                                        "kinesthetic": "Role-playing scenarios"
                                    }
                                },
                                {
                                    "type": "comparative_analysis",
                                    "title": "Solution Evaluation",
                                    "description": "Comparing and contrasting different approaches",
                                    "duration": 30,
                                    "materials": ["Comparison matrices", "Evaluation rubrics"],
                                    "differentiation": {
                                        "visual": "Comparison charts and tables",
                                        "auditory": "Verbal argumentation",
                                        "kinesthetic": "Physical sorting and ranking"
                                    }
                                },
                                {
                                    "type": "evidence_evaluation",
                                    "title": "Critical Judgment Exercise",
                                    "description": "Evaluating evidence quality and making judgments",
                                    "duration": 20,
                                    "materials": ["Evidence evaluation tools", "Decision matrices"],
                                    "differentiation": {
                                        "visual": "Evidence mapping",
                                        "auditory": "Oral presentations",
                                        "kinesthetic": "Evidence sorting activities"
                                    }
                                }
                            ],
                            "resources": [
                                "Case study library",
                                "Analysis tool templates",
                                "Evaluation frameworks",
                                "Research databases"
                            ],
                            "assessment_checkpoints": [
                                "Case study analysis quality",
                                "Comparative analysis depth",
                                "Evidence evaluation accuracy"
                            ]
                        }
                    ],
                    "formative_assessments": [
                        {
                            "type": "analysis_report",
                            "title": "Critical Analysis Assignment",
                            "bloom_level": "Analyze",
                            "questions": 5
                        },
                        {
                            "type": "evaluation_essay",
                            "title": "Solution Evaluation Paper",
                            "bloom_level": "Evaluate",
                            "questions": 3
                        }
                    ],
                    "summative_assessment": {
                        "title": "Week 3: Critical Thinking Portfolio",
                        "type": "portfolio",
                        "bloom_levels": ["Analyze", "Evaluate"],
                        "points": 100
                    }
                },
                {
                    "week_number": 4,
                    "title": "Synthesis & Innovation",
                    "bloom_focus": "Create",
                    "learning_outcomes": [
                        f"Create original {subject} solutions and products",
                        "Synthesize knowledge from multiple sources",
                        "Design innovative approaches to complex problems"
                    ],
                    "content_blocks": [
                        {
                            "title": "Creative Project Development",
                            "description": "Original creation incorporating all learned concepts",
                            "bloom_level": "Create",
                            "estimated_duration": 120,
                            "activities": [
                                {
                                    "type": "project_design",
                                    "title": "Innovation Challenge",
                                    "description": "Design and create original solutions",
                                    "duration": 50,
                                    "materials": ["Design thinking tools", "Creation platforms"],
                                    "differentiation": {
                                        "visual": "Visual design and prototyping",
                                        "auditory": "Presentation and storytelling",
                                        "kinesthetic": "Building and construction"
                                    }
                                },
                                {
                                    "type": "synthesis_project",
                                    "title": "Knowledge Integration",
                                    "description": "Combining concepts from all previous weeks",
                                    "duration": 40,
                                    "materials": ["Integration frameworks", "Synthesis tools"],
                                    "differentiation": {
                                        "visual": "Concept integration maps",
                                        "auditory": "Verbal synthesis presentations",
                                        "kinesthetic": "Interactive demonstrations"
                                    }
                                },
                                {
                                    "type": "peer_review",
                                    "title": "Collaborative Refinement",
                                    "description": "Peer feedback and project improvement",
                                    "duration": 30,
                                    "materials": ["Peer review protocols", "Feedback tools"],
                                    "differentiation": {
                                        "visual": "Visual feedback systems",
                                        "auditory": "Verbal feedback sessions",
                                        "kinesthetic": "Interactive review activities"
                                    }
                                }
                            ],
                            "resources": [
                                "Creation and design tools",
                                "Project templates",
                                "Peer collaboration platforms",
                                "Presentation technologies"
                            ],
                            "assessment_checkpoints": [
                                "Project proposal approval",
                                "Mid-development review",
                                "Peer feedback integration"
                            ]
                        }
                    ],
                    "formative_assessments": [
                        {
                            "type": "project_milestone",
                            "title": "Creation Progress Check",
                            "bloom_level": "Create",
                            "questions": 4
                        }
                    ],
                    "summative_assessment": {
                        "title": "Week 4: Innovation Showcase",
                        "type": "presentation",
                        "bloom_levels": ["Create"],
                        "points": 100
                    }
                }
            ],
            "final_project": {
                "title": f"Comprehensive {subject} Innovation Portfolio",
                "description": "Student-designed capstone project demonstrating mastery across all Bloom's taxonomy levels, incorporating insights from uploaded source materials",
                "bloom_levels": ["Apply", "Analyze", "Evaluate", "Create"],
                "deliverables": [
                    "Research and analysis component",
                    "Creative solution or product",
                    "Reflection and evaluation essay",
                    "Presentation to authentic audience"
                ],
                "rubric": {
                    "criteria": [
                        "Content mastery and accuracy",
                        "Critical thinking and analysis",
                        "Creativity and innovation",
                        "Communication and presentation",
                        "Reflection and metacognition"
                    ],
                    "levels": ["Exemplary (90-100%)", "Proficient (80-89%)", "Developing (70-79%)", "Beginning (60-69%)"]
                }
            },
            "differentiation_strategies": {
                "visual_learners": [
                    "Graphic organizers and concept maps",
                    "Infographics and visual representations",
                    "Video content and animations",
                    "Color-coded materials and highlighting"
                ],
                "auditory_learners": [
                    "Discussion forums and verbal processing",
                    "Podcasts and audio recordings",
                    "Think-aloud protocols",
                    "Music and rhythmic learning aids"
                ],
                "kinesthetic_learners": [
                    "Hands-on activities and experiments",
                    "Movement-based learning",
                    "Manipulatives and building activities",
                    "Role-playing and simulations"
                ],
                "advanced_students": [
                    "Independent research projects",
                    "Mentorship opportunities",
                    "Advanced problem-solving challenges",
                    "Leadership roles in group work"
                ],
                "struggling_students": [
                    "Additional scaffolding and support",
                    "Peer tutoring partnerships",
                    "Modified assessments and timelines",
                    "Frequent check-ins and feedback"
                ]
            },
            "technology_integration": [
                "Learning management system (LMS)",
                "Interactive simulation software",
                "Collaborative online platforms",
                "Digital creation and design tools",
                "Assessment and feedback systems",
                "Virtual and augmented reality applications"
            ],
            "real_world_connections": [
                f"Industry applications of {subject} concepts",
                "Career pathway exploration",
                "Community problem-solving projects",
                "Expert guest speakers and mentors",
                "Internship and job shadowing opportunities"
            ]
        }
    
    def _generate_enhanced_fallback_assessments(self, curriculum_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced fallback assessment generation"""
        return {
            "assessment_overview": {
                "title": "Comprehensive Curriculum Assessment",
                "description": "Multi-modal assessment covering all learning objectives and Bloom's taxonomy levels",
                "total_points": 100,
                "time_limit_minutes": 90,
                "bloom_distribution": {
                    "remember": 15,
                    "understand": 20,
                    "apply": 25,
                    "analyze": 20,
                    "evaluate": 10,
                    "create": 10
                }
            },
            "question_bank": [
                {
                    "id": 1,
                    "question_text": "Define the key concepts covered in this curriculum and explain their significance.",
                    "question_type": "multiple_choice",
                    "bloom_level": "remember",
                    "difficulty": "easy",
                    "points": 5,
                    "options": [
                        "Concepts are isolated facts with no connections",
                        "Key concepts form the foundation for understanding and application",
                        "Concepts are only important for testing purposes",
                        "Key concepts change frequently and have no lasting value"
                    ],
                    "correct_answer": "Key concepts form the foundation for understanding and application",
                    "explanation": "Key concepts serve as building blocks for deeper learning and practical application",
                    "learning_objective": "Remember and identify fundamental concepts",
                    "tags": ["foundational_knowledge", "concept_identification"]
                },
                {
                    "id": 2,
                    "question_text": "Explain how the concepts learned in this curriculum connect to real-world applications. Provide specific examples.",
                    "question_type": "short_answer",
                    "bloom_level": "understand",
                    "difficulty": "medium",
                    "points": 15,
                    "sample_answer": "Students should demonstrate understanding by connecting theoretical concepts to practical applications with specific, relevant examples",
                    "rubric": {
                        "excellent": {
                            "description": "Clear connections made with multiple specific examples and detailed explanations",
                            "points": "13-15"
                        },
                        "good": {
                            "description": "Good connections with some specific examples and adequate explanations",
                            "points": "10-12"
                        },
                        "satisfactory": {
                            "description": "Basic connections shown with limited examples",
                            "points": "7-9"
                        },
                        "needs_improvement": {
                            "description": "Unclear or missing connections and examples",
                            "points": "0-6"
                        }
                    },
                    "keywords": ["real-world application", "practical examples", "concept connection"]
                },
                {
                    "id": 3,
                    "question_text": "Apply the problem-solving framework learned in this curriculum to solve the following scenario: [Specific scenario based on curriculum content]",
                    "question_type": "problem_solving",
                    "bloom_level": "apply",
                    "difficulty": "medium",
                    "points": 20,
                    "scenario": "A complex, realistic problem requiring application of learned concepts",
                    "rubric": {
                        "problem_identification": {
                            "weight": 25,
                            "levels": ["Clearly identified", "Mostly identified", "Partially identified", "Not identified"]
                        },
                        "solution_process": {
                            "weight": 50,
                            "levels": ["Systematic and thorough", "Generally systematic", "Somewhat organized", "Disorganized"]
                        },
                        "final_solution": {
                            "weight": 25,
                            "levels": ["Correct and complete", "Mostly correct", "Partially correct", "Incorrect"]
                        }
                    }
                },
                {
                    "id": 4,
                    "question_text": "Analyze the strengths and weaknesses of different approaches to [curriculum-specific topic]. Compare at least three different methods.",
                    "question_type": "analytical_essay",
                    "bloom_level": "analyze",
                    "difficulty": "hard",
                    "points": 25,
                    "requirements": [
                        "Identify at least three different approaches",
                        "Analyze strengths and weaknesses of each",
                        "Use evidence to support analysis",
                        "Draw meaningful comparisons"
                    ],
                    "rubric": {
                        "depth_of_analysis": {
                            "weight": 40,
                            "levels": ["Thorough and insightful", "Good depth", "Adequate analysis", "Superficial"]
                        },
                        "use_of_evidence": {
                            "weight": 30,
                            "levels": ["Strong evidence", "Good evidence", "Some evidence", "Little evidence"]
                        },
                        "comparison_quality": {
                            "weight": 30,
                            "levels": ["Excellent comparisons", "Good comparisons", "Basic comparisons", "Poor comparisons"]
                        }
                    }
                },
                {
                    "id": 5,
                    "question_text": "Evaluate the effectiveness of the learning strategies used in this curriculum. Which were most beneficial for your learning and why?",
                    "question_type": "reflective_essay",
                    "bloom_level": "evaluate",
                    "difficulty": "medium",
                    "points": 15,
                    "requirements": [
                        "Identify specific learning strategies",
                        "Evaluate their effectiveness",
                        "Provide personal reflection",
                        "Justify opinions with reasoning"
                    ],
                    "rubric": {
                        "strategy_identification": {
                            "weight": 25,
                            "levels": ["Comprehensive", "Good", "Adequate", "Limited"]
                        },
                        "evaluation_quality": {
                            "weight": 50,
                            "levels": ["Thoughtful evaluation", "Good evaluation", "Basic evaluation", "Poor evaluation"]
                        },
                        "personal_reflection": {
                            "weight": 25,
                            "levels": ["Deep reflection", "Good reflection", "Some reflection", "Little reflection"]
                        }
                    }
                },
                {
                    "id": 6,
                    "question_text": "Create an innovative solution or product that demonstrates your mastery of the curriculum concepts. Include a detailed plan and rationale.",
                    "question_type": "creative_project",
                    "bloom_level": "create",
                    "difficulty": "hard",
                    "points": 20,
                    "deliverables": [
                        "Project proposal with clear objectives",
                        "Detailed implementation plan",
                        "Final product or prototype",
                        "Reflection on the creation process"
                    ],
                    "rubric": {
                        "creativity_innovation": {
                            "weight": 30,
                            "levels": ["Highly innovative", "Creative", "Somewhat creative", "Not creative"]
                        },
                        "concept_integration": {
                            "weight": 40,
                            "levels": ["Excellent integration", "Good integration", "Some integration", "Poor integration"]
                        },
                        "execution_quality": {
                            "weight": 30,
                            "levels": ["Excellent execution", "Good execution", "Adequate execution", "Poor execution"]
                        }
                    }
                }
            ],
            "adaptive_pathways": {
                "high_performers": [3, 4, 6],
                "average_performers": [1, 2, 3, 5],
                "struggling_learners": [1, 2, "with additional scaffolding and hints"]
            },
            "feedback_templates": {
                "correct": "Excellent work! You demonstrated strong understanding of {concept}. Consider exploring {extension_topic} to deepen your knowledge further.",
                "partially_correct": "Good effort! You showed understanding of {correct_aspects}. To improve, focus on {improvement_areas} and review {specific_resources}.",
                "incorrect": "Let's revisit this concept together. The key idea to remember is {key_concept}. Try reviewing {specific_materials} and then attempt {practice_activity}."
            }
        }
    
    def _generate_enhanced_fallback_personalized_path(self, student_profile: Dict[str, Any], curriculum_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced fallback personalized learning path"""
        learning_style = student_profile.get("learning_style", "mixed")
        prior_performance = student_profile.get("prior_performance", {})
        
        return {
            "personalization_overview": {
                "student_id": student_profile.get('id', 'student_001'),
                "learning_style": learning_style,
                "current_level": "Assessed based on prior performance and diagnostic",
                "target_level": "Mastery of all curriculum objectives",
                "estimated_completion": "4-6 weeks depending on pacing preferences"
            },
            "adaptive_sequence": [
                {
                    "module_id": 1,
                    "title": "Personalized Foundation Building",
                    "difficulty_adjustment": "standard",
                    "learning_style_adaptations": {
                        "primary_modality": learning_style,
                        "activities": self._get_style_specific_activities(learning_style),
                        "resources": self._get_style_specific_resources(learning_style)
                    },
                    "pacing": {
                        "recommended_hours": 8,
                        "flexibility": "high",
                        "checkpoints": ["Concept mastery check", "Application readiness", "Confidence assessment"]
                    }
                }
            ],
            "support_strategies": {
                "strengths": ["Identified through diagnostic assessment", "Learning style preferences", "Prior knowledge areas"],
                "growth_areas": ["Concepts needing reinforcement", "Skills requiring development", "Confidence building areas"],
                "interventions": ["Targeted practice sessions", "Peer tutoring opportunities", "Additional scaffolding"],
                "enrichment": ["Advanced challenges", "Independent research", "Leadership opportunities"]
            },
            "progress_monitoring": {
                "milestones": ["Weekly mastery checkpoints", "Module completion assessments", "Skill demonstration tasks"],
                "assessment_frequency": "weekly",
                "feedback_mechanisms": ["Immediate digital feedback", "Weekly progress reports", "Personalized recommendations"]
            }
        }
    
    def _get_style_specific_activities(self, learning_style: str) -> List[str]:
        """Get activities tailored to learning style"""
        activities = {
            "visual": ["Mind mapping", "Infographic creation", "Video analysis", "Diagram interpretation"],
            "auditory": ["Discussion forums", "Podcast creation", "Verbal explanations", "Music integration"],
            "kinesthetic": ["Hands-on experiments", "Role-playing", "Building activities", "Movement-based learning"],
            "mixed": ["Varied multi-modal activities", "Choice-based learning", "Flexible formats"]
        }
        return activities.get(learning_style, activities["mixed"])
    
    def _get_style_specific_resources(self, learning_style: str) -> List[str]:
        """Get resources tailored to learning style"""
        resources = {
            "visual": ["Interactive visualizations", "Graphic organizers", "Video libraries", "Image databases"],
            "auditory": ["Audio recordings", "Discussion platforms", "Verbal instruction tools", "Music resources"],
            "kinesthetic": ["Simulation software", "Virtual labs", "Interactive manipulatives", "Building tools"],
            "mixed": ["Multi-format resource library", "Adaptive content delivery", "Choice menus"]
        }
        return resources.get(learning_style, resources["mixed"])