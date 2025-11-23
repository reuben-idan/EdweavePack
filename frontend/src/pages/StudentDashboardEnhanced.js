import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { 
  BookOpen, Target, Calendar, TrendingUp, Clock, Award, User, Settings, 
  Upload, Play, CheckCircle, Circle, Brain, BarChart3, Star, Trophy,
  Zap, Flame, ChevronRight, Plus, Download, Share2, Bell, Search,
  Filter, RefreshCw, ArrowUp, ArrowDown, Bookmark, Heart, MessageCircle
} from 'lucide-react';
import { useStudentAuth } from '../hooks/useStudentAuth';
import { studentsAPI, analyticsAPI, assessmentAPI } from '../services/api';

const StudentDashboardEnhanced = () => {
  const navigate = useNavigate();
  const { student, logout } = useStudentAuth();
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [activeTab, setActiveTab] = useState('overview');
  const [notifications, setNotifications] = useState([]);
  const [showNotifications, setShowNotifications] = useState(false);

  useEffect(() => {
    if (student) {
      fetchDashboardData();
      fetchNotifications();
    }
  }, [student]);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Fetch comprehensive student data
      const [progressData, analyticsData, quizzesData] = await Promise.all([
        studentsAPI.getProgress(student.id).catch(() => ({ data: null })),
        analyticsAPI.getStudentProgress(student.id).catch(() => ({ data: null })),
        assessmentAPI.getStudentQuizzes().catch(() => ({ data: [] }))
      ]);

      // Comprehensive mock data with real structure
      const mockDashboard = {
        student: {
          ...student,
          streak: 12,
          level: 'Intermediate',
          xp: 2450,
          nextLevelXp: 3000,
          badges: ['Fast Learner', 'Quiz Master', 'Consistent Student'],
          achievements: [
            { id: 1, title: '7-Day Streak', icon: Flame, earned: true, date: '2024-01-15' },
            { id: 2, title: 'Perfect Score', icon: Star, earned: true, date: '2024-01-10' },
            { id: 3, title: 'Early Bird', icon: Zap, earned: false, progress: 60 },
            { id: 4, title: 'Quiz Champion', icon: Trophy, earned: false, progress: 80 }
          ]
        },
        progress: {
          overallProgress: 68,
          weeklyGoal: 85,
          dailyGoal: 75,
          completedLessons: 34,
          totalLessons: 50,
          averageScore: 87,
          studyTime: 145, // minutes today
          weeklyStudyTime: 720, // minutes this week
          masteryLevel: 72,
          improvementRate: 15 // percentage improvement this month
        },
        todaysTasks: [
          {
            id: 1,
            type: 'lesson',
            title: 'Advanced Algebra: Quadratic Functions',
            subject: 'Mathematics',
            duration: 45,
            difficulty: 'Medium',
            completed: false,
            priority: 'high',
            dueTime: '14:00',
            xpReward: 50,
            description: 'Learn to solve and graph quadratic equations'
          },
          {
            id: 2,
            type: 'practice',
            title: 'Physics Problem Set: Motion',
            subject: 'Physics',
            duration: 30,
            difficulty: 'Hard',
            completed: true,
            priority: 'medium',
            dueTime: '10:00',
            xpReward: 75,
            score: 92
          },
          {
            id: 3,
            type: 'quiz',
            title: 'Chemistry Quick Quiz',
            subject: 'Chemistry',
            duration: 15,
            difficulty: 'Easy',
            completed: false,
            priority: 'high',
            dueTime: '16:30',
            xpReward: 30,
            questions: 10
          },
          {
            id: 4,
            type: 'reading',
            title: 'Biology Chapter: Cell Structure',
            subject: 'Biology',
            duration: 25,
            difficulty: 'Medium',
            completed: false,
            priority: 'low',
            dueTime: '18:00',
            xpReward: 25,
            pages: 12
          }
        ],
        weeklyPlan: [
          { day: 'Mon', date: '15', tasks: 5, completed: 5, progress: 100, studyTime: 120 },
          { day: 'Tue', date: '16', tasks: 4, completed: 3, progress: 75, studyTime: 95 },
          { day: 'Wed', date: '17', tasks: 6, completed: 2, progress: 33, studyTime: 60 },
          { day: 'Thu', date: '18', tasks: 4, completed: 0, progress: 0, studyTime: 0 },
          { day: 'Fri', date: '19', tasks: 5, completed: 0, progress: 0, studyTime: 0 },
          { day: 'Sat', date: '20', tasks: 3, completed: 0, progress: 0, studyTime: 0 },
          { day: 'Sun', date: '21', tasks: 2, completed: 0, progress: 0, studyTime: 0 }
        ],
        subjects: [
          { 
            name: 'Mathematics', 
            progress: 85, 
            grade: 'A', 
            color: '#3B82F6',
            nextTopic: 'Calculus Basics',
            recentScore: 94,
            trend: 'up',
            lessons: 12,
            completedLessons: 10
          },
          { 
            name: 'Physics', 
            progress: 72, 
            grade: 'B+', 
            color: '#10B981',
            nextTopic: 'Thermodynamics',
            recentScore: 88,
            trend: 'up',
            lessons: 10,
            completedLessons: 7
          },
          { 
            name: 'Chemistry', 
            progress: 68, 
            grade: 'B', 
            color: '#F59E0B',
            nextTopic: 'Organic Chemistry',
            recentScore: 76,
            trend: 'stable',
            lessons: 8,
            completedLessons: 5
          },
          { 
            name: 'Biology', 
            progress: 45, 
            grade: 'C+', 
            color: '#EF4444',
            nextTopic: 'Genetics',
            recentScore: 65,
            trend: 'down',
            lessons: 9,
            completedLessons: 4
          }
        ],
        upcomingQuizzes: [
          {
            id: 1,
            title: 'Algebra Final Assessment',
            subject: 'Mathematics',
            date: '2024-01-25',
            time: '10:00 AM',
            duration: 90,
            questions: 25,
            difficulty: 'Hard',
            status: 'scheduled',
            preparationTime: 5 // days
          },
          {
            id: 2,
            title: 'Physics Midterm',
            subject: 'Physics',
            date: '2024-01-28',
            time: '2:00 PM',
            duration: 60,
            questions: 20,
            difficulty: 'Medium',
            status: 'available',
            preparationTime: 8
          }
        ],
        recentActivity: [
          {
            id: 1,
            type: 'quiz_completed',
            title: 'Completed Chemistry Quiz',
            score: 88,
            time: '2 hours ago',
            xpGained: 45
          },
          {
            id: 2,
            type: 'lesson_completed',
            title: 'Finished Physics Lesson',
            time: '5 hours ago',
            xpGained: 30
          },
          {
            id: 3,
            type: 'achievement_unlocked',
            title: 'Earned "Consistent Learner" Badge',
            time: '1 day ago',
            xpGained: 100
          }
        ],
        aiRecommendations: [
          {
            id: 1,
            type: 'focus',
            priority: 'high',
            title: 'Strengthen Biology Fundamentals',
            description: 'Your biology scores are below target. Focus on cell structure and basic concepts.',
            action: 'Start Biology Review',
            estimatedTime: 30,
            xpReward: 50
          },
          {
            id: 2,
            type: 'practice',
            priority: 'medium',
            title: 'Maintain Math Excellence',
            description: 'Great progress in mathematics! Continue with advanced topics to stay ahead.',
            action: 'Continue Advanced Math',
            estimatedTime: 45,
            xpReward: 75
          },
          {
            id: 3,
            type: 'schedule',
            priority: 'medium',
            title: 'Optimize Study Schedule',
            description: 'Consider studying chemistry in the morning when you\'re most focused.',
            action: 'Adjust Schedule',
            estimatedTime: 5,
            xpReward: 20
          }
        ],
        studyStreak: {
          current: 12,
          longest: 18,
          goal: 30,
          streakData: [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] // last 14 days
        }
      };

      setDashboardData(mockDashboard);
      
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const fetchNotifications = async () => {
    // Mock notifications
    const mockNotifications = [
      {
        id: 1,
        type: 'quiz_reminder',
        title: 'Quiz Reminder',
        message: 'Algebra Final Assessment is due in 3 days',
        time: '10 minutes ago',
        read: false,
        priority: 'high'
      },
      {
        id: 2,
        type: 'achievement',
        title: 'New Achievement!',
        message: 'You earned the "Fast Learner" badge',
        time: '2 hours ago',
        read: false,
        priority: 'medium'
      },
      {
        id: 3,
        type: 'study_reminder',
        title: 'Study Time',
        message: 'Time for your daily chemistry review',
        time: '1 day ago',
        read: true,
        priority: 'low'
      }
    ];
    
    setNotifications(mockNotifications);
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await fetchDashboardData();
    setRefreshing(false);
    toast.success('Dashboard refreshed!');
  };

  const handleTaskComplete = async (taskId) => {
    try {
      setDashboardData(prev => ({
        ...prev,
        todaysTasks: prev.todaysTasks.map(task =>
          task.id === taskId ? { ...task, completed: !task.completed } : task
        )
      }));
      
      const task = dashboardData.todaysTasks.find(t => t.id === taskId);
      if (!task.completed) {
        toast.success(`Great job! You earned ${task.xpReward} XP!`);
      }
    } catch (error) {
      toast.error('Failed to update task');
    }
  };

  const handleStartTask = (task) => {
    toast.info(`Starting ${task.title}...`);
    if (task.type === 'quiz') {
      navigate(`/student/quiz/${task.id}`);
    } else if (task.type === 'lesson') {
      navigate('/student/learning-path');
    } else {
      navigate('/student/learning-path');
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/student/login');
  };

  const getTaskIcon = (type) => {
    switch (type) {
      case 'lesson': return BookOpen;
      case 'practice': return Target;
      case 'quiz': return Brain;
      case 'reading': return BookOpen;
      default: return Circle;
    }
  };

  const getTaskColor = (type) => {
    switch (type) {
      case 'lesson': return 'bg-blue-500';
      case 'practice': return 'bg-green-500';
      case 'quiz': return 'bg-purple-500';
      case 'reading': return 'bg-orange-500';
      default: return 'bg-gray-500';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return 'border-red-500 bg-red-50';
      case 'medium': return 'border-yellow-500 bg-yellow-50';
      case 'low': return 'border-green-500 bg-green-50';
      default: return 'border-gray-300 bg-gray-50';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen animated-gradient flex items-center justify-center">
        <div className="glass-card p-8 text-center">
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-white font-medium">Loading your personalized dashboard...</p>
        </div>
      </div>
    );
  }

  if (!dashboardData) {
    return (
      <div className="min-h-screen animated-gradient flex items-center justify-center">
        <div className="glass-card p-8 text-center">
          <p className="text-white font-medium">Failed to load dashboard data</p>
          <button 
            onClick={fetchDashboardData}
            className="mt-4 premium-button"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen animated-gradient">
      {/* Enhanced Header */}
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
                <p className="text-white/80 text-sm">
                  Welcome back, {dashboardData.student.name} • Level {dashboardData.student.level}
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              {/* XP Display */}
              <div className="glass-card px-4 py-2 flex items-center space-x-2">
                <Star className="h-5 w-5 text-yellow-400" />
                <span className="text-white font-medium">
                  {dashboardData.student.xp} XP
                </span>
              </div>
              
              {/* Notifications */}
              <div className="relative">
                <button
                  onClick={() => setShowNotifications(!showNotifications)}
                  className="glass-button p-3 text-white hover-lift relative"
                >
                  <Bell className="h-5 w-5" />
                  {notifications.filter(n => !n.read).length > 0 && (
                    <div className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full"></div>
                  )}
                </button>
                
                {showNotifications && (
                  <div className="absolute right-0 top-12 w-80 glass-card p-4 max-h-96 overflow-y-auto">
                    <h3 className="font-semibold text-white mb-3">Notifications</h3>
                    <div className="space-y-3">
                      {notifications.map(notification => (
                        <div key={notification.id} className={`p-3 rounded-lg ${notification.read ? 'bg-white/5' : 'bg-blue-500/20'}`}>
                          <div className="flex justify-between items-start">
                            <div>
                              <p className="font-medium text-white text-sm">{notification.title}</p>
                              <p className="text-blue-100 text-xs">{notification.message}</p>
                            </div>
                            <span className="text-xs text-blue-200">{notification.time}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
              
              {/* Refresh Button */}
              <button
                onClick={handleRefresh}
                disabled={refreshing}
                className="glass-button p-3 text-white hover-lift"
              >
                <RefreshCw className={`h-5 w-5 ${refreshing ? 'animate-spin' : ''}`} />
              </button>
              
              {/* Profile Menu */}
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
        {/* Progress Overview Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="glass-card p-6 hover-lift">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">{dashboardData.progress.overallProgress}%</div>
                <div className="text-sm text-blue-200">Overall Progress</div>
                <div className="flex items-center mt-2">
                  <ArrowUp className="h-4 w-4 text-green-400 mr-1" />
                  <span className="text-xs text-green-400">+{dashboardData.progress.improvementRate}% this month</span>
                </div>
              </div>
              <div className="p-3 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl">
                <Target className="h-6 w-6 text-white" />
              </div>
            </div>
          </div>
          
          <div className="glass-card p-6 hover-lift">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">{dashboardData.progress.averageScore}%</div>
                <div className="text-sm text-blue-200">Average Score</div>
                <div className="text-xs text-blue-300 mt-2">Last 10 assessments</div>
              </div>
              <div className="p-3 bg-gradient-to-br from-green-500 to-teal-600 rounded-xl">
                <TrendingUp className="h-6 w-6 text-white" />
              </div>
            </div>
          </div>
          
          <div className="glass-card p-6 hover-lift">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white flex items-center">
                  {dashboardData.studyStreak.current}
                  <Flame className="h-5 w-5 text-orange-400 ml-1" />
                </div>
                <div className="text-sm text-blue-200">Study Streak</div>
                <div className="text-xs text-blue-300 mt-2">Goal: {dashboardData.studyStreak.goal} days</div>
              </div>
              <div className="p-3 bg-gradient-to-br from-orange-500 to-red-600 rounded-xl">
                <Calendar className="h-6 w-6 text-white" />
              </div>
            </div>
          </div>
          
          <div className="glass-card p-6 hover-lift">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">{Math.floor(dashboardData.progress.studyTime / 60)}h {dashboardData.progress.studyTime % 60}m</div>
                <div className="text-sm text-blue-200">Today's Study Time</div>
                <div className="text-xs text-blue-300 mt-2">Weekly: {Math.floor(dashboardData.progress.weeklyStudyTime / 60)}h</div>
              </div>
              <div className="p-3 bg-gradient-to-br from-purple-500 to-pink-600 rounded-xl">
                <Clock className="h-6 w-6 text-white" />
              </div>
            </div>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Tasks and Progress */}
          <div className="lg:col-span-2 space-y-8">
            {/* Today's Tasks */}
            <div className="glass-card p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-white flex items-center">
                  <CheckCircle className="h-6 w-6 mr-2 text-green-400" />
                  Today's Learning Tasks
                </h2>
                <div className="flex items-center space-x-2">
                  <span className="text-sm text-blue-200">
                    {dashboardData.todaysTasks.filter(t => t.completed).length}/{dashboardData.todaysTasks.length} completed
                  </span>
                  <button
                    onClick={() => navigate('/student/learning-path')}
                    className="glass-button bg-gradient-primary text-white text-sm"
                  >
                    View All
                  </button>
                </div>
              </div>
              
              <div className="space-y-4">
                {dashboardData.todaysTasks.map((task) => {
                  const TaskIcon = getTaskIcon(task.type);
                  return (
                    <div key={task.id} className={`glass-card p-4 hover-lift border-l-4 ${getPriorityColor(task.priority)}`}>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4 flex-1">
                          <button
                            onClick={() => handleTaskComplete(task.id)}
                            className={`p-2 rounded-full transition-all ${task.completed ? 'bg-green-500' : 'bg-gray-300 hover:bg-gray-400'}`}
                          >
                            {task.completed ? 
                              <CheckCircle className="h-4 w-4 text-white" /> : 
                              <Circle className="h-4 w-4 text-gray-600" />
                            }
                          </button>
                          
                          <div className={`p-3 rounded-lg ${getTaskColor(task.type)}`}>
                            <TaskIcon className="h-5 w-5 text-white" />
                          </div>
                          
                          <div className="flex-1">
                            <div className={`font-medium ${task.completed ? 'text-gray-500 line-through' : 'text-gray-900'}`}>
                              {task.title}
                            </div>
                            <div className="text-sm text-gray-600 flex items-center space-x-4">
                              <span>{task.subject}</span>
                              <span>•</span>
                              <span>{task.duration} min</span>
                              <span>•</span>
                              <span className="capitalize">{task.difficulty}</span>
                              <span>•</span>
                              <span className="flex items-center">
                                <Star className="h-3 w-3 text-yellow-500 mr-1" />
                                {task.xpReward} XP
                              </span>
                            </div>
                            {task.description && (
                              <div className="text-xs text-gray-500 mt-1">{task.description}</div>
                            )}
                          </div>
                        </div>
                        
                        <div className="flex items-center space-x-2">
                          {task.dueTime && (
                            <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
                              Due: {task.dueTime}
                            </span>
                          )}
                          {!task.completed && (
                            <button 
                              onClick={() => handleStartTask(task)}
                              className="glass-button bg-gradient-primary text-white text-sm px-4 py-2"
                            >
                              <Play className="h-3 w-3 mr-1" />
                              Start
                            </button>
                          )}
                          {task.completed && task.score && (
                            <span className="text-sm font-semibold text-green-600 bg-green-100 px-2 py-1 rounded">
                              {task.score}%
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Subject Progress */}
            <div className="glass-card p-6">
              <h2 className="text-xl font-semibold text-white mb-6 flex items-center">
                <BookOpen className="h-6 w-6 mr-2 text-blue-400" />
                Subject Progress
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {dashboardData.subjects.map((subject, index) => (
                  <div key={index} className="glass-card p-4 hover-lift">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center space-x-3">
                        <div 
                          className="w-4 h-4 rounded-full"
                          style={{ backgroundColor: subject.color }}
                        ></div>
                        <span className="font-medium text-gray-900">{subject.name}</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className="text-lg font-bold text-gray-900">{subject.grade}</span>
                        {subject.trend === 'up' && <ArrowUp className="h-4 w-4 text-green-500" />}
                        {subject.trend === 'down' && <ArrowDown className="h-4 w-4 text-red-500" />}
                      </div>
                    </div>
                    
                    <div className="mb-3">
                      <div className="flex justify-between text-sm mb-1">
                        <span className="text-gray-600">Progress</span>
                        <span className="text-gray-900 font-medium">{subject.progress}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="h-2 rounded-full transition-all duration-500"
                          style={{ 
                            width: `${subject.progress}%`,
                            backgroundColor: subject.color
                          }}
                        ></div>
                      </div>
                    </div>
                    
                    <div className="text-sm text-gray-600 space-y-1">
                      <div className="flex justify-between">
                        <span>Lessons:</span>
                        <span>{subject.completedLessons}/{subject.lessons}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Recent Score:</span>
                        <span className="font-medium">{subject.recentScore}%</span>
                      </div>
                      <div className="text-xs text-blue-600 mt-2">
                        Next: {subject.nextTopic}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right Column - Sidebar */}
          <div className="space-y-6">
            {/* Level Progress */}
            <div className="glass-card p-6">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
                <Trophy className="h-5 w-5 mr-2 text-yellow-400" />
                Level Progress
              </h3>
              <div className="text-center mb-4">
                <div className="text-3xl font-bold text-white mb-1">
                  {dashboardData.student.level}
                </div>
                <div className="text-sm text-blue-200">
                  {dashboardData.student.xp} / {dashboardData.student.nextLevelXp} XP
                </div>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3 mb-4">
                <div 
                  className="bg-gradient-to-r from-yellow-400 to-orange-500 h-3 rounded-full transition-all duration-500"
                  style={{ 
                    width: `${(dashboardData.student.xp / dashboardData.student.nextLevelXp) * 100}%`
                  }}
                ></div>
              </div>
              <div className="text-xs text-blue-200 text-center">
                {dashboardData.student.nextLevelXp - dashboardData.student.xp} XP to next level
              </div>
            </div>

            {/* Quick Actions */}
            <div className="glass-card p-6">
              <h3 className="text-lg font-semibold text-white mb-4">Quick Actions</h3>
              <div className="space-y-3">
                <button 
                  onClick={() => navigate('/student/learning-path')}
                  className="w-full glass-button bg-gradient-primary text-white hover-lift"
                >
                  <BookOpen className="h-4 w-4 mr-2" />
                  Continue Learning
                </button>
                <button 
                  onClick={() => navigate('/student/upload')}
                  className="w-full glass-button bg-gradient-secondary text-white hover-lift"
                >
                  <Upload className="h-4 w-4 mr-2" />
                  Upload Study Material
                </button>
                <button 
                  onClick={() => navigate('/student/progress')}
                  className="w-full glass-button bg-gradient-success text-white hover-lift"
                >
                  <BarChart3 className="h-4 w-4 mr-2" />
                  View Detailed Progress
                </button>
              </div>
            </div>

            {/* Upcoming Quizzes */}
            <div className="glass-card p-6">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
                <Brain className="h-5 w-5 mr-2 text-purple-400" />
                Upcoming Quizzes
              </h3>
              <div className="space-y-3">
                {dashboardData.upcomingQuizzes.map((quiz) => (
                  <div key={quiz.id} className="glass-card p-4">
                    <div className="flex items-center justify-between mb-2">
                      <div className="font-medium text-gray-900 text-sm">{quiz.title}</div>
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        quiz.difficulty === 'Hard' ? 'bg-red-100 text-red-800' :
                        quiz.difficulty === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-green-100 text-green-800'
                      }`}>
                        {quiz.difficulty}
                      </span>
                    </div>
                    <div className="text-xs text-gray-600 space-y-1">
                      <div>{quiz.subject}</div>
                      <div>{quiz.date} at {quiz.time}</div>
                      <div>{quiz.questions} questions • {quiz.duration} min</div>
                      <div className="text-blue-600">
                        {quiz.preparationTime} days to prepare
                      </div>
                    </div>
                    <button className="w-full mt-3 glass-button bg-gradient-primary text-white text-sm">
                      {quiz.status === 'available' ? 'Start Quiz' : 'Prepare'}
                    </button>
                  </div>
                ))}
              </div>
            </div>

            {/* AI Recommendations */}
            <div className="glass-card p-6">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
                <Brain className="h-5 w-5 mr-2 text-purple-400" />
                AI Recommendations
              </h3>
              <div className="space-y-4">
                {dashboardData.aiRecommendations.map((rec) => (
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
                    <p className="text-gray-600 text-xs mb-3">{rec.description}</p>
                    <div className="flex items-center justify-between">
                      <div className="text-xs text-gray-500">
                        {rec.estimatedTime} min • {rec.xpReward} XP
                      </div>
                      <button className="glass-button bg-gradient-primary text-white text-xs px-3 py-1">
                        {rec.action}
                      </button>
                    </div>
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

export default StudentDashboardEnhanced;