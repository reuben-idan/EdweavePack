from app.core.database import Base
from .user import User
from .curriculum import Curriculum, Assessment, Question
from .student import Student, StudentLearningPath, WeeklyPlan, DailyTask, StudentQuiz, StudentQuizResult, ProgressSnapshot
from .files import File, Module, StudentResponse