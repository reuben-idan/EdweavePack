import json
import yaml
from typing import Dict, List, Any, Tuple
from app.services.ai_service import AIService

class AutoGraderAgent:
    def __init__(self):
        self.ai_service = AIService()
        with open('agents/kiro_config.yaml', 'r') as f:
            self.config = yaml.safe_load(f)
    
    async def grade_submission(self, submission: Dict[str, Any], assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Grade student submission using AI with detailed feedback"""
        
        prompt = f"""
        Grade this student submission against the assessment rubric.
        
        Assessment: {json.dumps(assessment, indent=2)}
        Submission: {json.dumps(submission, indent=2)}
        
        For each question, provide:
        - Score (0-max points)
        - Detailed feedback
        - Areas for improvement
        - Strengths identified
        
        Output JSON:
        {{
            "submission_id": "{submission.get('id')}",
            "student_id": "{submission.get('student_id')}",
            "assessment_id": "{assessment.get('id')}",
            "total_score": 85,
            "max_score": 100,
            "percentage": 85.0,
            "grade": "B",
            "graded_at": "timestamp",
            "question_scores": [
                {{
                    "question_id": 1,
                    "score": 8,
                    "max_score": 10,
                    "feedback": "detailed_feedback_for_student",
                    "rubric_level": "good",
                    "strengths": ["strength1", "strength2"],
                    "improvements": ["improvement1", "improvement2"]
                }}
            ],
            "overall_feedback": "comprehensive_feedback_summary",
            "next_steps": ["recommended_action1", "recommended_action2"],
            "time_spent": "minutes_to_complete"
        }}
        """
        
        response = await self.ai_service.generate_content(prompt)
        return json.loads(response)
    
    async def grade_coding_submission(self, code: str, test_cases: List[Dict], rubric: Dict) -> Dict[str, Any]:
        """Grade coding submissions with test execution and code quality analysis"""
        
        prompt = f"""
        Grade this coding submission with comprehensive analysis.
        
        Code: {code}
        Test Cases: {json.dumps(test_cases, indent=2)}
        Rubric: {json.dumps(rubric, indent=2)}
        
        Evaluate:
        - Correctness (passes test cases)
        - Code quality (readability, structure)
        - Efficiency (time/space complexity)
        - Best practices (naming, comments)
        - Error handling
        
        Output JSON:
        {{
            "correctness": {{
                "score": 80,
                "max_score": 100,
                "tests_passed": 8,
                "total_tests": 10,
                "failed_tests": [
                    {{
                        "test_name": "edge_case_1",
                        "expected": "expected_output",
                        "actual": "actual_output",
                        "error": "error_message"
                    }}
                ]
            }},
            "code_quality": {{
                "score": 75,
                "max_score": 100,
                "readability": 80,
                "structure": 70,
                "naming": 85,
                "comments": 60,
                "feedback": "specific_quality_feedback"
            }},
            "efficiency": {{
                "score": 90,
                "time_complexity": "O(n)",
                "space_complexity": "O(1)",
                "optimization_suggestions": ["suggestion1"]
            }},
            "overall_score": 82,
            "grade": "B+",
            "detailed_feedback": "comprehensive_code_review",
            "suggestions": ["improvement1", "improvement2"]
        }}
        """
        
        response = await self.ai_service.generate_content(prompt)
        return json.loads(response)
    
    async def generate_feedback(self, score: float, rubric: Dict[str, Any], student_answer: str) -> str:
        """Generate personalized feedback based on score and rubric"""
        
        prompt = f"""
        Generate constructive, personalized feedback for this student response.
        
        Score: {score}%
        Student Answer: {student_answer}
        Rubric: {json.dumps(rubric, indent=2)}
        
        Feedback should be:
        - Encouraging and constructive
        - Specific about strengths and weaknesses
        - Actionable for improvement
        - Aligned with learning objectives
        
        Format as encouraging paragraph with specific suggestions.
        """
        
        response = await self.ai_service.generate_content(prompt)
        return response.strip()
    
    async def update_analytics(self, graded_submission: Dict[str, Any]) -> Dict[str, Any]:
        """Update dashboard analytics based on graded submission"""
        
        student_id = graded_submission['student_id']
        assessment_id = graded_submission['assessment_id']
        score = graded_submission['percentage']
        
        analytics_update = {
            'student_performance': {
                'student_id': student_id,
                'latest_score': score,
                'assessment_count': 1,
                'average_score': score,
                'improvement_trend': 'stable',
                'weak_areas': [],
                'strong_areas': []
            },
            'class_analytics': {
                'assessment_id': assessment_id,
                'submission_count': 1,
                'average_score': score,
                'score_distribution': {
                    'A': 1 if score >= 90 else 0,
                    'B': 1 if 80 <= score < 90 else 0,
                    'C': 1 if 70 <= score < 80 else 0,
                    'D': 1 if 60 <= score < 70 else 0,
                    'F': 1 if score < 60 else 0
                }
            },
            'curriculum_insights': {
                'difficult_questions': [],
                'mastery_levels': {},
                'completion_rates': {}
            }
        }
        
        return analytics_update
    
    async def detect_plagiarism(self, submission: str, reference_submissions: List[str]) -> Dict[str, Any]:
        """Detect potential plagiarism in submissions"""
        
        prompt = f"""
        Analyze this submission for potential plagiarism against reference submissions.
        
        Current Submission: {submission}
        Reference Submissions: {json.dumps(reference_submissions, indent=2)}
        
        Check for:
        - Exact text matches
        - Paraphrased content
        - Similar structure/logic
        - Unusual similarity patterns
        
        Return JSON:
        {{
            "plagiarism_detected": false,
            "similarity_score": 15.5,
            "threshold": 70.0,
            "matches": [
                {{
                    "reference_id": "ref_1",
                    "similarity": 25.0,
                    "matched_sections": ["section1", "section2"]
                }}
            ],
            "recommendation": "no_action|review_required|investigation_needed"
        }}
        """
        
        response = await self.ai_service.generate_content(prompt)
        return json.loads(response)
    
    async def batch_grade_submissions(self, submissions: List[Dict], assessment: Dict) -> List[Dict]:
        """Grade multiple submissions efficiently"""
        
        graded_submissions = []
        
        for submission in submissions:
            try:
                graded = await self.grade_submission(submission, assessment)
                graded_submissions.append(graded)
                
                # Update analytics for each submission
                analytics = await self.update_analytics(graded)
                graded['analytics_update'] = analytics
                
            except Exception as e:
                graded_submissions.append({
                    'submission_id': submission.get('id'),
                    'error': f'Grading failed: {str(e)}',
                    'status': 'failed'
                })
        
        return graded_submissions