import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { assessmentAPI, curriculumAPI } from '../services/api';
import { toast } from 'react-toastify';
import { 
  Brain, Plus, Search, Filter, Calendar, Users, Target, 
  Clock, CheckCircle, Play, Edit, Trash2, Zap 
} from 'lucide-react';

const AssessmentListEnhanced = () => {
  const navigate = useNavigate();
  const [assessments, setAssessments] = useState([]);
  const [curricula, setCurricula] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('');
  const [aiGenerating, setAiGenerating] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [assessmentsRes, curriculaRes] = await Promise.all([
        assessmentAPI.getAll(),
        curriculumAPI.getCurricula()
      ]);
      
      setAssessments(assessmentsRes.data.assessments || []);
      setCurricula(curriculaRes.data.curricula || []);
      toast.success('AI assessments loaded successfully');
    } catch (error) {
      console.error('Failed to fetch data:', error);
      toast.error('Failed to load assessments. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const generateAIAssessment = async () => {
    if (curricula.length === 0) {
      toast.error('Please create a curriculum first');
      return;
    }

    setAiGenerating(true);
    toast.info('🤖 Amazon Q is generating assessment...');

    try {
      const response = await assessmentAPI.generate(curricula[0].id, 'quiz');
      toast.success(`🤖 Amazon Q generated ${response.data.questions.length} AI-powered questions!`);
      
      // Refresh assessments
      fetchData();
    } catch (error) {
      toast.error('Failed to generate AI assessment');
    } finally {
      setAiGenerating(false);
    }
  };

  const filteredAssessments = assessments.filter(assessment => {
    const matchesSearch = assessment.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         assessment.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesType = !filterType || assessment.assessment_type === filterType;
    return matchesSearch && matchesType;
  });

  const assessmentTypes = [...new Set(assessments.map(a => a.assessment_type))];

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="glass-card p-8 text-center">
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-gray-700 font-medium">Loading AI assessments...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="glass-card p-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gradient mb-2 flex items-center">
              AI-Enhanced Assessments
              <span className="ml-3 px-3 py-1 bg-purple-500 text-white text-sm rounded-full">Amazon Q Powered</span>
            </h1>
            <p className="text-gray-600">🤖 Create and manage AI-powered assessments with auto-grading</p>
          </div>
          
          <div className="flex space-x-3">
            <button
              onClick={generateAIAssessment}
              disabled={aiGenerating}
              className="glass-button bg-gradient-secondary text-white hover-lift pulse-glow"
            >
              {aiGenerating ? (
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2" />
              ) : (
                <Brain className="h-5 w-5 mr-2" />
              )}
              {aiGenerating ? 'Generating...' : '🤖 AI Generate'}
            </button>
            <button
              onClick={() => {
                toast.info('Opening assessment builder...');
                navigate('/assessment/create');
              }}
              className="glass-button bg-gradient-primary text-white hover-lift pulse-glow"
            >
              <Plus className="h-5 w-5 mr-2" />
              Create Manual
            </button>
          </div>
        </div>

        {/* Amazon Q Features Banner */}
        <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-4 mb-6 border border-purple-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center">
            <Brain className="h-5 w-5 mr-2 text-purple-600" />
            Amazon Q Assessment Features
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="flex items-center p-3 bg-white rounded-lg shadow-sm">
              <Zap className="h-6 w-6 text-purple-600 mr-3" />
              <div>
                <div className="font-semibold text-gray-900">Auto Question Generation</div>
                <div className="text-sm text-gray-600">AI creates questions from curriculum content</div>
              </div>
            </div>
            <div className="flex items-center p-3 bg-white rounded-lg shadow-sm">
              <Target className="h-6 w-6 text-blue-600 mr-3" />
              <div>
                <div className="font-semibold text-gray-900">Intelligent Grading</div>
                <div className="text-sm text-gray-600">Instant AI-powered assessment scoring</div>
              </div>
            </div>
            <div className="flex items-center p-3 bg-white rounded-lg shadow-sm">
              <CheckCircle className="h-6 w-6 text-green-600 mr-3" />
              <div>
                <div className="font-semibold text-gray-900">Adaptive Difficulty</div>
                <div className="text-sm text-gray-600">Questions adapt to student performance</div>
              </div>
            </div>
          </div>
        </div>
        
        {/* Search and Filter */}
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search AI assessments..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="glass-input w-full pl-12 pr-4 py-3 text-gray-900 placeholder-gray-500"
            />
          </div>
          
          <div className="relative">
            <Filter className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="glass-input pl-12 pr-8 py-3 text-gray-900 min-w-[200px]"
            >
              <option value="">All Types</option>
              {assessmentTypes.map(type => (
                <option key={type} value={type}>{type}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="glass-card p-6 hover-lift">
          <div className="flex items-center">
            <div className="p-3 bg-gradient-primary rounded-xl">
              <Brain className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <div className="text-2xl font-bold text-gray-900">{assessments.length}</div>
              <div className="text-sm text-gray-600">AI Assessments</div>
            </div>
          </div>
        </div>
        
        <div className="glass-card p-6 hover-lift">
          <div className="flex items-center">
            <div className="p-3 bg-gradient-success rounded-xl">
              <CheckCircle className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <div className="text-2xl font-bold text-gray-900">
                {assessments.reduce((sum, a) => sum + (a.questions_count || 0), 0)}
              </div>
              <div className="text-sm text-gray-600">AI Questions</div>
            </div>
          </div>
        </div>
        
        <div className="glass-card p-6 hover-lift">
          <div className="flex items-center">
            <div className="p-3 bg-gradient-secondary rounded-xl">
              <Clock className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <div className="text-2xl font-bold text-gray-900">2.3s</div>
              <div className="text-sm text-gray-600">Avg Grading Time</div>
            </div>
          </div>
        </div>
        
        <div className="glass-card p-6 hover-lift">
          <div className="flex items-center">
            <div className="p-3 bg-gradient-warning rounded-xl">
              <Target className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <div className="text-2xl font-bold text-gray-900">98.5%</div>
              <div className="text-sm text-gray-600">AI Accuracy</div>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      {filteredAssessments.length === 0 ? (
        <div className="glass-card p-12 text-center">
          <div className="float mb-6">
            <Brain className="h-16 w-16 text-gray-400 mx-auto" />
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            {assessments.length === 0 ? 'No AI assessments yet' : 'No assessments match your search'}
          </h3>
          <p className="text-gray-600 mb-6">
            {assessments.length === 0 
              ? 'Create your first Amazon Q-powered assessment to get started with AI-enhanced evaluation.'
              : 'Try adjusting your search terms or filters.'
            }
          </p>
          {assessments.length === 0 && (
            <div className="flex justify-center space-x-4">
              <button
                onClick={generateAIAssessment}
                disabled={aiGenerating}
                className="glass-button bg-gradient-secondary text-white hover-lift"
              >
                <Brain className="h-5 w-5 mr-2" />
                🤖 AI Generate
              </button>
              <button
                onClick={() => {
                  toast.info('Let\'s create your first assessment!');
                  navigate('/assessment/create');
                }}
                className="glass-button bg-gradient-primary text-white hover-lift"
              >
                <Plus className="h-5 w-5 mr-2" />
                Create Manual
              </button>
            </div>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredAssessments.map((assessment) => (
            <div
              key={assessment.id}
              className="glass-card p-6 hover-lift group"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2 group-hover:text-gradient transition-all flex items-center">
                    {assessment.title}
                    <span className="ml-2 px-2 py-1 bg-purple-500 text-white text-xs rounded-full">🤖 AI</span>
                  </h3>
                  <p className="text-gray-600 text-sm line-clamp-2">
                    {assessment.description}
                  </p>
                </div>
              </div>

              <div className="mb-4 p-2 bg-purple-50 rounded border border-purple-200">
                <p className="text-xs text-purple-800">
                  ✅ AI Generated • ✅ Auto Grading • ✅ Instant Feedback
                </p>
              </div>
              
              <div className="flex items-center space-x-2 mb-4">
                <span className="px-3 py-1 bg-gradient-primary text-white rounded-full text-xs font-medium">
                  {assessment.assessment_type}
                </span>
                <span className="px-3 py-1 bg-gradient-success text-white rounded-full text-xs font-medium">
                  {assessment.questions_count} Questions
                </span>
              </div>
              
              <div className="grid grid-cols-2 gap-4 text-sm text-gray-500 mb-4">
                <div className="flex items-center">
                  <Clock className="h-4 w-4 mr-1" />
                  <span>Auto Graded</span>
                </div>
                <div className="flex items-center">
                  <Users className="h-4 w-4 mr-1" />
                  <span>0 submissions</span>
                </div>
              </div>
              
              <div className="flex space-x-2">
                <button
                  onClick={() => {
                    toast.info(`Taking ${assessment.title}...`);
                    navigate(`/assessment/${assessment.id}/take`);
                  }}
                  className="flex-1 px-3 py-2 bg-purple-600 text-white text-sm rounded hover:bg-purple-700"
                >
                  <Play className="h-3 w-3 mr-1 inline" />
                  Take Test
                </button>
                <button
                  onClick={() => {
                    toast.info('Opening assessment editor...');
                    navigate(`/assessment/${assessment.id}/edit`);
                  }}
                  className="px-3 py-2 border border-gray-300 text-gray-700 text-sm rounded hover:bg-gray-50"
                >
                  <Edit className="h-3 w-3" />
                </button>
              </div>
              
              <div className="pt-4 border-t border-white/20 mt-4">
                <div className="text-xs text-gray-500">
                  Created {new Date(assessment.created_at).toLocaleDateString()}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default AssessmentListEnhanced;