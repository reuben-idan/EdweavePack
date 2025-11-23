import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { BookOpen, Target, Calendar, TrendingUp, Clock, Award, User, Settings, Upload } from 'lucide-react';

const StudentDashboard = () => {
  const navigate = useNavigate();
  const [student, setStudent] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStudentData();
  }, []);

  const fetchStudentData = async () => {
    try {
      // Mock student data
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
          studyStreak: 7
        },
        recentActivity: [
          { id: 1, type: 'lesson', title: 'Quadratic Equations', score: 92, date: '2024-01-20' },
          { id: 2, type: 'quiz', title: 'Physics Motion Quiz', score: 88, date: '2024-01-19' },
          { id: 3, type: 'lesson', title: 'Chemical Bonding', score: 95, date: '2024-01-18' }
        ],
        upcomingDeadlines: [
          { id: 1, title: 'Mathematics Assignment', date: '2024-01-25', type: 'assignment' },
          { id: 2, title: 'Physics Quiz', date: '2024-01-27', type: 'quiz' },
          { id: 3, title: 'WASSCE Mock Exam', date: '2024-02-01', type: 'exam' }
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

  const handleLogout = () => {
    toast.success('Logged out successfully');
    navigate('/student/login');
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
                <BookOpen className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <div className="text-2xl font-bold text-gray-900">
                  {student.progress.completedLessons}/{student.progress.totalLessons}
                </div>
                <div className="text-sm text-gray-600">Lessons Completed</div>
              </div>
            </div>
          </div>
          
          <div className="glass-card p-6 hover-lift">
            <div className="flex items-center">
              <div className="p-3 bg-gradient-success rounded-xl">
                <Target className="h-6 w-6 text-white" />
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
                <TrendingUp className="h-6 w-6 text-white" />
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
                <Calendar className="h-6 w-6 text-white" />
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

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Learning Progress */}
          <div className="lg:col-span-2 space-y-6">
            <div className="glass-card p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Learning Progress</h2>
              <div className="mb-4">
                <div className="flex justify-between text-sm text-gray-600 mb-2">
                  <span>Overall Progress</span>
                  <span>{Math.round((student.progress.completedLessons / student.progress.totalLessons) * 100)}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div 
                    className="bg-gradient-primary h-3 rounded-full transition-all duration-500" 
                    style={{ width: `${(student.progress.completedLessons / student.progress.totalLessons) * 100}%` }}
                  ></div>
                </div>
              </div>
              
              <div className="grid grid-cols-3 gap-4">
                <button className="glass-button bg-gradient-primary text-white hover-lift">
                  <BookOpen className="h-5 w-5 mr-2" />
                  Continue Learning
                </button>
                <button className="glass-button bg-gradient-success text-white hover-lift">
                  <Target className="h-5 w-5 mr-2" />
                  Practice Quiz
                </button>
                <button 
                  onClick={() => navigate('/student/upload')}
                  className="glass-button bg-gradient-secondary text-white hover-lift"
                >
                  <Upload className="h-5 w-5 mr-2" />
                  Upload Goals
                </button>
              </div>
            </div>

            {/* Recent Activity */}
            <div className="glass-card p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Activity</h2>
              <div className="space-y-4">
                {student.recentActivity.map(activity => (
                  <div key={activity.id} className="flex items-center justify-between p-4 glass-card hover-lift">
                    <div className="flex items-center space-x-3">
                      <div className={`p-2 rounded-lg ${activity.type === 'lesson' ? 'bg-blue-100' : 'bg-green-100'}`}>
                        {activity.type === 'lesson' ? 
                          <BookOpen className="h-4 w-4 text-blue-600" /> : 
                          <Target className="h-4 w-4 text-green-600" />
                        }
                      </div>
                      <div>
                        <div className="font-medium text-gray-900">{activity.title}</div>
                        <div className="text-sm text-gray-500">{new Date(activity.date).toLocaleDateString()}</div>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="font-semibold text-gray-900">{activity.score}%</div>
                      <div className="text-sm text-gray-500">Score</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Profile Summary */}
            <div className="glass-card p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Profile</h3>
              <div className="space-y-3">
                <div className="flex items-center space-x-3">
                  <User className="h-5 w-5 text-gray-400" />
                  <span className="text-sm text-gray-600">{student.name}, {student.age} years old</span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="w-5 h-5 bg-gradient-primary rounded-full"></div>
                  <span className="text-sm text-gray-600">Learning Style: {student.learningStyle}</span>
                </div>
                <div className="flex items-center space-x-3">
                  <Target className="h-5 w-5 text-gray-400" />
                  <span className="text-sm text-gray-600">Target: {student.targetExams.join(', ')}</span>
                </div>
              </div>
              <button
                onClick={() => navigate('/student/profile')}
                className="w-full mt-4 glass-button text-gray-700 hover:bg-white/50"
              >
                Edit Profile
              </button>
            </div>

            {/* Upcoming Deadlines */}
            <div className="glass-card p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Upcoming Deadlines</h3>
              <div className="space-y-3">
                {student.upcomingDeadlines.map(deadline => (
                  <div key={deadline.id} className="flex items-center justify-between p-3 glass-card">
                    <div>
                      <div className="font-medium text-gray-900 text-sm">{deadline.title}</div>
                      <div className="text-xs text-gray-500">{deadline.type}</div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-medium text-gray-900">
                        {new Date(deadline.date).toLocaleDateString()}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Study Goals */}
            <div className="glass-card p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Academic Goals</h3>
              <p className="text-sm text-gray-600 mb-4">{student.academicGoals}</p>
              <div className="flex items-center space-x-2 text-sm text-gray-500">
                <Calendar className="h-4 w-4" />
                <span>Target Date: {new Date(student.examDate).toLocaleDateString()}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StudentDashboard;