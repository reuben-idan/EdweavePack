import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { ArrowLeft, TrendingUp, Target, Calendar, Award, BarChart3, Clock } from 'lucide-react';

const ProgressPage = () => {
  const navigate = useNavigate();
  const [progressData, setProgressData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProgressData();
  }, []);

  const fetchProgressData = async () => {
    try {
      // Mock comprehensive progress data
      const mockData = {
        topicMastery: [
          { subject: 'Algebra', mastery: 85, totalTopics: 12, masteredTopics: 10 },
          { subject: 'Geometry', mastery: 72, totalTopics: 8, masteredTopics: 6 },
          { subject: 'Physics', mastery: 68, totalTopics: 10, masteredTopics: 7 },
          { subject: 'Chemistry', mastery: 45, totalTopics: 15, masteredTopics: 7 }
        ],
        quizHistory: [
          { date: '2024-01-20', score: 92, subject: 'Algebra', type: 'Daily Quiz' },
          { date: '2024-01-19', score: 78, subject: 'Physics', type: 'Weekly Test' },
          { date: '2024-01-18', score: 85, subject: 'Geometry', type: 'Practice Quiz' },
          { date: '2024-01-17', score: 90, subject: 'Algebra', type: 'Daily Quiz' },
          { date: '2024-01-16', score: 65, subject: 'Chemistry', type: 'Weekly Test' },
          { date: '2024-01-15', score: 88, subject: 'Physics', type: 'Daily Quiz' }
        ],
        dailyStreaks: {
          current: 7,
          longest: 12,
          thisWeek: 5,
          thisMonth: 18
        },
        consistencyHeatmap: [
          [3, 2, 4, 1, 3, 2, 1], // Week 1
          [4, 3, 2, 4, 2, 1, 3], // Week 2
          [2, 4, 3, 1, 4, 3, 2], // Week 3
          [1, 3, 4, 2, 1, 4, 3], // Week 4
          [3, 4, 2, 3, 4, 1, 2]  // Week 5
        ],
        weeklyProgress: [
          { week: 'Week 1', completed: 85, target: 80 },
          { week: 'Week 2', completed: 92, target: 85 },
          { week: 'Week 3', completed: 78, target: 85 },
          { week: 'Week 4', completed: 88, target: 90 }
        ],
        achievements: [
          { title: '7-Day Streak', description: 'Studied for 7 consecutive days', earned: true },
          { title: 'Quiz Master', description: 'Scored 90+ on 5 quizzes', earned: true },
          { title: 'Algebra Expert', description: 'Mastered 80% of algebra topics', earned: true },
          { title: 'Perfect Week', description: 'Complete all tasks in a week', earned: false }
        ]
      };
      
      setProgressData(mockData);
      toast.success('Progress data loaded successfully');
    } catch (error) {
      toast.error('Failed to load progress data');
    } finally {
      setLoading(false);
    }
  };

  const getHeatmapColor = (value) => {
    const colors = ['#f3f4f6', '#dbeafe', '#93c5fd', '#3b82f6', '#1d4ed8'];
    return colors[Math.min(value, 4)];
  };

  const getMasteryColor = (mastery) => {
    if (mastery >= 80) return 'text-green-600';
    if (mastery >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  if (loading) {
    return (
      <div className="min-h-screen animated-gradient flex items-center justify-center">
        <div className="glass-card p-8 text-center">
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-gray-700 font-medium">Loading progress data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen animated-gradient">
      {/* Header */}
      <div className="glass-nav sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center space-x-4">
            <button
              onClick={() => navigate('/student/dashboard')}
              className="glass-button p-3 hover-lift"
            >
              <ArrowLeft className="h-5 w-5 text-white" />
            </button>
            <div>
              <h1 className="text-xl font-bold text-white">Learning Progress</h1>
              <p className="text-white/80 text-sm">Comprehensive analytics and insights</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">
        {/* Overview Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="glass-card p-6 hover-lift">
            <div className="flex items-center">
              <div className="p-3 bg-gradient-primary rounded-xl">
                <TrendingUp className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <div className="text-2xl font-bold text-gray-900">{progressData.dailyStreaks.current}</div>
                <div className="text-sm text-gray-600">Current Streak</div>
              </div>
            </div>
          </div>
          
          <div className="glass-card p-6 hover-lift">
            <div className="flex items-center">
              <div className="p-3 bg-gradient-success rounded-xl">
                <Target className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <div className="text-2xl font-bold text-gray-900">
                  {Math.round(progressData.quizHistory.reduce((sum, quiz) => sum + quiz.score, 0) / progressData.quizHistory.length)}%
                </div>
                <div className="text-sm text-gray-600">Avg Quiz Score</div>
              </div>
            </div>
          </div>
          
          <div className="glass-card p-6 hover-lift">
            <div className="flex items-center">
              <div className="p-3 bg-gradient-secondary rounded-xl">
                <Award className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <div className="text-2xl font-bold text-gray-900">
                  {progressData.achievements.filter(a => a.earned).length}
                </div>
                <div className="text-sm text-gray-600">Achievements</div>
              </div>
            </div>
          </div>
          
          <div className="glass-card p-6 hover-lift">
            <div className="flex items-center">
              <div className="p-3 bg-gradient-warning rounded-xl">
                <Clock className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <div className="text-2xl font-bold text-gray-900">{progressData.dailyStreaks.longest}</div>
                <div className="text-sm text-gray-600">Longest Streak</div>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Topic Mastery */}
          <div className="glass-card p-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
              <Target className="h-5 w-5 mr-2 text-blue-600" />
              Topic Mastery
            </h2>
            <div className="space-y-6">
              {progressData.topicMastery.map((topic, index) => (
                <div key={index}>
                  <div className="flex justify-between items-center mb-2">
                    <span className="font-medium text-gray-900">{topic.subject}</span>
                    <div className="text-right">
                      <span className={`text-lg font-bold ${getMasteryColor(topic.mastery)}`}>
                        {topic.mastery}%
                      </span>
                      <div className="text-xs text-gray-500">
                        {topic.masteredTopics}/{topic.totalTopics} topics
                      </div>
                    </div>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-4">
                    <div 
                      className={`h-4 rounded-full transition-all duration-500 ${
                        topic.mastery >= 80 ? 'bg-green-500' :
                        topic.mastery >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                      }`}
                      style={{ width: `${topic.mastery}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Quiz History */}
          <div className="glass-card p-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
              <BarChart3 className="h-5 w-5 mr-2 text-green-600" />
              Recent Quiz Performance
            </h2>
            <div className="space-y-4">
              {progressData.quizHistory.map((quiz, index) => (
                <div key={index} className="glass-card p-4 hover-lift">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="font-medium text-gray-900">{quiz.type}</div>
                      <div className="text-sm text-gray-600">{quiz.subject}</div>
                      <div className="text-xs text-gray-500">
                        {new Date(quiz.date).toLocaleDateString()}
                      </div>
                    </div>
                    <div className="text-right">
                      <div className={`text-2xl font-bold ${
                        quiz.score >= 90 ? 'text-green-600' :
                        quiz.score >= 80 ? 'text-blue-600' :
                        quiz.score >= 70 ? 'text-yellow-600' : 'text-red-600'
                      }`}>
                        {quiz.score}%
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Consistency Heatmap */}
        <div className="glass-card p-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
            <Calendar className="h-5 w-5 mr-2 text-purple-600" />
            Study Consistency Heatmap
          </h2>
          <div className="space-y-4">
            <div className="grid grid-cols-7 gap-2 text-xs text-gray-500 mb-4">
              {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((day, i) => (
                <div key={i} className="text-center font-medium">{day}</div>
              ))}
            </div>
            {progressData.consistencyHeatmap.map((week, weekIndex) => (
              <div key={weekIndex} className="grid grid-cols-7 gap-2">
                {week.map((value, dayIndex) => (
                  <div
                    key={dayIndex}
                    className="w-8 h-8 rounded-md flex items-center justify-center text-xs font-medium"
                    style={{ 
                      backgroundColor: getHeatmapColor(value),
                      color: value > 2 ? 'white' : '#374151'
                    }}
                    title={`${value} hours studied`}
                  >
                    {value > 0 ? value : ''}
                  </div>
                ))}
              </div>
            ))}
            <div className="flex items-center justify-between text-xs text-gray-500 mt-4">
              <span>Less active</span>
              <div className="flex space-x-1">
                {[0, 1, 2, 3, 4].map(i => (
                  <div
                    key={i}
                    className="w-4 h-4 rounded-sm"
                    style={{ backgroundColor: getHeatmapColor(i) }}
                  ></div>
                ))}
              </div>
              <span>More active</span>
            </div>
          </div>
        </div>

        {/* Weekly Progress & Achievements */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Weekly Progress Chart */}
          <div className="glass-card p-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Weekly Progress</h2>
            <div className="space-y-4">
              {progressData.weeklyProgress.map((week, index) => (
                <div key={index} className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="font-medium text-gray-700">{week.week}</span>
                    <span className="text-gray-500">{week.completed}% / {week.target}%</span>
                  </div>
                  <div className="relative">
                    <div className="w-full bg-gray-200 rounded-full h-3">
                      <div 
                        className={`h-3 rounded-full transition-all duration-500 ${
                          week.completed >= week.target ? 'bg-green-500' : 'bg-blue-500'
                        }`}
                        style={{ width: `${Math.min(week.completed, 100)}%` }}
                      ></div>
                    </div>
                    <div 
                      className="absolute top-0 w-1 h-3 bg-red-500 rounded"
                      style={{ left: `${week.target}%` }}
                      title={`Target: ${week.target}%`}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Achievements */}
          <div className="glass-card p-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
              <Award className="h-5 w-5 mr-2 text-yellow-600" />
              Achievements
            </h2>
            <div className="space-y-4">
              {progressData.achievements.map((achievement, index) => (
                <div key={index} className={`glass-card p-4 ${
                  achievement.earned ? 'bg-yellow-50 border-yellow-200' : 'bg-gray-50 border-gray-200'
                } border`}>
                  <div className="flex items-center space-x-3">
                    <div className={`p-2 rounded-full ${
                      achievement.earned ? 'bg-yellow-500' : 'bg-gray-400'
                    }`}>
                      <Award className="h-4 w-4 text-white" />
                    </div>
                    <div>
                      <div className={`font-medium ${
                        achievement.earned ? 'text-yellow-800' : 'text-gray-600'
                      }`}>
                        {achievement.title}
                      </div>
                      <div className={`text-sm ${
                        achievement.earned ? 'text-yellow-700' : 'text-gray-500'
                      }`}>
                        {achievement.description}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProgressPage;