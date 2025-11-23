import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { BookOpen, Target, Calendar, TrendingUp, Clock, Award, User, Settings, Upload, Play, CheckCircle, Circle, Brain, BarChart3 } from 'lucide-react';

const StudentDashboard = () => {
  const navigate = useNavigate();
  const [student, setStudent] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStudentData();
  }, []);

  const fetchStudentData = async () => {
    try {
      // Mock comprehensive student data
      const mockStudent = {
        name: 'Alex Johnson',
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
        aiRecommendations: [
          {
            id: 1,
            type: 'focus',
            title: 'Strengthen Chemistry Fundamentals',
            description: 'Your chemistry scores are below target. Spend 20 extra minutes daily on basic concepts.',
            priority: 'high',
            action: 'Start Chemistry Basics'
          },
          {
            id: 2,
            type: 'practice',
            title: 'Increase Geometry Practice',
            description: 'Great progress! Add 2 more geometry problems daily to maintain momentum.',
            priority: 'medium',
            action: 'Practice Now'
          },
          {
            id: 3,
            type: 'review',
            title: 'Review Quadratic Equations',
            description: 'You missed 3 questions on quadratics. Quick review recommended before moving forward.',
            priority: 'high',
            action: 'Review Topic'
          },
          {
            id: 4,
            type: 'achievement',
            title: 'Excellent Algebra Progress!',
            description: 'You\'ve mastered 85% of algebra concepts. Ready for advanced topics.',
            priority: 'low',
            action: 'Continue Learning'
          }
        ]
      };
      
      setStudent(mockStudent);
      toast.success('Welcome back! Ready to continue learning?');
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

  const handleRecommendationAction = (rec) => {
    toast.info(`${rec.action}...`);
    if (rec.type === 'focus' || rec.type === 'practice') {
      navigate('/student/learning-path');
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
                <h1 className="text-xl font-bold text-white">Student Portal</h1>
                <p className="text-white/80 text-sm">Welcome back, {student?.name}</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/student/profile')}
                className="glass-button p-3 text-white hover-lift"
              >
                <Settings className="h-5 w-5" />
              </button>
              <button
                onClick={handleLogout}
                className="glass-button bg-red-500/20 text-white hover:bg-red-500/30"
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
          <div className="glass-card p-6 hover-lift">
            <div className="flex items-center">
              <div className="p-3 bg-gradient-primary rounded-xl">
                <Target className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <div className="text-2xl font-bold text-gray-900">{student.progress.masteryPercentage}%</div>
                <div className="text-sm text-gray-600">Mastery Level</div>
              </div>
            </div>
          </div>
          
          <div className="glass-card p-6 hover-lift">
            <div className="flex items-center">
              <div className="p-3 bg-gradient-success rounded-xl">
                <TrendingUp className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <div className="text-2xl font-bold text-gray-900">{student.progress.averageScore}%</div>
                <div className="text-sm text-gray-600">Average Score</div>
              </div>
            </div>
          </div>
          
          <div className="glass-card p-6 hover-lift">
            <div className="flex items-center">
              <div className="p-3 bg-gradient-secondary rounded-xl">
                <Calendar className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <div className="text-2xl font-bold text-gray-900">{student.progress.studyStreak}</div>
                <div className="text-sm text-gray-600">Day Streak</div>
              </div>
            </div>
          </div>
          
          <div className="glass-card p-6 hover-lift">
            <div className="flex items-center">
              <div className="p-3 bg-gradient-warning rounded-xl">
                <Clock className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <div className="text-2xl font-bold text-gray-900">
                  {Math.ceil((new Date(student.examDate) - new Date()) / (1000 * 60 * 60 * 24))}
                </div>
                <div className="text-sm text-gray-600">Days to Exam</div>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column */}
          <div className="lg:col-span-2 space-y-8">
            {/* Today's Tasks */}
            <div className="glass-card p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-gray-900">Today's Tasks</h2>
                <button
                  onClick={() => navigate('/student/learning-path')}
                  className="glass-button bg-gradient-primary text-white text-sm"
                >
                  View All
                </button>
              </div>
              
              <div className="space-y-4">
                {student.todaysTasks.map((task) => (
                  <div key={task.id} className="glass-card p-4 hover-lift">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4">
                        <button
                          onClick={() => handleTaskComplete(task.id)}
                          className={`p-2 rounded-full ${task.completed ? 'bg-green-500' : 'bg-gray-300'}`}
                        >
                          {task.completed ? 
                            <CheckCircle className="h-4 w-4 text-white" /> : 
                            <Circle className="h-4 w-4 text-gray-500" />
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
                          <div className={`font-medium ${task.completed ? 'text-gray-500 line-through' : 'text-gray-900'}`}>
                            {task.title}
                          </div>
                          <div className="text-sm text-gray-500">{task.duration} min • {task.priority} priority</div>
                        </div>
                      </div>
                      
                      {!task.completed && (
                        <button className="glass-button bg-gradient-primary text-white text-sm">
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
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Weekly Progress</h2>
              <div className="grid grid-cols-5 gap-4">
                {student.weeklyPlan.map((day, index) => (
                  <div key={index} className="text-center">
                    <div className="glass-card p-4 hover-lift">
                      <div className="font-medium text-gray-900 mb-2">{day.day}</div>
                      <div className="text-2xl font-bold text-gray-900 mb-1">{day.completed}/{day.tasks}</div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-gradient-primary h-2 rounded-full transition-all duration-500" 
                          style={{ width: `${day.progress}%` }}
                        ></div>
                      </div>
                      <div className="text-xs text-gray-500 mt-1">{day.progress}%</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Progress Graphs */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Mastery Progress */}
              <div className="glass-card p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Subject Mastery</h3>
                <div className="space-y-4">
                  {student.masteryData.map((subject, index) => (
                    <div key={index}>
                      <div className="flex justify-between text-sm mb-1">
                        <span className="font-medium text-gray-700">{subject.subject}</span>
                        <span className="text-gray-500">{subject.mastery}%</span>
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
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Study Consistency</h3>
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
            <div className="glass-card p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
              <div className="space-y-3">
                <button 
                  onClick={() => navigate('/student/learning-path')}
                  className="w-full glass-button bg-gradient-primary text-white hover-lift"
                >
                  <BookOpen className="h-4 w-4 mr-2" />
                  My Learning Path
                </button>
                <button 
                  onClick={() => navigate('/student/upload')}
                  className="w-full glass-button bg-gradient-secondary text-white hover-lift"
                >
                  <Upload className="h-4 w-4 mr-2" />
                  Upload Goals
                </button>
                <button className="w-full glass-button bg-gradient-success text-white hover-lift">
                  <BarChart3 className="h-4 w-4 mr-2" />
                  View Analytics
                </button>
              </div>
            </div>

            {/* Quizzes */}
            <div className="glass-card p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Available Quizzes</h3>
              <div className="space-y-3">
                {student.quizzes.map((quiz) => (
                  <div key={quiz.id} className="glass-card p-4">
                    <div className="flex items-center justify-between mb-2">
                      <div className="font-medium text-gray-900">{quiz.title}</div>
                      {quiz.score && (
                        <div className="text-sm font-semibold text-green-600">{quiz.score}%</div>
                      )}
                    </div>
                    
                    <button
                      onClick={() => handleQuizAction(quiz)}
                      className={`w-full text-sm glass-button ${
                        quiz.status === 'completed' ? 'bg-gradient-success text-white' :
                        quiz.status === 'in-progress' ? 'bg-gradient-warning text-white' :
                        'bg-gradient-primary text-white'
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

            {/* AI Recommendations */}
            <div className="glass-card p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <Brain className="h-5 w-5 mr-2 text-purple-600" />
                AI Recommendations
              </h3>
              <div className="space-y-4">
                {student.aiRecommendations.map((rec) => (
                  <div key={rec.id} className={`glass-card p-4 border-l-4 ${
                    rec.priority === 'high' ? 'border-red-500' :
                    rec.priority === 'medium' ? 'border-yellow-500' : 'border-green-500'
                  }`}>
                    <div className="flex items-start justify-between mb-2">
                      <div className="font-medium text-gray-900 text-sm">{rec.title}</div>
                      <div className={`px-2 py-1 rounded-full text-xs ${
                        rec.priority === 'high' ? 'bg-red-100 text-red-800' :
                        rec.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800'
                      }`}>
                        {rec.priority}
                      </div>
                    </div>
                    <p className="text-gray-600 text-sm mb-3">{rec.description}</p>
                    <button
                      onClick={() => handleRecommendationAction(rec)}
                      className="w-full glass-button bg-gradient-primary text-white text-sm"
                    >
                      {rec.action}
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StudentDashboard;