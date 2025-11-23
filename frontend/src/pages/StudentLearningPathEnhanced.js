import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { 
  ArrowLeft, BookOpen, Play, CheckCircle, Clock, Star, Target,
  Brain, Award, ChevronRight, Lock, Unlock, BarChart3, Calendar,
  Download, Share2, Bookmark, Heart, MessageCircle, Filter,
  Search, RefreshCw, Plus, Edit, Settings, Trophy, Zap, Flame
} from 'lucide-react';
import { useStudentAuth } from '../hooks/useStudentAuth';

const StudentLearningPathEnhanced = () => {
  const navigate = useNavigate();
  const { student } = useStudentAuth();
  const [learningPath, setLearningPath] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeWeek, setActiveWeek] = useState(1);
  const [filterType, setFilterType] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchLearningPath();
  }, []);

  const fetchLearningPath = async () => {
    try {
      setLoading(true);
      
      // Mock comprehensive learning path data
      const mockLearningPath = {
        id: 1,
        title: 'Advanced Mathematics Mastery Path',
        description: 'Comprehensive 12-week journey through advanced mathematical concepts',
        totalWeeks: 12,
        currentWeek: 3,
        overallProgress: 68,
        estimatedCompletion: '2024-04-15',
        difficulty: 'Advanced',
        subject: 'Mathematics',
        learningStyle: 'Visual',
        
        weeks: [
          {
            weekNumber: 1,
            title: 'Algebraic Foundations',
            status: 'completed',
            progress: 100,
            unlocked: true,
            startDate: '2024-01-01',
            endDate: '2024-01-07',
            estimatedHours: 8,
            actualHours: 9,
            bloomLevel: 'Remember & Understand',
            
            lessons: [
              {
                id: 1,
                title: 'Linear Equations Review',
                type: 'lesson',
                duration: 45,
                status: 'completed',
                score: 95,
                xpEarned: 50,
                bloomLevel: 'Remember',
                difficulty: 'Easy'
              },
              {
                id: 2,
                title: 'Quadratic Functions',
                type: 'lesson',
                duration: 60,
                status: 'completed',
                score: 88,
                xpEarned: 75,
                bloomLevel: 'Understand',
                difficulty: 'Medium'
              },
              {
                id: 3,
                title: 'Practice Problems Set A',
                type: 'practice',
                duration: 30,
                status: 'completed',
                score: 92,
                xpEarned: 40,
                bloomLevel: 'Apply',
                difficulty: 'Medium'
              }
            ]
          },
          {
            weekNumber: 2,
            title: 'Advanced Algebra',
            status: 'completed',
            progress: 100,
            unlocked: true,
            startDate: '2024-01-08',
            endDate: '2024-01-14',
            estimatedHours: 10,
            actualHours: 8,
            bloomLevel: 'Apply & Analyze',
            
            lessons: [
              {
                id: 4,
                title: 'Polynomial Functions',
                type: 'lesson',
                duration: 50,
                status: 'completed',
                score: 91,
                xpEarned: 60,
                bloomLevel: 'Apply',
                difficulty: 'Medium'
              },
              {
                id: 5,
                title: 'Rational Functions',
                type: 'lesson',
                duration: 55,
                status: 'completed',
                score: 85,
                xpEarned: 65,
                bloomLevel: 'Analyze',
                difficulty: 'Hard'
              }
            ]
          },
          {
            weekNumber: 3,
            title: 'Calculus Introduction',
            status: 'in-progress',
            progress: 60,
            unlocked: true,
            startDate: '2024-01-15',
            endDate: '2024-01-21',
            estimatedHours: 12,
            actualHours: 7,
            bloomLevel: 'Analyze & Evaluate',
            
            lessons: [
              {
                id: 6,
                title: 'Limits and Continuity',
                type: 'lesson',
                duration: 60,
                status: 'completed',
                score: 89,
                xpEarned: 70,
                bloomLevel: 'Analyze',
                difficulty: 'Hard'
              },
              {
                id: 7,
                title: 'Derivatives Basics',
                type: 'lesson',
                duration: 65,
                status: 'in-progress',
                progress: 40,
                bloomLevel: 'Evaluate',
                difficulty: 'Hard'
              },
              {
                id: 8,
                title: 'Calculus Quiz',
                type: 'quiz',
                duration: 30,
                status: 'locked',
                bloomLevel: 'Evaluate',
                difficulty: 'Hard'
              }
            ]
          }
        ],
        
        achievements: [
          {
            id: 1,
            title: 'Week 1 Champion',
            description: 'Completed all Week 1 activities with 90%+ average',
            icon: Trophy,
            earned: true,
            earnedDate: '2024-01-07'
          },
          {
            id: 2,
            title: 'Speed Learner',
            description: 'Completed lessons faster than estimated time',
            icon: Zap,
            earned: true,
            earnedDate: '2024-01-10'
          },
          {
            id: 3,
            title: 'Calculus Explorer',
            description: 'Started advanced calculus topics',
            icon: Brain,
            earned: false,
            progress: 60
          }
        ],
        
        analytics: {
          totalLessons: 25,
          completedLessons: 15,
          averageScore: 89,
          totalXP: 850,
          studyTime: 24, // hours
          streakDays: 12,
          strongAreas: ['Linear Algebra', 'Quadratic Functions'],
          improvementAreas: ['Complex Numbers', 'Trigonometry']
        }
      };
      
      setLearningPath(mockLearningPath);
    } catch (error) {
      console.error('Error fetching learning path:', error);
      toast.error('Failed to load learning path');
    } finally {
      setLoading(false);
    }
  };

  const handleLessonStart = (lesson) => {
    if (lesson.status === 'locked') {
      toast.warning('Complete previous lessons to unlock this one');
      return;
    }
    
    toast.info(`Starting ${lesson.title}...`);
    if (lesson.type === 'quiz') {
      navigate(`/student/quiz/${lesson.id}`);
    } else {
      // Navigate to lesson content
      navigate(`/student/lesson/${lesson.id}`);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'text-green-600 bg-green-100';
      case 'in-progress': return 'text-blue-600 bg-blue-100';
      case 'locked': return 'text-gray-500 bg-gray-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed': return CheckCircle;
      case 'in-progress': return Play;
      case 'locked': return Lock;
      default: return Clock;
    }
  };

  const getLessonIcon = (type) => {
    switch (type) {
      case 'lesson': return BookOpen;
      case 'practice': return Target;
      case 'quiz': return Brain;
      default: return BookOpen;
    }
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'Easy': return 'text-green-600 bg-green-100';
      case 'Medium': return 'text-yellow-600 bg-yellow-100';
      case 'Hard': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen animated-gradient flex items-center justify-center">
        <div className="glass-card p-8 text-center">
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-white font-medium">Loading your personalized learning path...</p>
        </div>
      </div>
    );
  }

  if (!learningPath) {
    return (
      <div className="min-h-screen animated-gradient flex items-center justify-center">
        <div className="glass-card p-8 text-center">
          <BookOpen className="h-16 w-16 text-blue-300 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-white mb-2">No Learning Path Found</h3>
          <p className="text-blue-100 mb-6">Start by uploading your study goals to generate a personalized path.</p>
          <button
            onClick={() => navigate('/student/upload')}
            className="premium-button"
          >
            Upload Study Goals
          </button>
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
              <button
                onClick={() => navigate('/student/dashboard')}
                className="glass-button p-3 hover-lift"
              >
                <ArrowLeft className="h-5 w-5 text-white" />
              </button>
              <div>
                <h1 className="text-xl font-bold text-white">{learningPath.title}</h1>
                <p className="text-white/80 text-sm">
                  Week {learningPath.currentWeek} of {learningPath.totalWeeks} • {learningPath.overallProgress}% Complete
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="glass-card px-4 py-2 flex items-center space-x-2">
                <Star className="h-5 w-5 text-yellow-400" />
                <span className="text-white font-medium">{learningPath.analytics.totalXP} XP</span>
              </div>
              <button className="glass-button p-3 text-white hover-lift">
                <Settings className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">
        {/* Progress Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="glass-card p-6">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">{learningPath.overallProgress}%</div>
                <div className="text-sm text-blue-200">Overall Progress</div>
              </div>
              <Target className="h-8 w-8 text-blue-400" />
            </div>
            <div className="mt-4 w-full bg-white/20 rounded-full h-2">
              <div 
                className="bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full transition-all duration-500"
                style={{ width: `${learningPath.overallProgress}%` }}
              ></div>
            </div>
          </div>
          
          <div className="glass-card p-6">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">{learningPath.analytics.completedLessons}/{learningPath.analytics.totalLessons}</div>
                <div className="text-sm text-blue-200">Lessons Complete</div>
              </div>
              <BookOpen className="h-8 w-8 text-green-400" />
            </div>
          </div>
          
          <div className="glass-card p-6">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white">{learningPath.analytics.averageScore}%</div>
                <div className="text-sm text-blue-200">Average Score</div>
              </div>
              <BarChart3 className="h-8 w-8 text-yellow-400" />
            </div>
          </div>
          
          <div className="glass-card p-6">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-white flex items-center">
                  {learningPath.analytics.streakDays}
                  <Flame className="h-5 w-5 text-orange-400 ml-1" />
                </div>
                <div className="text-sm text-blue-200">Study Streak</div>
              </div>
              <Calendar className="h-8 w-8 text-orange-400" />
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Week Navigation Sidebar */}
          <div className="lg:col-span-1">
            <div className="glass-card p-6 sticky top-24">
              <h3 className="text-lg font-semibold text-white mb-4">Learning Weeks</h3>
              <div className="space-y-3">
                {learningPath.weeks.map((week) => {
                  const StatusIcon = getStatusIcon(week.status);
                  return (
                    <button
                      key={week.weekNumber}
                      onClick={() => setActiveWeek(week.weekNumber)}
                      className={`w-full text-left p-3 rounded-lg transition-all ${
                        activeWeek === week.weekNumber 
                          ? 'bg-blue-500/20 border border-blue-400' 
                          : 'bg-white/10 hover:bg-white/20'
                      } ${!week.unlocked ? 'opacity-50 cursor-not-allowed' : ''}`}
                      disabled={!week.unlocked}
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="font-medium text-white text-sm">Week {week.weekNumber}</div>
                          <div className="text-xs text-blue-200">{week.title}</div>
                        </div>
                        <div className="flex items-center space-x-2">
                          <StatusIcon className="h-4 w-4 text-white" />
                          <span className="text-xs text-white">{week.progress}%</span>
                        </div>
                      </div>
                      <div className="mt-2 w-full bg-white/20 rounded-full h-1">
                        <div 
                          className="bg-gradient-to-r from-blue-400 to-purple-500 h-1 rounded-full transition-all duration-300"
                          style={{ width: `${week.progress}%` }}
                        ></div>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Week Content */}
          <div className="lg:col-span-3">
            {learningPath.weeks
              .filter(week => week.weekNumber === activeWeek)
              .map(week => (
                <div key={week.weekNumber} className="space-y-6">
                  {/* Week Header */}
                  <div className="glass-card p-6">
                    <div className="flex items-center justify-between mb-4">
                      <div>
                        <h2 className="text-2xl font-bold text-white">Week {week.weekNumber}: {week.title}</h2>
                        <p className="text-blue-200">Bloom's Taxonomy Focus: {week.bloomLevel}</p>
                      </div>
                      <div className="flex items-center space-x-4">
                        <div className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(week.status)}`}>
                          {week.status.replace('-', ' ').toUpperCase()}
                        </div>
                        <div className="text-right">
                          <div className="text-2xl font-bold text-white">{week.progress}%</div>
                          <div className="text-sm text-blue-200">Complete</div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                      <div className="text-center">
                        <div className="text-lg font-semibold text-white">{week.estimatedHours}h</div>
                        <div className="text-sm text-blue-200">Estimated Time</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-semibold text-white">{week.actualHours || 0}h</div>
                        <div className="text-sm text-blue-200">Time Spent</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-semibold text-white">{week.lessons?.length || 0}</div>
                        <div className="text-sm text-blue-200">Activities</div>
                      </div>
                    </div>
                    
                    <div className="w-full bg-white/20 rounded-full h-3">
                      <div 
                        className="bg-gradient-to-r from-blue-500 to-purple-600 h-3 rounded-full transition-all duration-500"
                        style={{ width: `${week.progress}%` }}
                      ></div>
                    </div>
                  </div>

                  {/* Lessons */}
                  <div className="space-y-4">
                    {week.lessons?.map((lesson) => {
                      const LessonIcon = getLessonIcon(lesson.type);
                      const StatusIcon = getStatusIcon(lesson.status);
                      
                      return (
                        <div key={lesson.id} className="glass-card p-6 hover-lift">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-4 flex-1">
                              <div className={`p-3 rounded-lg ${
                                lesson.type === 'lesson' ? 'bg-blue-500' :
                                lesson.type === 'practice' ? 'bg-green-500' :
                                lesson.type === 'quiz' ? 'bg-purple-500' : 'bg-gray-500'
                              }`}>
                                <LessonIcon className="h-6 w-6 text-white" />
                              </div>
                              
                              <div className="flex-1">
                                <div className="flex items-center space-x-3 mb-2">
                                  <h3 className="font-semibold text-white">{lesson.title}</h3>
                                  <div className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(lesson.difficulty)}`}>
                                    {lesson.difficulty}
                                  </div>
                                  <div className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs">
                                    {lesson.bloomLevel}
                                  </div>
                                </div>
                                
                                <div className="flex items-center space-x-4 text-sm text-blue-200">
                                  <span className="flex items-center">
                                    <Clock className="h-4 w-4 mr-1" />
                                    {lesson.duration} min
                                  </span>
                                  {lesson.xpEarned && (
                                    <span className="flex items-center">
                                      <Star className="h-4 w-4 mr-1 text-yellow-400" />
                                      {lesson.xpEarned} XP
                                    </span>
                                  )}
                                  {lesson.score && (
                                    <span className="flex items-center text-green-400">
                                      <Trophy className="h-4 w-4 mr-1" />
                                      {lesson.score}%
                                    </span>
                                  )}
                                </div>
                                
                                {lesson.status === 'in-progress' && lesson.progress && (
                                  <div className="mt-2 w-full bg-white/20 rounded-full h-2">
                                    <div 
                                      className="bg-gradient-to-r from-blue-400 to-purple-500 h-2 rounded-full transition-all duration-300"
                                      style={{ width: `${lesson.progress}%` }}
                                    ></div>
                                  </div>
                                )}
                              </div>
                            </div>
                            
                            <div className="flex items-center space-x-3">
                              <div className={`p-2 rounded-full ${getStatusColor(lesson.status)}`}>
                                <StatusIcon className="h-5 w-5" />
                              </div>
                              
                              {lesson.status !== 'locked' && (
                                <button
                                  onClick={() => handleLessonStart(lesson)}
                                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                                    lesson.status === 'completed' 
                                      ? 'bg-green-500/20 text-green-400 hover:bg-green-500/30'
                                      : 'bg-blue-500/20 text-blue-400 hover:bg-blue-500/30'
                                  }`}
                                >
                                  {lesson.status === 'completed' ? 'Review' : 
                                   lesson.status === 'in-progress' ? 'Continue' : 'Start'}
                                </button>
                              )}
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))}
          </div>
        </div>

        {/* Achievements Section */}
        {learningPath.achievements && learningPath.achievements.length > 0 && (
          <div className="glass-card p-6">
            <h3 className="text-xl font-semibold text-white mb-6 flex items-center">
              <Award className="h-6 w-6 mr-2 text-yellow-400" />
              Achievements
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {learningPath.achievements.map((achievement) => {
                const AchievementIcon = achievement.icon;
                return (
                  <div key={achievement.id} className={`glass-card p-4 ${achievement.earned ? 'bg-yellow-500/10 border border-yellow-400' : 'bg-gray-500/10'}`}>
                    <div className="flex items-center space-x-3 mb-3">
                      <div className={`p-2 rounded-full ${achievement.earned ? 'bg-yellow-500' : 'bg-gray-500'}`}>
                        <AchievementIcon className="h-5 w-5 text-white" />
                      </div>
                      <div>
                        <div className={`font-medium ${achievement.earned ? 'text-yellow-400' : 'text-gray-400'}`}>
                          {achievement.title}
                        </div>
                        {achievement.earned && achievement.earnedDate && (
                          <div className="text-xs text-yellow-300">
                            Earned: {new Date(achievement.earnedDate).toLocaleDateString()}
                          </div>
                        )}
                      </div>
                    </div>
                    <p className="text-sm text-blue-200 mb-3">{achievement.description}</p>
                    {!achievement.earned && achievement.progress && (
                      <div className="w-full bg-gray-600 rounded-full h-2">
                        <div 
                          className="bg-gradient-to-r from-yellow-400 to-orange-500 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${achievement.progress}%` }}
                        ></div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default StudentLearningPathEnhanced;