import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { Upload, Target, Brain, ArrowLeft, FileText, Sparkles } from 'lucide-react';

const StudentUploadGoals = () => {
  const navigate = useNavigate();
  const [goals, setGoals] = useState('');
  const [loading, setLoading] = useState(false);
  const [aiAnalysis, setAiAnalysis] = useState(null);

  const handleUploadGoals = async () => {
    if (!goals.trim()) {
      toast.error('Please enter your learning goals');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8003/api/goals/upload', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ goals })
      });
      
      const data = await response.json();
      setAiAnalysis(data.ai_analysis);
      toast.success('Goals analyzed successfully!');
    } catch (error) {
      toast.error('Failed to analyze goals');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen animated-gradient p-6">
      <div className="max-w-4xl mx-auto">
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
                  <Target className="w-8 h-8 text-blue-400" />
                  Upload Learning Goals
                </h1>
                <p className="text-blue-100">Let AI analyze and optimize your learning objectives</p>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Goals Input */}
          <div className="glass-card p-6">
            <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
              <FileText className="w-5 h-5 text-blue-400" />
              Your Learning Goals
            </h2>
            
            <textarea
              value={goals}
              onChange={(e) => setGoals(e.target.value)}
              placeholder="Enter your learning goals, target grades, exam objectives, or areas you want to improve..."
              className="glass-input w-full h-64 resize-none text-gray-900"
            />
            
            <button
              onClick={handleUploadGoals}
              disabled={loading || !goals.trim()}
              className="w-full mt-4 glass-button bg-gradient-primary text-white hover-lift disabled:opacity-50"
            >
              {loading ? (
                <div className="flex items-center justify-center gap-2">
                  <div className="spinner w-4 h-4"></div>
                  AI Analyzing...
                </div>
              ) : (
                <div className="flex items-center justify-center gap-2">
                  <Brain className="w-4 h-4" />
                  Analyze with AI
                </div>
              )}
            </button>
          </div>

          {/* AI Analysis Results */}
          <div className="glass-card p-6">
            <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-purple-400" />
              AI Analysis Results
            </h2>
            
            {!aiAnalysis ? (
              <div className="text-center py-12">
                <Brain className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-400">Upload your goals to see AI analysis</p>
              </div>
            ) : (
              <div className="space-y-6">
                {/* Parsed Goals */}
                <div>
                  <h3 className="font-semibold text-white mb-3">📋 Parsed Goals</h3>
                  <div className="space-y-2">
                    {aiAnalysis.parsed_goals.map((goal, index) => (
                      <div key={index} className="glass-card p-3 border-l-4 border-blue-500">
                        <div className="font-medium text-white">{goal.goal}</div>
                        <div className="text-sm text-gray-300 flex gap-4">
                          <span>Priority: {goal.priority}</span>
                          <span>Timeline: {goal.timeline}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* AI Recommendations */}
                <div>
                  <h3 className="font-semibold text-white mb-3">🤖 AI Recommendations</h3>
                  <div className="space-y-2">
                    {aiAnalysis.recommendations.map((rec, index) => (
                      <div key={index} className="glass-card p-3 bg-gradient-to-r from-purple-500/10 to-blue-500/10">
                        <div className="text-white">{rec}</div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Success Metrics */}
                <div>
                  <h3 className="font-semibold text-white mb-3">📊 Success Metrics</h3>
                  <div className="space-y-2">
                    {aiAnalysis.success_metrics.map((metric, index) => (
                      <div key={index} className="glass-card p-3 bg-gradient-to-r from-green-500/10 to-blue-500/10">
                        <div className="text-white">{metric}</div>
                      </div>
                    ))}
                  </div>
                </div>

                <button
                  onClick={() => navigate('/student/learning-path')}
                  className="w-full glass-button bg-gradient-success text-white hover-lift"
                >
                  Apply to Learning Path
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default StudentUploadGoals;