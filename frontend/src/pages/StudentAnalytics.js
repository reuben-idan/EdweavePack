import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { BarChart3, TrendingUp, Brain, ArrowLeft, Target, Clock, Award, AlertTriangle } from 'lucide-react';

const StudentAnalytics = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [aiInsights, setAiInsights] = useState(null);

  useEffect(() => {
    fetchAIInsights();
  }, []);

  const fetchAIInsights = async () => {
    try {
      const response = await fetch('http://localhost:8003/api/analytics/ai-insights');
      const data = await response.json();
      setAiInsights(data);
      toast.success('AI insights loaded successfully!');
    } catch (error) {
      toast.error('Failed to load analytics');
    } finally {
      setLoading(false);
    }
  };

  const getInsightIcon = (type) => {
    switch (type) {
      case 'performance_trend': return <TrendingUp className="w-5 h-5" />;
      case 'engagement_pattern': return <Clock className="w-5 h-5" />;
      case 'content_gap': return <AlertTriangle className="w-5 h-5" />;
      default: return <Brain className="w-5 h-5" />;
    }
  };

  const getInsightColor = (type) => {
    switch (type) {
      case 'performance_trend': return 'from-green-500 to-blue-500';
      case 'engagement_pattern': return 'from-blue-500 to-purple-500';
      case 'content_gap': return 'from-yellow-500 to-red-500';
      default: return 'from-gray-500 to-gray-600';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen animated-gradient flex items-center justify-center">
        <div className="glass-card p-8 text-center">
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-white font-medium">Loading AI analytics...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen animated-gradient p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="glass-card p-6 mb-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/student/dashboard')}
                className="glass-button p-3"
              >
                <ArrowLeft className="h-5 w-5" />
              </button>
              <div>
                <h1 className="text-2xl font-bold text-white flex items-center gap-3">
                  <BarChart3 className="w-8 h-8 text-blue-400" />
                  AI Learning Analytics
                </h1>
                <p className="text-blue-100">Personalized insights powered by artificial intelligence</p>
              </div>
            </div>
          </div>
        </div>

        {/* AI Predictions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div className="glass-card p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-blue-100 text-sm">Predicted Performance</p>
                <p className="text-3xl font-bold text-white">{aiInsights?.predictions?.next_month_performance}%</p>
                <p className="text-green-400 text-sm">Next Month</p>
              </div>
              <TrendingUp className="w-12 h-12 text-green-400" />
            </div>
          </div>

          <div className="glass-card p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-blue-100 text-sm">At-Risk Areas</p>
                <p className="text-3xl font-bold text-white">{aiInsights?.predictions?.at_risk_students}</p>
                <p className="text-yellow-400 text-sm">Subjects</p>
              </div>
              <AlertTriangle className="w-12 h-12 text-yellow-400" />
            </div>
          </div>

          <div className="glass-card p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-blue-100 text-sm">Completion Rate</p>
                <p className="text-3xl font-bold text-white">{aiInsights?.predictions?.completion_rate}%</p>
                <p className="text-blue-400 text-sm">Projected</p>
              </div>
              <Award className="w-12 h-12 text-blue-400" />
            </div>
          </div>
        </div>

        {/* AI Insights */}
        <div className="glass-card p-6">
          <h2 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
            <Brain className="w-6 h-6 text-purple-400" />
            AI-Powered Learning Insights
          </h2>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {aiInsights?.insights?.map((insight, index) => (
              <div key={index} className="glass-card p-6 hover-lift">
                <div className="flex items-start gap-4">
                  <div className={`p-3 rounded-xl bg-gradient-to-r ${getInsightColor(insight.type)}`}>
                    {getInsightIcon(insight.type)}
                  </div>
                  
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-semibold text-white">{insight.title}</h3>
                      <div className="flex items-center gap-2">
                        <span className="px-2 py-1 bg-blue-500/20 text-blue-300 text-xs rounded-full">
                          AI
                        </span>
                        <span className="text-xs text-gray-400">
                          {Math.round(insight.confidence * 100)}% confidence
                        </span>
                      </div>
                    </div>
                    
                    <p className="text-gray-300 text-sm mb-4">{insight.description}</p>
                    
                    <div className="bg-white/5 p-3 rounded-lg border-l-4 border-blue-500">
                      <p className="text-blue-200 text-sm font-medium">
                        💡 Recommendation: {insight.recommendation}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Performance Chart Placeholder */}
        <div className="glass-card p-6 mt-6">
          <h2 className="text-xl font-semibold text-white mb-6">Performance Trends</h2>
          <div className="bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-lg p-8 text-center">
            <BarChart3 className="w-16 h-16 text-blue-400 mx-auto mb-4" />
            <p className="text-white font-medium mb-2">Interactive Performance Charts</p>
            <p className="text-gray-300 text-sm">AI-powered visualizations showing your learning progress, strengths, and areas for improvement</p>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-4 mt-6">
          <button
            onClick={() => navigate('/student/learning-path')}
            className="flex-1 glass-button bg-gradient-primary text-white hover-lift"
          >
            <Target className="w-4 h-4 mr-2" />
            Optimize Learning Path
          </button>
          <button
            onClick={() => navigate('/student/upload-goals')}
            className="flex-1 glass-button bg-gradient-secondary text-white hover-lift"
          >
            <Brain className="w-4 h-4 mr-2" />
            Update Goals
          </button>
        </div>
      </div>
    </div>
  );
};

export default StudentAnalytics;