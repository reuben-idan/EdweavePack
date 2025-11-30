import React, { useState, useEffect } from 'react';
import { 
  Brain, 
  TrendingUp, 
  Users, 
  BookOpen, 
  Target, 
  Zap,
  MessageSquare,
  BarChart3,
  Lightbulb,
  Sparkles
} from 'lucide-react';
import { useAuth } from '../hooks/useAuth';

const AIEnhancedDashboard = ({ userRole = 'teacher' }) => {
  const { user } = useAuth();
  const [aiInsights, setAiInsights] = useState(null);
  const [loading, setLoading] = useState(true);
  const [suggestions, setSuggestions] = useState([]);

  useEffect(() => {
    fetchAIInsights();
  }, [userRole]);

  const fetchAIInsights = async () => {
    try {
      setLoading(true);
      
      // Fetch role-specific AI insights
      const response = await fetch('/api/ai/learning-insights', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      const data = await response.json();
      
      if (data.success) {
        setAiInsights(data.insights);
        generateSuggestions(data.insights);
      }
    } catch (error) {
      console.error('Failed to fetch AI insights:', error);
    } finally {
      setLoading(false);
    }
  };

  const generateSuggestions = (insights) => {
    const roleSuggestions = {
      teacher: [
        "Create adaptive assessments for struggling students",
        "Generate differentiated content for visual learners",
        "Analyze student performance patterns",
        "Design intervention strategies"
      ],
      student: [
        "Review concepts you're struggling with",
        "Practice with AI-generated questions",
        "Get personalized study recommendations",
        "Track your learning progress"
      ],
      curriculum_creator: [
        "Analyze content alignment with standards",
        "Optimize learning sequence",
        "Enhance accessibility features",
        "Validate assessment quality"
      ]
    };
    
    setSuggestions(roleSuggestions[userRole] || roleSuggestions.teacher);
  };

  const AIInsightCard = ({ title, value, trend, icon: Icon, color = "blue" }) => (
    <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
          {trend && (
            <p className={`text-sm mt-1 flex items-center ${
              trend > 0 ? 'text-green-600' : 'text-red-600'
            }`}>
              <TrendingUp size={16} className="mr-1" />
              {trend > 0 ? '+' : ''}{trend}%
            </p>
          )}
        </div>
        <div className={`p-3 rounded-full bg-${color}-100`}>
          <Icon className={`w-6 h-6 text-${color}-600`} />
        </div>
      </div>
    </div>
  );

  const AIActionCard = ({ title, description, action, icon: Icon }) => (
    <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-4 border border-purple-200">
      <div className="flex items-start space-x-3">
        <div className="p-2 bg-purple-100 rounded-lg">
          <Icon className="w-5 h-5 text-purple-600" />
        </div>
        <div className="flex-1">
          <h4 className="font-semibold text-gray-900">{title}</h4>
          <p className="text-sm text-gray-600 mt-1">{description}</p>
          <button 
            onClick={action}
            className="mt-2 text-sm bg-purple-600 text-white px-3 py-1 rounded hover:bg-purple-700 transition-colors"
          >
            Try Now
          </button>
        </div>
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center space-x-2">
          <Brain className="w-6 h-6 text-purple-600 animate-pulse" />
          <h2 className="text-xl font-bold text-gray-900">Loading AI Insights...</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[1, 2, 3].map(i => (
            <div key={i} className="bg-gray-200 rounded-lg h-32 animate-pulse"></div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* AI Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Brain className="w-6 h-6 text-purple-600" />
          <h2 className="text-xl font-bold text-gray-900">AI-Powered Insights</h2>
          <Sparkles className="w-5 h-5 text-yellow-500" />
        </div>
        <button 
          onClick={fetchAIInsights}
          className="flex items-center space-x-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
        >
          <Zap className="w-4 h-4" />
          <span>Refresh Insights</span>
        </button>
      </div>

      {/* Role-specific AI Metrics */}
      {userRole === 'teacher' && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <AIInsightCard
            title="Student Engagement"
            value="87%"
            trend={5}
            icon={Users}
            color="green"
          />
          <AIInsightCard
            title="Content Effectiveness"
            value="92%"
            trend={3}
            icon={BookOpen}
            color="blue"
          />
          <AIInsightCard
            title="Learning Objectives Met"
            value="15/18"
            trend={8}
            icon={Target}
            color="purple"
          />
          <AIInsightCard
            title="AI Recommendations"
            value="12"
            icon={Lightbulb}
            color="yellow"
          />
        </div>
      )}

      {userRole === 'student' && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <AIInsightCard
            title="Learning Progress"
            value="78%"
            trend={12}
            icon={TrendingUp}
            color="green"
          />
          <AIInsightCard
            title="Concepts Mastered"
            value="24/30"
            trend={6}
            icon={Brain}
            color="blue"
          />
          <AIInsightCard
            title="Study Streak"
            value="7 days"
            icon={Target}
            color="purple"
          />
          <AIInsightCard
            title="AI Study Tips"
            value="5"
            icon={Lightbulb}
            color="yellow"
          />
        </div>
      )}

      {userRole === 'curriculum_creator' && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <AIInsightCard
            title="Content Quality Score"
            value="94%"
            trend={2}
            icon={BarChart3}
            color="green"
          />
          <AIInsightCard
            title="Standards Alignment"
            value="98%"
            trend={1}
            icon={Target}
            color="blue"
          />
          <AIInsightCard
            title="Accessibility Score"
            value="89%"
            trend={7}
            icon={Users}
            color="purple"
          />
          <AIInsightCard
            title="AI Optimizations"
            value="8"
            icon={Zap}
            color="yellow"
          />
        </div>
      )}

      {/* AI-Powered Suggestions */}
      <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-200">
        <div className="flex items-center space-x-2 mb-4">
          <Lightbulb className="w-5 h-5 text-yellow-500" />
          <h3 className="text-lg font-semibold text-gray-900">AI Recommendations</h3>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {suggestions.map((suggestion, index) => (
            <AIActionCard
              key={index}
              title={`Recommendation ${index + 1}`}
              description={suggestion}
              action={() => console.log('Action:', suggestion)}
              icon={Brain}
            />
          ))}
        </div>
      </div>

      {/* AI Analytics Chart Placeholder */}
      <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-200">
        <div className="flex items-center space-x-2 mb-4">
          <BarChart3 className="w-5 h-5 text-blue-500" />
          <h3 className="text-lg font-semibold text-gray-900">Learning Analytics</h3>
        </div>
        
        <div className="h-64 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg flex items-center justify-center">
          <div className="text-center">
            <Brain className="w-12 h-12 text-purple-400 mx-auto mb-2" />
            <p className="text-gray-600">AI-powered analytics visualization</p>
            <p className="text-sm text-gray-500">Real-time learning insights and predictions</p>
          </div>
        </div>
      </div>

      {/* Quick AI Actions */}
      <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg p-6 text-white">
        <div className="flex items-center space-x-2 mb-4">
          <MessageSquare className="w-5 h-5" />
          <h3 className="text-lg font-semibold">AI Assistant Ready</h3>
        </div>
        
        <p className="mb-4 opacity-90">
          Your AI assistant is ready to help with {
            userRole === 'teacher' ? 'curriculum design, student analytics, and teaching strategies' :
            userRole === 'student' ? 'learning support, concept explanations, and study planning' :
            'content analysis, quality assurance, and optimization recommendations'
          }.
        </p>
        
        <div className="flex flex-wrap gap-2">
          <button className="px-4 py-2 bg-white bg-opacity-20 rounded-lg hover:bg-opacity-30 transition-colors">
            Ask AI Assistant
          </button>
          <button className="px-4 py-2 bg-white bg-opacity-20 rounded-lg hover:bg-opacity-30 transition-colors">
            Generate Content
          </button>
          <button className="px-4 py-2 bg-white bg-opacity-20 rounded-lg hover:bg-opacity-30 transition-colors">
            Analyze Performance
          </button>
        </div>
      </div>
    </div>
  );
};

export default AIEnhancedDashboard;