import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { ArrowLeft, Calendar, Clock, Target, TrendingUp, CheckCircle, Circle, Play, BookOpen, Brain } from 'lucide-react';

const StudentLearningPath = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('weekly');
  const [learningPath, setLearningPath] = useState(null);

  useEffect(() => {
    generateLearningPath();
  }, []);

  const generateLearningPath = async () => {
    try {
      setLoading(true);
      toast.info('AI is generating your personalized learning path...');
      
      // Mock AI-generated learning path
      const mockPath = {
        weeklyPlan: [
          {
            week: 1,
            title: 'Algebra Fundamentals',
            topics: ['Linear Equations', 'Quadratic Functions', 'Graphing'],
            difficulty: 'Beginner',
            estimatedHours: 8,
            progress: 75,
            dailyTasks: [
              { day: 'Monday', tasks: ['Watch Linear Equations video', 'Complete 10 practice problems', 'Read Chapter 3'], completed: [true, true, false] },
              { day: 'Tuesday', tasks: ['Quiz: Linear Equations', 'Practice graphing', 'Review notes'], completed: [true, false, false] },
              { day: 'Wednesday', tasks: ['Quadratic functions lesson', 'Solve 15 problems', 'Create summary'], completed: [false, false, false] }
            ]
          },
          {
            week: 2,
            title: 'Advanced Algebra',
            topics: ['Polynomials', 'Factoring', 'Systems of Equations'],
            difficulty: 'Intermediate',
            estimatedHours: 10,
            progress: 0,
            dailyTasks: []
          }
        ],
        todaysTasks: [
          { id: 1, type: 'lesson', title: 'Quadratic Functions Introduction', duration: 30, completed: false },
          { id: 2, type: 'practice', title: 'Solve 15 Quadratic Problems', duration: 45, completed: false },
          { id: 3, type: 'quiz', title: 'Daily Math Quiz', duration: 15, completed: true },
          { id: 4, type: 'reading', title: 'Read: Factoring Methods', duration: 20, completed: false }
        ],
        quizzes: [
          { id: 1, title: 'Linear Equations Quiz', score: 85, date: '2024-01-20', questions: 10 },
          { id: 2, title: 'Daily Practice Quiz', score: 92, date: '2024-01-21', questions: 5 },
          { id: 3, title: 'Weekly Assessment', score: null, date: null, questions: 15, available: true }
        ],
        progress: {
          overallCompletion: 35,
          weeklyCompletion: 75,
          averageScore: 88,
          streak: 5,
          recommendations: [
            'Revise quadratic factoring - you scored 65% on this topic',
            'Increase practice on word problems - spend 15 more minutes daily',
            'Focus more on graphing techniques this week'
          ]
        }
      };
      
      setLearningPath(mockPath);
      toast.success('Your personalized learning path is ready!');
      
    } catch (error) {
      toast.error('Failed to generate learning path');
    } finally {
      setLoading(false);
    }
  };

  const handleTaskComplete = (taskId) => {
    setLearningPath(prev => ({
      ...prev,
      todaysTasks: prev.todaysTasks.map(task =>
        task.id === taskId ? { ...task, completed: !task.completed } : task
      )
    }));
    toast.success('Task updated!');
  };

  const handleStartQuiz = (quizId) => {
    toast.info('Starting quiz...');
    navigate(`/student/quiz/${quizId}`);
  };

  if (loading) {
    return (
      <div className="min-h-screen animated-gradient flex items-center justify-center">
        <div className="glass-card p-8 text-center">
          <Brain className="h-16 w-16 text-blue-600 mx-auto mb-4 animate-pulse" />
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-gray-700 font-medium">AI is creating your personalized learning path...</p>
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
              <h1 className="text-xl font-bold text-white">My Learning Path</h1>
              <p className="text-white/80 text-sm">AI-generated personalized study plan</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Progress Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="glass-card p-6 hover-lift">
            <div className="flex items-center">
              <div className="p-3 bg-gradient-primary rounded-xl">
                <Target className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <div className="text-2xl font-bold text-gray-900">{learningPath.progress.overallCompletion}%</div>
                <div className="text-sm text-gray-600">Overall Progress</div>
              </div>
            </div>
          </div>
          
          <div className="glass-card p-6 hover-lift">
            <div className="flex items-center">
              <div className="p-3 bg-gradient-success rounded-xl">
                <TrendingUp className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <div className="text-2xl font-bold text-gray-900">{learningPath.progress.averageScore}%</div>
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
                <div className="text-2xl font-bold text-gray-900">{learningPath.progress.streak}</div>
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
                <div className="text-2xl font-bold text-gray-900">{learningPath.progress.weeklyCompletion}%</div>
                <div className="text-sm text-gray-600">This Week</div>
              </div>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="glass-card p-2 mb-8">
          <nav className="flex space-x-2">
            {[
              { id: 'weekly', label: 'Weekly Plan' },
              { id: 'daily', label: 'Today\'s Tasks' },
              { id: 'quizzes', label: 'Quizzes' },
              { id: 'progress', label: 'Progress & Tips' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-6 py-3 rounded-xl font-medium text-sm transition-all duration-300 ${
                  activeTab === tab.id
                    ? 'bg-gradient-primary text-white shadow-lg'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-white/50'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Content */}
        <div>
          {/* Weekly Plan */}
          {activeTab === 'weekly' && (
            <div className="space-y-6">
              {learningPath.weeklyPlan.map((week) => (
                <div key={week.week} className="glass-card p-8 hover-lift">
                  <div className="flex items-center justify-between mb-6">
                    <div>
                      <h3 className="text-xl font-semibold text-gray-900">Week {week.week}: {week.title}</h3>
                      <p className="text-gray-600">Difficulty: {week.difficulty} • {week.estimatedHours} hours</p>
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-bold text-gray-900">{week.progress}%</div>
                      <div className="text-sm text-gray-600">Complete</div>
                    </div>
                  </div>
                  
                  <div className="mb-4">
                    <div className="w-full bg-gray-200 rounded-full h-3">
                      <div 
                        className="bg-gradient-primary h-3 rounded-full transition-all duration-500" 
                        style={{ width: `${week.progress}%` }}
                      ></div>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                    {week.topics.map((topic, index) => (
                      <div key={index} className="glass-card p-4">
                        <div className="font-medium text-gray-900">{topic}</div>
                      </div>
                    ))}
                  </div>
                  
                  {week.dailyTasks.length > 0 && (
                    <div>
                      <h4 className="font-semibold text-gray-900 mb-3">Daily Breakdown:</h4>
                      <div className="space-y-2">
                        {week.dailyTasks.map((day, dayIndex) => (
                          <div key={dayIndex} className="glass-card p-4">
                            <div className="font-medium text-gray-900 mb-2">{day.day}</div>
                            <div className="space-y-1">
                              {day.tasks.map((task, taskIndex) => (
                                <div key={taskIndex} className="flex items-center space-x-2 text-sm">
                                  {day.completed[taskIndex] ? 
                                    <CheckCircle className="h-4 w-4 text-green-600" /> : 
                                    <Circle className="h-4 w-4 text-gray-400" />
                                  }
                                  <span className={day.completed[taskIndex] ? 'text-green-600' : 'text-gray-600'}>
                                    {task}
                                  </span>
                                </div>
                              ))}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Today's Tasks */}
          {activeTab === 'daily' && (
            <div className="glass-card p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Today's Learning Tasks</h2>
              <div className="space-y-4">
                {learningPath.todaysTasks.map((task) => (
                  <div key={task.id} className="glass-card p-6 hover-lift">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4">
                        <button
                          onClick={() => handleTaskComplete(task.id)}
                          className={`p-2 rounded-full ${task.completed ? 'bg-green-500' : 'bg-gray-300'}`}
                        >
                          <CheckCircle className={`h-5 w-5 ${task.completed ? 'text-white' : 'text-gray-500'}`} />
                        </button>
                        
                        <div className={`p-3 rounded-xl ${
                          task.type === 'lesson' ? 'bg-blue-100' :
                          task.type === 'practice' ? 'bg-green-100' :
                          task.type === 'quiz' ? 'bg-purple-100' : 'bg-orange-100'
                        }`}>
                          {task.type === 'lesson' && <BookOpen className="h-5 w-5 text-blue-600" />}
                          {task.type === 'practice' && <Target className="h-5 w-5 text-green-600" />}
                          {task.type === 'quiz' && <Brain className="h-5 w-5 text-purple-600" />}
                          {task.type === 'reading' && <BookOpen className="h-5 w-5 text-orange-600" />}
                        </div>
                        
                        <div>
                          <div className={`font-medium ${task.completed ? 'text-gray-500 line-through' : 'text-gray-900'}`}>
                            {task.title}
                          </div>
                          <div className="text-sm text-gray-500">{task.duration} minutes • {task.type}</div>
                        </div>
                      </div>
                      
                      {!task.completed && (
                        <button className="glass-button bg-gradient-primary text-white">
                          <Play className="h-4 w-4 mr-2" />
                          Start
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Quizzes */}
          {activeTab === 'quizzes' && (
            <div className="space-y-6">
              <div className="glass-card p-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">Practice Quizzes</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {learningPath.quizzes.map((quiz) => (
                    <div key={quiz.id} className="glass-card p-6 hover-lift">
                      <div className="flex items-center justify-between mb-4">
                        <h3 className="font-semibold text-gray-900">{quiz.title}</h3>
                        {quiz.score !== null && (
                          <div className="text-right">
                            <div className="text-lg font-bold text-gray-900">{quiz.score}%</div>
                            <div className="text-sm text-gray-500">Score</div>
                          </div>
                        )}
                      </div>
                      
                      <div className="text-sm text-gray-600 mb-4">
                        {quiz.questions} questions
                        {quiz.date && ` • Completed ${new Date(quiz.date).toLocaleDateString()}`}
                      </div>
                      
                      {quiz.available && quiz.score === null ? (
                        <button
                          onClick={() => handleStartQuiz(quiz.id)}
                          className="w-full glass-button bg-gradient-primary text-white"
                        >
                          <Play className="h-4 w-4 mr-2" />
                          Start Quiz
                        </button>
                      ) : quiz.score !== null ? (
                        <button className="w-full glass-button bg-gradient-success text-white">
                          <CheckCircle className="h-4 w-4 mr-2" />
                          Completed
                        </button>
                      ) : (
                        <button className="w-full glass-button text-gray-500" disabled>
                          Available Soon
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Progress & Recommendations */}
          {activeTab === 'progress' && (
            <div className="space-y-6">
              <div className="glass-card p-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">AI Recommendations</h2>
                <div className="space-y-4">
                  {learningPath.progress.recommendations.map((rec, index) => (
                    <div key={index} className="glass-card p-4 border-l-4 border-blue-500">
                      <div className="flex items-start space-x-3">
                        <Brain className="h-5 w-5 text-blue-600 mt-0.5" />
                        <p className="text-gray-700">{rec}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              
              <div className="glass-card p-8">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Learning Analytics</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <div className="text-sm text-gray-600 mb-2">Weekly Progress</div>
                    <div className="w-full bg-gray-200 rounded-full h-4">
                      <div 
                        className="bg-gradient-primary h-4 rounded-full" 
                        style={{ width: `${learningPath.progress.weeklyCompletion}%` }}
                      ></div>
                    </div>
                    <div className="text-sm text-gray-500 mt-1">{learningPath.progress.weeklyCompletion}% complete</div>
                  </div>
                  
                  <div>
                    <div className="text-sm text-gray-600 mb-2">Overall Progress</div>
                    <div className="w-full bg-gray-200 rounded-full h-4">
                      <div 
                        className="bg-gradient-success h-4 rounded-full" 
                        style={{ width: `${learningPath.progress.overallCompletion}%` }}
                      ></div>
                    </div>
                    <div className="text-sm text-gray-500 mt-1">{learningPath.progress.overallCompletion}% complete</div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default StudentLearningPath;