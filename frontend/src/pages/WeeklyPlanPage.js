import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { ArrowLeft, Calendar, Clock, Target, CheckCircle, Circle, Play } from 'lucide-react';

const WeeklyPlanPage = () => {
  const navigate = useNavigate();
  const [weeklyPlans, setWeeklyPlans] = useState([]);
  const [currentWeek, setCurrentWeek] = useState(1);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchWeeklyPlans();
  }, []);

  const fetchWeeklyPlans = async () => {
    try {
      // Mock weekly plans data
      const mockPlans = [
        {
          week: 1,
          title: 'Algebra Fundamentals',
          topics: ['Linear Equations', 'Graphing', 'Word Problems'],
          estimatedHours: 8,
          progress: 85,
          dailyTasks: [
            { day: 'Mon', tasks: ['Linear Equations Lesson', 'Practice Set A'], completed: [true, true] },
            { day: 'Tue', tasks: ['Graphing Tutorial', 'Quiz 1'], completed: [true, false] },
            { day: 'Wed', tasks: ['Word Problems', 'Practice Set B'], completed: [false, false] },
            { day: 'Thu', tasks: ['Review Session', 'Quiz 2'], completed: [false, false] },
            { day: 'Fri', tasks: ['Weekly Assessment'], completed: [false] }
          ]
        },
        {
          week: 2,
          title: 'Quadratic Functions',
          topics: ['Parabolas', 'Factoring', 'Vertex Form'],
          estimatedHours: 10,
          progress: 45,
          dailyTasks: [
            { day: 'Mon', tasks: ['Parabola Basics', 'Graphing Practice'], completed: [true, false] },
            { day: 'Tue', tasks: ['Factoring Methods', 'Practice Problems'], completed: [false, false] },
            { day: 'Wed', tasks: ['Vertex Form', 'Applications'], completed: [false, false] },
            { day: 'Thu', tasks: ['Mixed Practice', 'Quiz'], completed: [false, false] },
            { day: 'Fri', tasks: ['Weekly Test'], completed: [false] }
          ]
        }
      ];
      
      setWeeklyPlans(mockPlans);
      toast.success('Weekly plans loaded successfully');
    } catch (error) {
      toast.error('Failed to load weekly plans');
    } finally {
      setLoading(false);
    }
  };

  const handleTaskClick = (week, day, taskIndex) => {
    toast.info(`Opening ${weeklyPlans[week-1].dailyTasks.find(d => d.day === day).tasks[taskIndex]}...`);
  };

  const getCompletionColor = (progress) => {
    if (progress >= 80) return 'bg-green-500';
    if (progress >= 60) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  if (loading) {
    return (
      <div className="min-h-screen animated-gradient flex items-center justify-center">
        <div className="glass-card p-8 text-center">
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-gray-700 font-medium">Loading weekly plans...</p>
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
              <h1 className="text-xl font-bold text-white">Weekly Learning Plan</h1>
              <p className="text-white/80 text-sm">Interactive weekly overview</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Week Navigation */}
        <div className="glass-card p-6 mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900">Select Week</h2>
            <div className="text-sm text-gray-600">
              {weeklyPlans.length} weeks total
            </div>
          </div>
          
          <div className="flex space-x-4 overflow-x-auto">
            {weeklyPlans.map((plan) => (
              <button
                key={plan.week}
                onClick={() => setCurrentWeek(plan.week)}
                className={`flex-shrink-0 glass-card p-4 min-w-[200px] hover-lift ${
                  currentWeek === plan.week ? 'ring-2 ring-blue-500' : ''
                }`}
              >
                <div className="text-center">
                  <div className="text-lg font-semibold text-gray-900">Week {plan.week}</div>
                  <div className="text-sm text-gray-600 mb-2">{plan.title}</div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full ${getCompletionColor(plan.progress)}`}
                      style={{ width: `${plan.progress}%` }}
                    ></div>
                  </div>
                  <div className="text-xs text-gray-500 mt-1">{plan.progress}% complete</div>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Current Week Details */}
        {weeklyPlans.find(p => p.week === currentWeek) && (
          <div className="space-y-8">
            {(() => {
              const plan = weeklyPlans.find(p => p.week === currentWeek);
              return (
                <>
                  {/* Week Overview */}
                  <div className="glass-card p-8">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                      <div className="text-center">
                        <Calendar className="h-8 w-8 text-blue-600 mx-auto mb-2" />
                        <div className="text-2xl font-bold text-gray-900">Week {plan.week}</div>
                        <div className="text-sm text-gray-600">{plan.title}</div>
                      </div>
                      
                      <div className="text-center">
                        <Clock className="h-8 w-8 text-green-600 mx-auto mb-2" />
                        <div className="text-2xl font-bold text-gray-900">{plan.estimatedHours}h</div>
                        <div className="text-sm text-gray-600">Estimated Time</div>
                      </div>
                      
                      <div className="text-center">
                        <Target className="h-8 w-8 text-purple-600 mx-auto mb-2" />
                        <div className="text-2xl font-bold text-gray-900">{plan.progress}%</div>
                        <div className="text-sm text-gray-600">Progress</div>
                      </div>
                    </div>
                    
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-3">Topics This Week</h3>
                      <div className="flex flex-wrap gap-2">
                        {plan.topics.map((topic, index) => (
                          <span key={index} className="px-3 py-1 bg-gradient-primary text-white rounded-full text-sm">
                            {topic}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Daily Breakdown */}
                  <div className="glass-card p-8">
                    <h3 className="text-xl font-semibold text-gray-900 mb-6">Daily Breakdown</h3>
                    <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
                      {plan.dailyTasks.map((day, dayIndex) => (
                        <div key={dayIndex} className="glass-card p-4">
                          <div className="text-center mb-4">
                            <div className="font-semibold text-gray-900">{day.day}</div>
                            <div className="text-sm text-gray-500">
                              {day.completed.filter(Boolean).length}/{day.tasks.length} complete
                            </div>
                          </div>
                          
                          <div className="space-y-3">
                            {day.tasks.map((task, taskIndex) => (
                              <button
                                key={taskIndex}
                                onClick={() => handleTaskClick(plan.week, day.day, taskIndex)}
                                className="w-full glass-card p-3 text-left hover-lift"
                              >
                                <div className="flex items-center space-x-2">
                                  {day.completed[taskIndex] ? 
                                    <CheckCircle className="h-4 w-4 text-green-600 flex-shrink-0" /> : 
                                    <Circle className="h-4 w-4 text-gray-400 flex-shrink-0" />
                                  }
                                  <span className={`text-sm ${
                                    day.completed[taskIndex] ? 'text-green-600 line-through' : 'text-gray-700'
                                  }`}>
                                    {task}
                                  </span>
                                </div>
                              </button>
                            ))}
                          </div>
                          
                          <div className="mt-4">
                            <div className="w-full bg-gray-200 rounded-full h-2">
                              <div 
                                className="bg-gradient-primary h-2 rounded-full"
                                style={{ 
                                  width: `${(day.completed.filter(Boolean).length / day.tasks.length) * 100}%` 
                                }}
                              ></div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Quick Actions */}
                  <div className="glass-card p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <button 
                        onClick={() => navigate('/student/daily-plan')}
                        className="glass-button bg-gradient-primary text-white hover-lift"
                      >
                        <Play className="h-4 w-4 mr-2" />
                        Today's Tasks
                      </button>
                      <button 
                        onClick={() => navigate('/student/quiz/weekly')}
                        className="glass-button bg-gradient-success text-white hover-lift"
                      >
                        <Target className="h-4 w-4 mr-2" />
                        Weekly Quiz
                      </button>
                      <button 
                        onClick={() => navigate('/student/progress')}
                        className="glass-button bg-gradient-secondary text-white hover-lift"
                      >
                        <Calendar className="h-4 w-4 mr-2" />
                        View Progress
                      </button>
                    </div>
                  </div>
                </>
              );
            })()}
          </div>
        )}
      </div>
    </div>
  );
};

export default WeeklyPlanPage;