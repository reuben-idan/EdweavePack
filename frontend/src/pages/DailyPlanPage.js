import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { ArrowLeft, CheckCircle, Circle, Play, Clock, Target, BookOpen, Brain, Calendar } from 'lucide-react';

const DailyPlanPage = () => {
  const navigate = useNavigate();
  const [dailyTasks, setDailyTasks] = useState([]);
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDailyTasks();
  }, [selectedDate]);

  const fetchDailyTasks = async () => {
    try {
      setLoading(true);
      
      // Mock daily tasks data
      const mockTasks = [
        {
          id: 1,
          type: 'lesson',
          title: 'Quadratic Functions Introduction',
          description: 'Learn the basics of quadratic functions and their properties',
          duration: 30,
          priority: 'high',
          completed: false,
          estimatedTime: '9:00 AM'
        },
        {
          id: 2,
          type: 'practice',
          title: 'Solve 15 Quadratic Problems',
          description: 'Practice solving quadratic equations using different methods',
          duration: 45,
          priority: 'high',
          completed: true,
          estimatedTime: '10:00 AM'
        },
        {
          id: 3,
          type: 'quiz',
          title: 'Daily Math Quiz',
          description: 'Quick assessment of today\'s learning',
          duration: 15,
          priority: 'medium',
          completed: false,
          estimatedTime: '2:00 PM'
        },
        {
          id: 4,
          type: 'reading',
          title: 'Read Chapter 8: Parabolas',
          description: 'Study the properties and applications of parabolas',
          duration: 25,
          priority: 'medium',
          completed: false,
          estimatedTime: '3:00 PM'
        },
        {
          id: 5,
          type: 'reflection',
          title: 'Create Concept Map',
          description: 'Summarize today\'s learning in a visual concept map',
          duration: 20,
          priority: 'low',
          completed: false,
          estimatedTime: '4:00 PM'
        }
      ];
      
      setDailyTasks(mockTasks);
      toast.success('Daily tasks loaded successfully');
    } catch (error) {
      toast.error('Failed to load daily tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleTaskToggle = (taskId) => {
    setDailyTasks(prev => prev.map(task => 
      task.id === taskId ? { ...task, completed: !task.completed } : task
    ));
    
    const task = dailyTasks.find(t => t.id === taskId);
    toast.success(task.completed ? 'Task marked as incomplete' : 'Task completed! Great job!');
  };

  const handleStartTask = (task) => {
    if (task.type === 'quiz') {
      navigate(`/student/quiz/${task.id}`);
    } else {
      toast.info(`Starting ${task.title}...`);
    }
  };

  const getTaskIcon = (type) => {
    switch (type) {
      case 'lesson': return <BookOpen className="h-5 w-5 text-blue-600" />;
      case 'practice': return <Target className="h-5 w-5 text-green-600" />;
      case 'quiz': return <Brain className="h-5 w-5 text-purple-600" />;
      case 'reading': return <BookOpen className="h-5 w-5 text-orange-600" />;
      case 'reflection': return <Circle className="h-5 w-5 text-pink-600" />;
      default: return <Circle className="h-5 w-5 text-gray-600" />;
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return 'border-red-500 bg-red-50';
      case 'medium': return 'border-yellow-500 bg-yellow-50';
      case 'low': return 'border-green-500 bg-green-50';
      default: return 'border-gray-500 bg-gray-50';
    }
  };

  const completedTasks = dailyTasks.filter(task => task.completed).length;
  const totalTasks = dailyTasks.length;
  const completionPercentage = totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0;

  if (loading) {
    return (
      <div className="min-h-screen animated-gradient flex items-center justify-center">
        <div className="glass-card p-8 text-center">
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-gray-700 font-medium">Loading daily plan...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen animated-gradient">
      {/* Header */}
      <div className="glass-nav sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center space-x-4">
            <button
              onClick={() => navigate('/student/dashboard')}
              className="glass-button p-3 hover-lift"
            >
              <ArrowLeft className="h-5 w-5 text-white" />
            </button>
            <div>
              <h1 className="text-xl font-bold text-white">Daily Learning Plan</h1>
              <p className="text-white/80 text-sm">
                {new Date(selectedDate).toLocaleDateString('en-US', { 
                  weekday: 'long', 
                  year: 'numeric', 
                  month: 'long', 
                  day: 'numeric' 
                })}
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
        {/* Date Selector & Progress */}
        <div className="glass-card p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-xl font-semibold text-gray-900">Today's Progress</h2>
              <p className="text-gray-600">{completedTasks} of {totalTasks} tasks completed</p>
            </div>
            
            <div className="flex items-center space-x-4">
              <input
                type="date"
                value={selectedDate}
                onChange={(e) => setSelectedDate(e.target.value)}
                className="glass-input px-3 py-2 text-gray-900"
              />
            </div>
          </div>
          
          {/* Progress Ring */}
          <div className="flex items-center justify-center mb-6">
            <div className="relative w-32 h-32">
              <svg className="w-32 h-32 transform -rotate-90" viewBox="0 0 120 120">
                <circle
                  cx="60"
                  cy="60"
                  r="50"
                  stroke="currentColor"
                  strokeWidth="8"
                  fill="none"
                  className="text-gray-200"
                />
                <circle
                  cx="60"
                  cy="60"
                  r="50"
                  stroke="currentColor"
                  strokeWidth="8"
                  fill="none"
                  strokeDasharray={`${2 * Math.PI * 50}`}
                  strokeDashoffset={`${2 * Math.PI * 50 * (1 - completionPercentage / 100)}`}
                  className="text-blue-600 transition-all duration-500"
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-center">
                  <div className="text-2xl font-bold text-gray-900">{Math.round(completionPercentage)}%</div>
                  <div className="text-sm text-gray-600">Complete</div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-lg font-semibold text-gray-900">{completedTasks}</div>
              <div className="text-sm text-gray-600">Completed</div>
            </div>
            <div>
              <div className="text-lg font-semibold text-gray-900">{totalTasks - completedTasks}</div>
              <div className="text-sm text-gray-600">Remaining</div>
            </div>
            <div>
              <div className="text-lg font-semibold text-gray-900">
                {dailyTasks.reduce((sum, task) => sum + task.duration, 0)} min
              </div>
              <div className="text-sm text-gray-600">Total Time</div>
            </div>
          </div>
        </div>

        {/* Task List */}
        <div className="glass-card p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Today's Tasks</h2>
          
          {dailyTasks.length === 0 ? (
            <div className="text-center py-8">
              <Calendar className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No tasks for today</h3>
              <p className="text-gray-600">Enjoy your free day or check back tomorrow!</p>
            </div>
          ) : (
            <div className="space-y-4">
              {dailyTasks.map((task) => (
                <div
                  key={task.id}
                  className={`glass-card p-4 border-l-4 ${getPriorityColor(task.priority)} hover-lift`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4 flex-1">
                      {/* Checkbox */}
                      <button
                        onClick={() => handleTaskToggle(task.id)}
                        className={`p-2 rounded-full transition-colors ${
                          task.completed ? 'bg-green-500' : 'bg-gray-300 hover:bg-gray-400'
                        }`}
                      >
                        {task.completed ? 
                          <CheckCircle className="h-5 w-5 text-white" /> : 
                          <Circle className="h-5 w-5 text-gray-600" />
                        }
                      </button>
                      
                      {/* Task Icon */}
                      <div className="p-2 bg-white rounded-lg">
                        {getTaskIcon(task.type)}
                      </div>
                      
                      {/* Task Details */}
                      <div className="flex-1">
                        <div className={`font-medium ${
                          task.completed ? 'text-gray-500 line-through' : 'text-gray-900'
                        }`}>
                          {task.title}
                        </div>
                        <div className="text-sm text-gray-600 mt-1">{task.description}</div>
                        <div className="flex items-center space-x-4 mt-2 text-xs text-gray-500">
                          <div className="flex items-center">
                            <Clock className="h-3 w-3 mr-1" />
                            {task.duration} min
                          </div>
                          <div className="flex items-center">
                            <Calendar className="h-3 w-3 mr-1" />
                            {task.estimatedTime}
                          </div>
                          <div className={`px-2 py-1 rounded-full text-xs font-medium ${
                            task.priority === 'high' ? 'bg-red-100 text-red-800' :
                            task.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-green-100 text-green-800'
                          }`}>
                            {task.priority} priority
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    {/* Action Button */}
                    {!task.completed && (
                      <button
                        onClick={() => handleStartTask(task)}
                        className="glass-button bg-gradient-primary text-white ml-4"
                      >
                        <Play className="h-4 w-4 mr-2" />
                        Start
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Quick Actions */}
        <div className="glass-card p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button 
              onClick={() => navigate('/student/weekly-plan')}
              className="glass-button bg-gradient-secondary text-white hover-lift"
            >
              <Calendar className="h-4 w-4 mr-2" />
              Weekly Plan
            </button>
            <button 
              onClick={() => navigate('/student/quiz/daily')}
              className="glass-button bg-gradient-success text-white hover-lift"
            >
              <Brain className="h-4 w-4 mr-2" />
              Daily Quiz
            </button>
            <button 
              onClick={() => navigate('/student/progress')}
              className="glass-button bg-gradient-warning text-white hover-lift"
            >
              <Target className="h-4 w-4 mr-2" />
              View Progress
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DailyPlanPage;