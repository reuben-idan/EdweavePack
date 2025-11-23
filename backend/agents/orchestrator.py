import asyncio
import json
from typing import Dict, List, Any
from agents.curriculum_architect import CurriculumArchitectAgent
from agents.assessment_generator import AssessmentGeneratorAgent
from agents.personalized_learning import PersonalizedLearningAgent
from agents.auto_grader import AutoGraderAgent

class AgentOrchestrator:
    """Orchestrates multiple AI agents for comprehensive educational content generation"""
    
    def __init__(self):
        self.curriculum_agent = CurriculumArchitectAgent()
        self.assessment_agent = AssessmentGeneratorAgent()
        self.learning_agent = PersonalizedLearningAgent()
        self.grader_agent = AutoGraderAgent()
    
    async def create_complete_curriculum(self, content: str, level: str, subject: str, student_profiles: List[Dict] = None) -> Dict[str, Any]:
        """Orchestrate complete curriculum creation with all agents"""
        
        # Step 1: Generate base curriculum
        curriculum = await self.curriculum_agent.generate_curriculum(content, level, subject)
        
        # Step 2: Generate assessments for each module
        assessments = []
        for module in curriculum['modules']:
            assessment = await self.assessment_agent.generate_assessment(module)
            assessments.append(assessment)
        
        curriculum['assessments'] = assessments
        
        # Step 3: Create personalized learning paths if student profiles provided
        if student_profiles:
            learning_paths = []
            for profile in student_profiles:
                path = await self.learning_agent.generate_learning_path(profile, curriculum)
                learning_paths.append(path)
            curriculum['personalized_paths'] = learning_paths
        
        # Step 4: Generate prerequisite mapping
        prerequisite_map = await self.curriculum_agent.generate_prerequisite_map(curriculum['modules'])
        curriculum['prerequisites'] = prerequisite_map
        
        return curriculum
    
    async def process_student_submission(self, submission: Dict[str, Any], assessment: Dict[str, Any], student_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Process student submission with grading and personalized recommendations"""
        
        # Step 1: Grade the submission
        graded_result = await self.grader_agent.grade_submission(submission, assessment)
        
        # Step 2: Update student performance profile
        updated_profile = await self._update_student_profile(student_profile, graded_result)
        
        # Step 3: Generate next learning recommendations
        recommendations = await self.learning_agent.recommend_next_activities(
            student_profile['id'], 
            updated_profile['progress']
        )
        
        # Step 4: Check if remediation is needed
        if graded_result['percentage'] < 70:
            weak_areas = self._identify_weak_areas(graded_result)
            remediation_plan = await self.learning_agent.generate_remediation_plan(
                student_profile['id'], 
                weak_areas
            )
            graded_result['remediation_plan'] = remediation_plan
        
        graded_result['recommendations'] = recommendations
        graded_result['updated_profile'] = updated_profile
        
        return graded_result
    
    async def adapt_curriculum_for_class(self, curriculum: Dict[str, Any], class_performance: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt curriculum based on overall class performance"""
        
        # Analyze class performance patterns
        struggling_topics = class_performance.get('struggling_topics', [])
        mastered_topics = class_performance.get('mastered_topics', [])
        average_pace = class_performance.get('average_pace', 'normal')
        
        adapted_curriculum = curriculum.copy()
        
        # Adapt modules based on performance
        for module in adapted_curriculum['modules']:
            if module['title'] in struggling_topics:
                # Add remediation content
                module['remediation_activities'] = await self._generate_remediation_activities(module)
                # Extend timeline
                module['extended_timeline'] = True
            
            elif module['title'] in mastered_topics:
                # Add enrichment activities
                module['enrichment_activities'] = await self._generate_enrichment_activities(module)
                # Allow acceleration
                module['accelerated_option'] = True
        
        return adapted_curriculum
    
    async def generate_progress_insights(self, student_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive progress insights for dashboard"""
        
        insights = {
            'class_overview': {
                'total_students': len(student_data),
                'average_progress': 0,
                'completion_rate': 0,
                'engagement_level': 'medium'
            },
            'performance_trends': {
                'improving_students': [],
                'struggling_students': [],
                'consistent_performers': []
            },
            'content_effectiveness': {
                'high_performing_modules': [],
                'challenging_modules': [],
                'engagement_by_activity_type': {}
            },
            'recommendations': {
                'curriculum_adjustments': [],
                'teaching_strategies': [],
                'individual_interventions': []
            }
        }
        
        # Analyze student performance patterns
        total_progress = 0
        completed_students = 0
        
        for student in student_data:
            progress = student.get('progress_percentage', 0)
            total_progress += progress
            
            if progress >= 100:
                completed_students += 1
            
            # Categorize student performance trends
            trend = student.get('performance_trend', 'stable')
            if trend == 'improving':
                insights['performance_trends']['improving_students'].append(student['id'])
            elif trend == 'declining':
                insights['performance_trends']['struggling_students'].append(student['id'])
            else:
                insights['performance_trends']['consistent_performers'].append(student['id'])
        
        insights['class_overview']['average_progress'] = total_progress / len(student_data) if student_data else 0
        insights['class_overview']['completion_rate'] = (completed_students / len(student_data)) * 100 if student_data else 0
        
        return insights
    
    async def _update_student_profile(self, profile: Dict[str, Any], graded_result: Dict[str, Any]) -> Dict[str, Any]:
        """Update student profile based on latest assessment results"""
        
        updated_profile = profile.copy()
        
        # Update performance metrics
        if 'performance_history' not in updated_profile:
            updated_profile['performance_history'] = []
        
        updated_profile['performance_history'].append({
            'assessment_id': graded_result['assessment_id'],
            'score': graded_result['percentage'],
            'date': graded_result['graded_at'],
            'time_spent': graded_result.get('time_spent', 0)
        })
        
        # Calculate new averages
        scores = [h['score'] for h in updated_profile['performance_history']]
        updated_profile['average_score'] = sum(scores) / len(scores)
        
        # Update learning velocity
        if len(scores) >= 2:
            recent_trend = scores[-2:]
            if recent_trend[-1] > recent_trend[-2]:
                updated_profile['performance_trend'] = 'improving'
            elif recent_trend[-1] < recent_trend[-2]:
                updated_profile['performance_trend'] = 'declining'
            else:
                updated_profile['performance_trend'] = 'stable'
        
        return updated_profile
    
    def _identify_weak_areas(self, graded_result: Dict[str, Any]) -> List[str]:
        """Identify weak areas from graded submission"""
        
        weak_areas = []
        
        for question_score in graded_result.get('question_scores', []):
            if question_score['score'] / question_score['max_score'] < 0.6:
                # Extract topic/concept from question
                weak_areas.extend(question_score.get('improvements', []))
        
        return list(set(weak_areas))  # Remove duplicates
    
    async def _generate_remediation_activities(self, module: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate additional remediation activities for struggling topics"""
        
        prompt = f"""
        Generate remediation activities for students struggling with this module:
        
        Module: {json.dumps(module, indent=2)}
        
        Create 3-5 scaffolded activities that:
        - Break down complex concepts
        - Provide additional practice
        - Use different learning modalities
        - Include self-assessment checkpoints
        
        Return JSON array of activities.
        """
        
        response = await self.curriculum_agent.ai_service.generate_content(prompt)
        return json.loads(response)
    
    async def _generate_enrichment_activities(self, module: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate enrichment activities for advanced students"""
        
        prompt = f"""
        Generate enrichment activities for students who have mastered this module:
        
        Module: {json.dumps(module, indent=2)}
        
        Create 3-5 challenging activities that:
        - Extend learning beyond basic requirements
        - Encourage creative application
        - Connect to real-world scenarios
        - Promote higher-order thinking
        
        Return JSON array of activities.
        """
        
        response = await self.curriculum_agent.ai_service.generate_content(prompt)
        return json.loads(response)