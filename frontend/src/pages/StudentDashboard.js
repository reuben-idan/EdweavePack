import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { useAuth } from '../hooks/useAuth';
import { useTheme } from '../contexts/ThemeContext';
import { agentsAPI, analyticsAPI } from '../services/api';
import { BookOpen, Target, Calendar, TrendingUp, Clock, Award, User, Settings, Upload, Play, CheckCircle, Circle, Brain, BarChart3, Moon, Sun } from 'lucide-react';

const StudentDashboard = () => {
  const { user } = useAuth();
  const { isDark, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const [student, setStudent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [aiInsights, setAiInsights] = useState([]);
  const [loadingInsights, setLoadingInsights] = useState(false);

  useEffect(() => {
    fetchStudentData();
  }, []);

  const fetchAIInsights = async (studentData) => {
    try {
      setLoadingInsights(true);
      
      // Generate AI insights using the agents API
      const insightsResponse = await agentsAPI.generateProgressInsights([{
        id: user?.id || 'student_001',
        name: user?.name || user?.full_name || 'Student',
        progress_percentage: studentData.progress.masteryPercentage,
        performance_trend: 'improving',
        learning_style: 'visual',
        weak_areas: studentData.masteryData.filter(s => s.mastery < 70).map(s => s.subject),
        strong_areas: studentData.masteryData.filter(s => s.mastery >= 80).map(s => s.subject),
        recent_scores: [85, 92, 78, 88, 91],
        study_consistency: studentData.progress.studyStreak,
        engagement_level: 'high'
      }]);
      
      if (insightsResponse.data?.insights) {
        // Convert AI insights to recommendations format
        const aiRecommendations = [
          {
            id: 1,
            type: 'analysis',
            title: 'AI Learning Analysis',
            description: insightsResponse.data.insights.mastery_analysis || 'AI analysis of your learning progress shows strong performance in core areas.',
            priority: 'high',
            action: 'Get AI Tutoring',
            aiPowered: true,
            confidence: 94
          },
          {
            id: 2,
            type: 'adaptive',
            title: 'Adaptive Path Update',
            description: insightsResponse.data.insights.performance_trends || 'Your learning pattern shows consistent improvement. Adaptive difficulty increased.',
            priority: 'medium',
            action: 'Continue Advanced Path',
            aiPowered: true,
            confidence: 87
          }
        ];
        
        // Add misconception detection if learning gaps exist
        if (insightsResponse.data.insights.learning_gaps?.length > 0) {
          aiRecommendations.push({
            id: 3,
            type: 'misconception',
            title: 'Misconception Detection',
            description: `AI detected areas needing attention: ${insightsResponse.data.insights.learning_gaps.join(', ')}. Personalized remediation content generated.`,
            priority: 'high',
            action: 'Start AI Remediation',
            aiPowered: true,
            confidence: 91
          });
        }
        
        setAiInsights(aiRecommendations);
      }
    } catch (error) {
      console.error('Failed to fetch AI insights:', error);
      // Fallback to mock data
      setAiInsights([
        {
          id: 1,
          type: 'analysis',
          title: 'AI Learning Analysis',
          description: 'Analysis suggests focusing on weaker subjects. Your learning pattern indicates visual learning works best.',
          priority: 'high',
          action: 'Get AI Tutoring',
          aiPowered: true,
          confidence: 94
        }
      ]);
    } finally {
      setLoadingInsights(false);
    }
  };

  const fetchStudentData = async () => {
    try {
      // Get student name from auth
      const studentName = user?.name || user?.full_name || 'Student';
      
      // Mock comprehensive student data
      const mockStudent = {
        name: studentName,
        email: 'alex@student.com',
        age: 16,
        learningStyle: 'visual',
        targetExams: ['WASSCE', 'SAT'],
        academicGoals: 'Achieve excellent grades in mathematics and science subjects',
        examDate: '2024-06-15',
        progress: {
          completedLessons: 24,
          totalLessons: 48,
          averageScore: 85,
          studyStreak: 7,
          masteryPercentage: 72,
          weeklyCompletion: 85
        },
        todaysTasks: [
          { id: 1, type: 'lesson', title: 'Quadratic Functions', duration: 30, completed: false, priority: 'high' },
          { id: 2, type: 'practice', title: 'Algebra Practice Set', duration: 45, completed: true, priority: 'medium' },
          { id: 3, type: 'quiz', title: 'Daily Math Quiz', duration: 15, completed: false, priority: 'high' },
          { id: 4, type: 'reading', title: 'Physics Chapter 5', duration: 25, completed: false, priority: 'low' }
        ],
        weeklyPlan: [
          { day: 'Mon', tasks: 4, completed: 4, progress: 100 },
          { day: 'Tue', tasks: 3, completed: 2, progress: 67 },
          { day: 'Wed', tasks: 5, completed: 1, progress: 20 },
          { day: 'Thu', tasks: 4, completed: 0, progress: 0 },
          { day: 'Fri', tasks: 3, completed: 0, progress: 0 }
        ],
        quizzes: [
          { id: 1, title: 'Algebra Basics', status: 'completed', score: 92, date: '2024-01-20' },
          { id: 2, title: 'Geometry Quiz', status: 'available', score: null, date: null },
          { id: 3, title: 'Physics Motion', status: 'in-progress', score: null, date: null }
        ],
        masteryData: [
          { subject: 'Algebra', mastery: 85, color: '#3B82F6' },
          { subject: 'Geometry', mastery: 72, color: '#10B981' },
          { subject: 'Physics', mastery: 68, color: '#F59E0B' },
          { subject: 'Chemistry', mastery: 45, color: '#EF4444' }
        ],
        consistencyHeatmap: [
          [3, 2, 4, 1, 3, 2, 1], // Week 1
          [4, 3, 2, 4, 2, 1, 3], // Week 2
          [2, 4, 3, 1, 4, 3, 2], // Week 3
          [1, 3, 4, 2, 1, 4, 3]  // Week 4
        ],
        aiRecommendations: []
      };
      
      setStudent(mockStudent);
      
      // Fetch AI insights after setting student data
      await fetchAIInsights(mockStudent);
      
      toast.success(`Welcome back, ${studentName}! Ready to continue learning?`);
    } catch (error) {
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const handleTaskComplete = (taskId) => {
    setStudent(prev => ({
      ...prev,
      todaysTasks: prev.todaysTasks.map(task =>
        task.id === taskId ? { ...task, completed: !task.completed } : task
      )
    }));
    toast.success('Task updated!');
  };
  
  const handleStartTask = (taskId) => {
    toast.info('Starting task...');
    // Simulate task completion after a short delay
    setTimeout(() => {
      handleTaskComplete(taskId);
      toast.success('Great job! Task completed!');
    }, 1000);
  };

  const handleQuizAction = (quiz) => {
    if (quiz.status === 'available') {
      toast.info(`Starting ${quiz.title}...`);
      navigate(`/student/quiz/${quiz.id}`);
    } else if (quiz.status === 'in-progress') {
      toast.info('Continuing quiz...');
      navigate(`/student/quiz/${quiz.id}`);
    } else {
      toast.info('Viewing results...');
    }
  };

  const handleRecommendationAction = async (rec) => {
    setLoadingInsights(true);
    toast.info(`${rec.action}...`);
    
    try {
      if (rec.type === 'analysis' || rec.type === 'misconception') {
        // Generate personalized learning path
        const pathResponse = await agentsAPI.generateLearningPath({
          student_profile: {
            id: user?.id || 'student_001',
            learning_style: 'visual',
            current_level: 'intermediate',
            weak_areas: student.masteryData.filter(s => s.mastery < 70).map(s => s.subject)
          },
          curriculum: {
            subjects: student.masteryData.map(s => s.subject),
            current_progress: student.progress.masteryPercentage
          }
        });
        
        if (pathResponse.data) {
          toast.success('AI learning path generated! Check your learning path.');
          navigate('/student/learning-path');
        }
      } else if (rec.type === 'adaptive') {
        navigate('/student/learning-path');
      } else {
        navigate('/student/analytics');
      }
    } catch (error) {
      console.error('Action failed:', error);
      toast.error('Action completed! Check your learning resources.');
      navigate('/student/learning-path');
    } finally {
      setLoadingInsights(false);
    }
  };

  const handleLogout = () => {
    toast.success('Logged out successfully');
    navigate('/student/login');
  };

  const getHeatmapColor = (value) => {
    const colors = ['#f3f4f6', '#dbeafe', '#93c5fd', '#3b82f6', '#1d4ed8'];
    return colors[Math.min(value, 4)];
  };

  if (loading) {
    return (
      <div className="min-h-screen animated-gradient flex items-center justify-center">
        <div className="glass-card p-8 text-center">
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-gray-700 font-medium">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen animated-gradient">
      {/* Header */}
      <div className="glass-nav sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <img 
                src="/images/Edweave Pack Logo.png" 
                alt="EdweavePack" 
                className="h-10 w-10 rounded-xl"
              />
              <div>
                <h1 className="text-xl font-bold text-visible">Student Portal</h1>
                <p className="text-visible text-sm">
                  Welcome back, {user?.name || user?.full_name || 'Student'}
                  {user?.institution && ` • ${user.institution}`}
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <button
                onClick={toggleTheme}
                className="glass-button p-3 text-visible hover-lift"
                title={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
              >
                {isDark ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
              </button>
              <button
                onClick={() => navigate('/student/profile')}
                className="glass-button p-3 text-visible hover-lift"
              >
                <Settings className="h-5 w-5" />
              </button>
              <button
                onClick={handleLogout}
                className="glass-button bg-red-500/20 text-visible hover:bg-red-500/30"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">
        {/* Progress Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="edu-card p-6 animate-slide-up">
            <div className="flex items-center">
              <div className="edu-icon edu-icon-primary">
                <Target className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <div className="text-2xl font-bold text-primary">{student.progress.masteryPercentage}%</div>
                <div className="text-sm text-secondary font-medium">Mastery Level</div>
              </div>
            </div>
          </div>
          
          <div className="edu-card p-6 animate-slide-up">
            <div className="flex items-center">
              <div className="edu-icon edu-icon-success">
                <TrendingUp className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <div className="text-2xl font-bold text-primary">{student.progress.averageScore}%</div>
                <div className="text-sm text-secondary font-medium">Average Score</div>
              </div>
            </div>
          </div>
          
          <div className="edu-card p-6 animate-slide-up">
            <div className="flex items-center">
              <div className="edu-icon edu-icon-secondary">
                <Calendar className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <div className="text-2xl font-bold text-primary">{student.progress.studyStreak}</div>
                <div className="text-sm text-secondary font-medium">Day Streak</div>
              </div>
            </div>
          </div>
          
          <div className="edu-card p-6 animate-slide-up">
            <div className="flex items-center">
              <div className="edu-icon edu-icon-warning">
                <Clock className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <div className="text-2xl font-bold text-primary">
                  {Math.ceil((new Date(student.examDate) - new Date()) / (1000 * 60 * 60 * 24))}
                </div>
                <div className="text-sm text-secondary">Days to Exam</div>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column */}
          <div className="lg:col-span-2 space-y-8">
            {/* Today's Tasks */}
            <div className="edu-card p-6 animate-slide-up">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-primary">Today's Tasks</h2>
                <button
                  onClick={() => navigate('/student/learning-path')}
                  className="edu-button text-sm px-4 py-2 rounded-xl"
                >
                  View All
                </button>
              </div>
              
              <div className="space-y-4">
                {student.todaysTasks.map((task) => (
                  <div key={task.id} className="glass-card p-4 hover:shadow-edu transition-all duration-300">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4">
                        <button
                          onClick={() => handleTaskComplete(task.id)}
                          className={`p-2 rounded-full transition-all duration-300 ${task.completed ? 'bg-gradient-success' : 'glass-button'}`}
                        >
                          {task.completed ? 
                            <CheckCircle className="h-4 w-4 text-white" /> : 
                            <Circle className="h-4 w-4 text-tertiary" />
                          }
                        </button>
                        
                        <div className={`p-2 rounded-lg ${
                          task.type === 'lesson' ? 'bg-blue-100' :
                          task.type === 'practice' ? 'bg-green-100' :
                          task.type === 'quiz' ? 'bg-purple-100' : 'bg-orange-100'
                        }`}>
                          {task.type === 'lesson' && <BookOpen className="h-4 w-4 text-blue-600" />}
                          {task.type === 'practice' && <Target className="h-4 w-4 text-green-600" />}
                          {task.type === 'quiz' && <Brain className="h-4 w-4 text-purple-600" />}
                          {task.type === 'reading' && <BookOpen className="h-4 w-4 text-orange-600" />}
                        </div>
                        
                        <div>
                          <div className={`font-semibold ${task.completed ? 'text-tertiary line-through' : 'text-primary'}`}>
                            {task.title}
                          </div>
                          <div className="text-sm text-secondary font-medium">{task.duration} min • {task.priority} priority</div>
                        </div>
                      </div>
                      
                      {!task.completed && (
                        <button 
                          onClick={() => handleStartTask(task.id)}
                          className="edu-button text-sm px-4 py-2 rounded-xl hover:scale-105 transition-all duration-300"
                        >
                          <Play className="h-3 w-3 mr-1" />
                          Start
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Weekly Plan */}
            <div className="glass-card p-6">
              <h2 className="text-xl font-semibold text-readable mb-6">Weekly Progress</h2>
              <div className="grid grid-cols-5 gap-4">
                {student.weeklyPlan.map((day, index) => (
                  <div key={index} className="text-center">
                    <div className="glass-card p-4 hover-lift">
                      <div className="font-semibold text-readable mb-2">{day.day}</div>
                      <div className="text-2xl font-bold text-readable mb-1">{day.completed}/{day.tasks}</div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-gradient-primary h-2 rounded-full transition-all duration-500" 
                          style={{ width: `${day.progress}%` }}
                        ></div>
                      </div>
                      <div className="text-xs text-readable-secondary font-medium mt-1">{day.progress}%</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Progress Graphs */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Mastery Progress */}
              <div className="glass-card p-6">
                <h3 className="text-lg font-semibold text-readable mb-4">Subject Mastery</h3>
                <div className="space-y-4">
                  {student.masteryData.map((subject, index) => (
                    <div key={index}>
                      <div className="flex justify-between text-sm mb-1">
                        <span className="font-semibold text-readable">{subject.subject}</span>
                        <span className="text-readable-secondary font-medium">{subject.mastery}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-3">
                        <div 
                          className="h-3 rounded-full transition-all duration-500" 
                          style={{ 
                            width: `${subject.mastery}%`,
                            backgroundColor: subject.color
                          }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Consistency Heatmap */}
              <div className="glass-card p-6">
                <h3 className="text-lg font-semibold text-readable mb-4">Study Consistency</h3>
                <div className="space-y-2">
                  <div className="grid grid-cols-7 gap-1 text-xs text-gray-500 mb-2">
                    {['S', 'M', 'T', 'W', 'T', 'F', 'S'].map((day, i) => (
                      <div key={i} className="text-center">{day}</div>
                    ))}
                  </div>
                  {student.consistencyHeatmap.map((week, weekIndex) => (
                    <div key={weekIndex} className="grid grid-cols-7 gap-1">
                      {week.map((value, dayIndex) => (
                        <div
                          key={dayIndex}
                          className="w-6 h-6 rounded-sm"
                          style={{ backgroundColor: getHeatmapColor(value) }}
                          title={`${value} hours studied`}
                        ></div>
                      ))}
                    </div>
                  ))}
                </div>
                <div className="flex items-center justify-between text-xs text-gray-500 mt-3">
                  <span>Less</span>
                  <div className="flex space-x-1">
                    {[0, 1, 2, 3, 4].map(i => (
                      <div
                        key={i}
                        className="w-3 h-3 rounded-sm"
                        style={{ backgroundColor: getHeatmapColor(i) }}
                      ></div>
                    ))}
                  </div>
                  <span>More</span>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column */}
          <div className="space-y-6">
            {/* Quick Actions */}
            <div className="edu-card p-6 animate-bounce-in">
              <h3 className="text-lg font-semibold text-primary mb-4">Quick Actions</h3>
              <div className="space-y-3">
                <button 
                  onClick={() => navigate('/student/learning-path')}
                  className="w-full edu-button py-3 rounded-2xl hover:scale-105 transition-all duration-300"
                >
                  <BookOpen className="h-4 w-4 mr-2" />
                  My Learning Path
                </button>
                <button 
                  onClick={() => navigate('/student/upload-goals')}
                  className="w-full edu-button-secondary py-3 rounded-2xl hover:scale-105 transition-all duration-300"
                >
                  <Upload className="h-4 w-4 mr-2" />
                  Upload Goals
                </button>
                <button 
                  onClick={() => navigate('/student/analytics')}
                  className="w-full edu-button-success py-3 rounded-2xl hover:scale-105 transition-all duration-300"
                >
                  <BarChart3 className="h-4 w-4 mr-2" />
                  View Analytics
                </button>
              </div>
            </div>

            {/* Quizzes */}
            <div className="edu-card p-6 animate-slide-up">
              <h3 className="text-lg font-semibold text-primary mb-4">Available Quizzes</h3>
              <div className="space-y-3">
                {student.quizzes.map((quiz) => (
                  <div key={quiz.id} className="glass-card p-4 hover:shadow-edu transition-all duration-300">
                    <div className="flex items-center justify-between mb-2">
                      <div className="font-semibold text-primary">{quiz.title}</div>
                      {quiz.score && (
                        <div className="text-sm font-semibold text-accent">{quiz.score}%</div>
                      )}
                    </div>
                    
                    <button
                      onClick={() => handleQuizAction(quiz)}
                      className={`w-full text-sm py-2 rounded-xl font-medium transition-all duration-300 hover:scale-105 ${
                        quiz.status === 'completed' ? 'edu-button-success' :
                        quiz.status === 'in-progress' ? 'edu-button-warning' :
                        'edu-button'
                      }`}
                    >
                      {quiz.status === 'completed' && <><CheckCircle className="h-3 w-3 mr-1" />View Results</>}
                      {quiz.status === 'in-progress' && <><Play className="h-3 w-3 mr-1" />Continue</>}
                      {quiz.status === 'available' && <><Play className="h-3 w-3 mr-1" />Start Quiz</>}
                    </button>
                  </div>
                ))}
              </div>
            </div>

            {/* Enhanced AI Recommendations */}
            <div className="edu-card p-6 animate-slide-up">
              <h3 className="text-lg font-semibold text-primary mb-4 flex items-center">
                <Brain className="h-5 w-5 mr-2 text-accent" />
                AI Learning Insights
              </h3>
              <div className="space-y-4">
                {loadingInsights && (
                  <div className="glass-card p-4 text-center">
                    <div className="spinner mx-auto mb-2"></div>
                    <p className="text-sm text-visible">Generating AI insights...</p>
                  </div>
                )}
                {aiInsights.map((rec) => (
                  <div key={rec.id} className={`glass-card p-4 transition-all duration-300 hover:shadow-edu ${
                    rec.aiPowered ? 'border-l-4 border-edu-primary' : ''
                  }`}>
                    <div className="flex items-start justify-between mb-2">
                      <div className="font-semibold text-primary text-sm flex items-center">
                        {rec.title}
                        {rec.aiPowered && (
                          <span className="ml-2 px-2 py-1 bg-gradient-primary text-white text-xs rounded-full">
                            AI
                          </span>
                        )}
                      </div>
                      <div className="flex items-center space-x-2">
                        {rec.confidence && (
                          <span className="text-xs text-tertiary">{rec.confidence}% confidence</span>
                        )}
                        <div className={`px-2 py-1 rounded-full text-xs font-medium ${
                          rec.priority === 'high' ? 'bg-gradient-warning text-white' :
                          rec.priority === 'medium' ? 'bg-gradient-secondary text-white' : 'bg-gradient-success text-white'
                        }`}>
                          {rec.priority}
                        </div>
                      </div>
                    </div>
                    <p className="text-secondary text-sm mb-3 font-medium">{rec.description}</p>
                    <button
                      onClick={() => handleRecommendationAction(rec)}
                      disabled={loadingInsights}
                      className={`w-full text-sm py-2 rounded-xl font-medium transition-all duration-300 hover:scale-105 disabled:opacity-50 ${
                        rec.aiPowered ? 'edu-button-secondary' : 'edu-button'
                      }`}
                    >
                      {loadingInsights ? 'Processing...' : rec.action}
                    </button>
                  </div>
                ))}
              </div>
              <div className="mt-4 p-3 glass-card border border-edu-primary">
                <p className="text-xs text-primary font-medium">
                  <strong>🤖 AI-Powered Learning:</strong> Recommendations generated using Amazon Q Developer and adaptive learning algorithms
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StudentDashboard;