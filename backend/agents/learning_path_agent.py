import json
from typing import Dict, Any, List
from datetime import datetime, timedelta

class LearningPathAgent:
    """AI agent for generating personalized learning paths"""
    
    def __init__(self):
        self.bloom_levels = [
            "remember", "understand", "apply", 
            "analyze", "evaluate", "create"
        ]
        
    def generate_path(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized learning path using AI"""
        
        profile = student_data["student_profile"]
        goals = student_data["goals"]
        
        # Calculate timeline
        exam_date = profile.get("exam_date")
        if exam_date:
            weeks_available = max(4, (datetime.fromisoformat(str(exam_date)) - datetime.now()).days // 7)
        else:
            weeks_available = 12  # Default 3 months
            
        # Determine difficulty progression
        difficulty_level = self._determine_difficulty(profile, goals)
        
        # Generate weekly structure
        weekly_structure = self._generate_weekly_structure(
            goals["subjects"], 
            weeks_available, 
            difficulty_level,
            profile["learning_style"]
        )
        
        return {
            "title": f"Personalized {', '.join(goals['subjects'][:2])} Learning Path",
            "description": f"AI-generated path for {profile['target_exams']} preparation",
            "total_weeks": weeks_available,
            "difficulty_level": difficulty_level,
            "metadata": {
                "learning_style": profile["learning_style"],
                "target_exams": profile["target_exams"],
                "focus_subjects": goals["subjects"]
            },
            "weekly_structure": weekly_structure
        }
    
    def _determine_difficulty(self, profile: Dict, goals: Dict) -> str:
        """Determine appropriate difficulty level"""
        age = profile.get("age", 16)
        target_exams = profile.get("target_exams", [])
        
        if age < 14 or "BECE" in target_exams:
            return "beginner"
        elif "WASSCE" in target_exams or "IGCSE" in target_exams:
            return "intermediate"
        elif "SAT" in target_exams or "University" in str(target_exams):
            return "advanced"
        else:
            return "intermediate"
    
    def _generate_weekly_structure(self, subjects: List[str], weeks: int, 
                                 difficulty: str, learning_style: str) -> Dict[str, Any]:
        """Generate week-by-week learning structure"""
        
        weekly_plans = []
        
        for week_num in range(1, min(weeks + 1, 16)):  # Max 16 weeks
            week_topics = self._select_week_topics(subjects, week_num, difficulty)
            
            weekly_plan = {
                "week_number": week_num,
                "title": f"Week {week_num}: {week_topics[0] if week_topics else 'Review'}",
                "topics": week_topics,
                "difficulty": self._get_week_difficulty(week_num, difficulty),
                "estimated_hours": self._calculate_weekly_hours(week_num, difficulty),
                "daily_structure": self._generate_daily_structure(
                    week_topics, learning_style, difficulty
                )
            }
            weekly_plans.append(weekly_plan)
        
        return {"weeks": weekly_plans}
    
    def _select_week_topics(self, subjects: List[str], week_num: int, difficulty: str) -> List[str]:
        """Select topics for a specific week"""
        
        # Topic progression templates by subject
        topic_progressions = {
            "Mathematics": [
                "Basic Operations", "Linear Equations", "Quadratic Functions",
                "Polynomials", "Exponential Functions", "Logarithms",
                "Trigonometry", "Calculus Basics", "Statistics", "Probability"
            ],
            "Physics": [
                "Motion and Forces", "Energy and Work", "Waves and Sound",
                "Electricity", "Magnetism", "Light and Optics",
                "Atomic Physics", "Thermodynamics", "Modern Physics"
            ],
            "Chemistry": [
                "Atomic Structure", "Chemical Bonding", "Stoichiometry",
                "Acids and Bases", "Redox Reactions", "Organic Chemistry",
                "Thermochemistry", "Kinetics", "Equilibrium"
            ]
        }
        
        selected_topics = []
        for subject in subjects[:2]:  # Focus on max 2 subjects per week
            if subject in topic_progressions:
                topics = topic_progressions[subject]
                if week_num <= len(topics):
                    selected_topics.append(topics[week_num - 1])
        
        return selected_topics
    
    def _get_week_difficulty(self, week_num: int, base_difficulty: str) -> str:
        """Determine difficulty for specific week"""
        if week_num <= 2:
            return "beginner"
        elif week_num <= 6:
            return base_difficulty
        else:
            difficulty_map = {
                "beginner": "intermediate",
                "intermediate": "advanced",
                "advanced": "advanced"
            }
            return difficulty_map.get(base_difficulty, "intermediate")
    
    def _calculate_weekly_hours(self, week_num: int, difficulty: str) -> float:
        """Calculate estimated hours for week"""
        base_hours = {
            "beginner": 6,
            "intermediate": 8,
            "advanced": 10
        }
        
        hours = base_hours.get(difficulty, 8)
        
        # Increase hours slightly as weeks progress
        if week_num > 4:
            hours += 1
        if week_num > 8:
            hours += 1
            
        return min(hours, 12)  # Cap at 12 hours
    
    def _generate_daily_structure(self, topics: List[str], learning_style: str, 
                                difficulty: str) -> Dict[str, Any]:
        """Generate daily task structure for the week"""
        
        days = ["monday", "tuesday", "wednesday", "thursday", "friday"]
        daily_structure = {"days": []}
        
        for i, day in enumerate(days):
            day_tasks = self._generate_day_tasks(
                topics, i + 1, learning_style, difficulty
            )
            
            daily_structure["days"].append({
                "day_of_week": i + 1,
                "day_name": day.capitalize(),
                "tasks": day_tasks
            })
        
        return daily_structure
    
    def _generate_day_tasks(self, topics: List[str], day_num: int, 
                          learning_style: str, difficulty: str) -> List[Dict[str, Any]]:
        """Generate tasks for a specific day"""
        
        tasks = []
        
        # Task templates based on learning style
        style_tasks = {
            "visual": [
                {"type": "lesson", "title": "Watch Video Tutorial", "duration": 25},
                {"type": "practice", "title": "Complete Diagram Exercises", "duration": 30},
                {"type": "reading", "title": "Review Visual Examples", "duration": 20}
            ],
            "auditory": [
                {"type": "lesson", "title": "Listen to Audio Lesson", "duration": 30},
                {"type": "practice", "title": "Discuss Concepts Aloud", "duration": 25},
                {"type": "reading", "title": "Read and Summarize", "duration": 20}
            ],
            "reading": [
                {"type": "reading", "title": "Read Chapter Content", "duration": 35},
                {"type": "practice", "title": "Written Exercises", "duration": 30},
                {"type": "reflection", "title": "Create Notes", "duration": 15}
            ],
            "kinesthetic": [
                {"type": "practice", "title": "Hands-on Activities", "duration": 35},
                {"type": "lesson", "title": "Interactive Simulation", "duration": 25},
                {"type": "reflection", "title": "Build Models", "duration": 20}
            ]
        }
        
        # Select appropriate tasks
        base_tasks = style_tasks.get(learning_style, style_tasks["reading"])
        
        for i, task_template in enumerate(base_tasks[:3]):  # Max 3 tasks per day
            if i < len(topics):
                topic = topics[i]
            else:
                topic = topics[0] if topics else "General Review"
                
            task = {
                "type": task_template["type"],
                "title": f"{task_template['title']}: {topic}",
                "description": f"Focus on {topic} concepts and applications",
                "duration": task_template["duration"],
                "priority": "high" if i == 0 else "medium"
            }
            tasks.append(task)
        
        # Add quiz on specific days
        if day_num in [2, 4]:  # Tuesday and Thursday
            tasks.append({
                "type": "quiz",
                "title": f"Quick Quiz: {topics[0] if topics else 'Review'}",
                "description": "Test your understanding with a short quiz",
                "duration": 15,
                "priority": "high"
            })
        
        return tasks