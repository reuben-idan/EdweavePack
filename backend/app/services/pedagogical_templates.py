from typing import Dict, List, Any
from enum import Enum

class EducationLevel(Enum):
    ELEMENTARY_K2 = "K-2"
    ELEMENTARY_35 = "3-5"
    MIDDLE_68 = "6-8"
    HIGH_912 = "9-12"
    UNIVERSITY = "University"

class PedagogicalTemplate:
    def __init__(self):
        self.templates = {
            "K-2": {
                "learning_duration": {"min": 15, "max": 30},
                "assessment_types": ["visual", "hands_on", "simple_mcq"],
                "bloom_focus": ["Remember", "Understand"],
                "activity_types": ["games", "stories", "drawing", "movement"],
                "vocabulary_level": "simple",
                "instruction_style": "concrete_examples"
            },
            "3-5": {
                "learning_duration": {"min": 20, "max": 45},
                "assessment_types": ["mcq", "short_answer", "project"],
                "bloom_focus": ["Remember", "Understand", "Apply"],
                "activity_types": ["experiments", "group_work", "presentations"],
                "vocabulary_level": "intermediate",
                "instruction_style": "guided_discovery"
            },
            "6-8": {
                "learning_duration": {"min": 30, "max": 60},
                "assessment_types": ["mcq", "short_answer", "essay", "project"],
                "bloom_focus": ["Understand", "Apply", "Analyze"],
                "activity_types": ["research", "debates", "labs", "peer_review"],
                "vocabulary_level": "advanced",
                "instruction_style": "inquiry_based"
            },
            "9-12": {
                "learning_duration": {"min": 45, "max": 90},
                "assessment_types": ["mcq", "essay", "project", "presentation"],
                "bloom_focus": ["Apply", "Analyze", "Evaluate", "Create"],
                "activity_types": ["research_projects", "case_studies", "simulations"],
                "vocabulary_level": "sophisticated",
                "instruction_style": "problem_based"
            },
            "University": {
                "learning_duration": {"min": 60, "max": 180},
                "assessment_types": ["essay", "research_paper", "thesis", "coding"],
                "bloom_focus": ["Analyze", "Evaluate", "Create"],
                "activity_types": ["independent_research", "peer_collaboration", "internships"],
                "vocabulary_level": "academic",
                "instruction_style": "self_directed"
            }
        }
    
    def get_template(self, level: str) -> Dict[str, Any]:
        return self.templates.get(level, self.templates["6-8"])
    
    def adapt_curriculum_for_level(self, curriculum_data: Dict[str, Any], level: str) -> Dict[str, Any]:
        template = self.get_template(level)
        
        # Adapt weekly modules based on level
        adapted_modules = []
        for module in curriculum_data.get("weekly_modules", []):
            adapted_module = module.copy()
            
            # Adjust duration based on level
            for block in adapted_module.get("content_blocks", []):
                current_duration = block.get("estimated_duration", 60)
                min_dur, max_dur = template["learning_duration"]["min"], template["learning_duration"]["max"]
                block["estimated_duration"] = max(min_dur, min(max_dur, current_duration))
                
                # Adapt activities for level
                block["activities"] = self._adapt_activities(block.get("activities", []), template)
            
            adapted_modules.append(adapted_module)
        
        curriculum_data["weekly_modules"] = adapted_modules
        curriculum_data["pedagogical_template"] = template
        curriculum_data["education_level"] = level
        
        return curriculum_data
    
    def _adapt_activities(self, activities: List[str], template: Dict[str, Any]) -> List[str]:
        level_activities = template["activity_types"]
        adapted = []
        
        for activity in activities:
            if any(level_act in activity.lower() for level_act in level_activities):
                adapted.append(activity)
            else:
                # Replace with level-appropriate activity
                adapted.append(level_activities[0] if level_activities else activity)
        
        return adapted
    
    def generate_scaffolded_project(self, subject: str, level: str, topic: str) -> Dict[str, Any]:
        template = self.get_template(level)
        
        if level in ["K-2", "3-5"]:
            return self._elementary_project(subject, topic, template)
        elif level in ["6-8"]:
            return self._middle_project(subject, topic, template)
        elif level in ["9-12"]:
            return self._high_school_project(subject, topic, template)
        else:  # University
            return self._university_project(subject, topic, template)
    
    def _elementary_project(self, subject: str, topic: str, template: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "title": f"My {topic} Discovery Book",
            "description": f"Create a picture book about {topic}",
            "duration_weeks": 2,
            "scaffolds": [
                {"step": 1, "task": "Draw what you know about the topic", "support": "Teacher guidance"},
                {"step": 2, "task": "Ask 3 questions about the topic", "support": "Question starters provided"},
                {"step": 3, "task": "Find answers with help", "support": "Guided research"},
                {"step": 4, "task": "Create your book pages", "support": "Templates provided"},
                {"step": 5, "task": "Share with class", "support": "Presentation tips"}
            ],
            "rubric": {
                "creativity": {"excellent": "Very creative pictures", "good": "Some creative ideas", "needs_work": "Basic pictures"},
                "content": {"excellent": "Shows understanding", "good": "Shows some understanding", "needs_work": "Needs more detail"},
                "effort": {"excellent": "Tried very hard", "good": "Good effort", "needs_work": "Could try harder"}
            }
        }
    
    def _middle_project(self, subject: str, topic: str, template: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "title": f"{topic} Investigation Project",
            "description": f"Research and present findings about {topic}",
            "duration_weeks": 3,
            "scaffolds": [
                {"step": 1, "task": "Develop research questions", "support": "Question framework provided"},
                {"step": 2, "task": "Gather information from 3+ sources", "support": "Source evaluation checklist"},
                {"step": 3, "task": "Organize findings", "support": "Graphic organizer templates"},
                {"step": 4, "task": "Create presentation", "support": "Presentation guidelines"},
                {"step": 5, "task": "Present and peer review", "support": "Feedback forms"}
            ],
            "rubric": {
                "research_quality": {"excellent": "Multiple reliable sources", "good": "Some reliable sources", "needs_improvement": "Limited sources"},
                "analysis": {"excellent": "Deep analysis and connections", "good": "Some analysis", "needs_improvement": "Surface level"},
                "presentation": {"excellent": "Clear, engaging delivery", "good": "Generally clear", "needs_improvement": "Unclear delivery"}
            }
        }
    
    def _high_school_project(self, subject: str, topic: str, template: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "title": f"Advanced {topic} Research Project",
            "description": f"Conduct independent research and analysis on {topic}",
            "duration_weeks": 4,
            "scaffolds": [
                {"step": 1, "task": "Literature review and hypothesis", "support": "Research methodology guide"},
                {"step": 2, "task": "Data collection/experimentation", "support": "Data collection protocols"},
                {"step": 3, "task": "Analysis and interpretation", "support": "Analysis frameworks"},
                {"step": 4, "task": "Draft research paper", "support": "Writing guidelines"},
                {"step": 5, "task": "Peer review and revision", "support": "Peer review rubric"},
                {"step": 6, "task": "Final presentation", "support": "Presentation standards"}
            ],
            "rubric": {
                "methodology": {"excellent": "Rigorous methodology", "good": "Sound methodology", "needs_improvement": "Weak methodology"},
                "analysis": {"excellent": "Sophisticated analysis", "good": "Adequate analysis", "needs_improvement": "Superficial analysis"},
                "communication": {"excellent": "Professional presentation", "good": "Clear communication", "needs_improvement": "Unclear communication"}
            }
        }
    
    def _university_project(self, subject: str, topic: str, template: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "title": f"Independent {topic} Research Thesis",
            "description": f"Original research contribution to {topic} field",
            "duration_weeks": 8,
            "scaffolds": [
                {"step": 1, "task": "Proposal and literature review", "support": "Faculty advisor meetings"},
                {"step": 2, "task": "Methodology development", "support": "IRB approval if needed"},
                {"step": 3, "task": "Data collection phase", "support": "Regular check-ins"},
                {"step": 4, "task": "Preliminary analysis", "support": "Statistical consultation"},
                {"step": 5, "task": "Draft chapters", "support": "Writing center resources"},
                {"step": 6, "task": "Peer and faculty review", "support": "Review committees"},
                {"step": 7, "task": "Revision and finalization", "support": "Editorial support"},
                {"step": 8, "task": "Defense presentation", "support": "Presentation coaching"}
            ],
            "rubric": {
                "originality": {"excellent": "Novel contribution", "good": "Some originality", "needs_improvement": "Limited novelty"},
                "rigor": {"excellent": "Methodologically sound", "good": "Generally rigorous", "needs_improvement": "Methodological issues"},
                "significance": {"excellent": "Important implications", "good": "Some significance", "needs_improvement": "Limited impact"}
            }
        }