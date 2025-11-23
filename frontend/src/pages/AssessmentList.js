import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { assessmentAPI, curriculumAPI } from '../services/api';
import { toast } from 'react-toastify';
import { FileText, Plus, Search, Filter, Clock, Users, Target, Play, Eye, BarChart3, Sparkles, Zap } from 'lucide-react';

const AssessmentList = () => {
  const navigate = useNavigate();
  const [assessments, setAssessments] = useState([]);
  const [curricula, setCurricula] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('');
  const [filterCurriculum, setFilterCurriculum] = useState('');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      
      // Fetch curricula for filter options
      const curriculaResponse = await curriculumAPI.getAll();
      setCurricula(curriculaResponse.data);
      
      // Mock assessments data (replace with real API call)
      const mockAssessments = [
        {
          id: 1,
          title: 'Python Fundamentals Quiz',
          description: 'Basic concepts and syntax assessment',
          assessment_type: 'quiz',
          curriculum_id: 1,
          curriculum_title: 'Python Programming Basics',
          total_points: 50,
          time_limit: 30,
          questions_count: 15,
          attempts_count: 23,
          average_score: 78.5,
          created_at: '2024-01-15T10:00:00Z',
          status: 'active'
        },
        {
          id: 2,
          title: 'Advanced Python Test',
          description: 'Comprehensive evaluation of advanced concepts',
          assessment_type: 'test',
          curriculum_id: 1,
          curriculum_title: 'Python Programming Basics',
          total_points: 100,
          time_limit: 90,
          questions_count: 25,
          attempts_count: 12,
          average_score: 82.3,
          created_at: '2024-01-20T14:30:00Z',
          status: 'active'
        },
        {
          id: 3,
          title: 'Algebra Midterm Exam',
          description: 'Mid-semester algebra assessment',
          assessment_type: 'exam',
          curriculum_id: 2,
          curriculum_title: 'Algebra Fundamentals',
          total_points: 150,
          time_limit: 120,
          questions_count: 30,
          attempts_count: 45,
          average_score: 75.8,
          created_at: '2024-01-18T09:00:00Z',
          status: 'active'
        }
      ];
      
      setAssessments(mockAssessments);
      toast.success('Assessments loaded successfully');
      
    } catch (error) {
      console.error('Failed to fetch assessments:', error);
      toast.error('Failed to load assessments. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateAssessment = () => {
    toast.info('Opening assessment builder...');
    navigate('/assessments/create');
  };

  const handleTakeAssessment = (assessment) => {
    toast.info(`Starting ${assessment.title}...`);
    navigate(`/assessment/${assessment.id}`);
  };

  const handleViewResults = (assessment) => {
    toast.info('Loading assessment analytics...');
    navigate(`/assessments/${assessment.id}/results`);
  };

  const handleEditAssessment = (assessment) => {
    toast.info(`Opening ${assessment.title} editor...`);
    navigate(`/assessments/${assessment.id}/edit`);
  };

  const handleGenerateAssessment = async (curriculumId) => {
    try {
      toast.info('AI is generating questions...', { autoClose: 6000 });
      await assessmentAPI.generate(curriculumId, 'mixed');
      toast.success('Assessment generated successfully!');
      fetchData();
    } catch (error) {
      toast.error('Failed to generate assessment. Please try again.');
    }
  };

  const filteredAssessments = assessments.filter(assessment => {
    const matchesSearch = assessment.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         assessment.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesType = !filterType || assessment.assessment_type === filterType;
    const matchesCurriculum = !filterCurriculum || assessment.curriculum_id.toString() === filterCurriculum;
    return matchesSearch && matchesType && matchesCurriculum;
  });

  const assessmentTypes = [...new Set(assessments.map(a => a.assessment_type))];

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="glass-card p-8 text-center">
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-gray-700 font-medium">Loading assessments...</p>
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
            <h1 className="text-3xl font-bold text-gradient mb-2">Assessments</h1>
            <p className="text-gray-600">Create, manage, and analyze student assessments</p>
          </div>
          
          <button
            onClick={handleCreateAssessment}
            className="glass-button bg-gradient-primary text-white hover-lift pulse-glow"
          >
            <Plus className="h-5 w-5 mr-2" />
            Create Assessment
          </button>
        </div>
        
        {/* Search and Filters */}
        <div className="flex flex-col lg:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search assessments..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="glass-input w-full pl-12 pr-4 py-3 text-gray-900 placeholder-gray-500"
            />
          </div>
          
          <div className="flex gap-4">
            <div className="relative">
              <Filter className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <select
                value={filterType}
                onChange={(e) => setFilterType(e.target.value)}
                className="glass-input pl-12 pr-8 py-3 text-gray-900 min-w-[150px]"
              >
                <option value="">All Types</option>
                {assessmentTypes.map(type => (
                  <option key={type} value={type}>{type.charAt(0).toUpperCase() + type.slice(1)}</option>
                ))}
              </select>
            </div>
            
            <div className="relative">
              <select
                value={filterCurriculum}
                onChange={(e) => setFilterCurriculum(e.target.value)}
                className="glass-input pl-4 pr-8 py-3 text-gray-900 min-w-[200px]"
              >
                <option value="">All Curricula</option>
                {curricula.map(curriculum => (
                  <option key={curriculum.id} value={curriculum.id}>{curriculum.title}</option>
                ))}
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="glass-card p-6 hover-lift">
          <div className="flex items-center">
            <div className="p-3 bg-gradient-primary rounded-xl">
              <FileText className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <div className="text-2xl font-bold text-gray-900">{assessments.length}</div>
              <div className="text-sm text-gray-600">Total Assessments</div>
            </div>
          </div>
        </div>
        
        <div className="glass-card p-6 hover-lift">
          <div className="flex items-center">
            <div className="p-3 bg-gradient-success rounded-xl">
              <Users className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <div className="text-2xl font-bold text-gray-900">
                {assessments.reduce((sum, a) => sum + a.attempts_count, 0)}
              </div>
              <div className="text-sm text-gray-600">Total Attempts</div>
            </div>
          </div>
        </div>
        
        <div className="glass-card p-6 hover-lift">
          <div className="flex items-center">
            <div className="p-3 bg-gradient-secondary rounded-xl">
              <Target className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <div className="text-2xl font-bold text-gray-900">
                {Math.round(assessments.reduce((sum, a) => sum + a.average_score, 0) / assessments.length) || 0}%
              </div>
              <div className="text-sm text-gray-600">Average Score</div>
            </div>
          </div>
        </div>
        
        <div className="glass-card p-6 hover-lift">
          <div className="flex items-center">
            <div className="p-3 bg-gradient-warning rounded-xl">
              <Clock className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <div className="text-2xl font-bold text-gray-900">
                {Math.round(assessments.reduce((sum, a) => sum + a.time_limit, 0) / assessments.length) || 0}
              </div>
              <div className="text-sm text-gray-600">Avg Duration (min)</div>
            </div>
          </div>
        </div>
      </div>

      {/* Assessments Grid */}
      {filteredAssessments.length === 0 ? (
        <div className="glass-card p-12 text-center">
          <div className="float mb-6">
            <FileText className="h-16 w-16 text-gray-400 mx-auto" />
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            {assessments.length === 0 ? 'No assessments yet' : 'No assessments match your search'}
          </h3>
          <p className="text-gray-600 mb-6">
            {assessments.length === 0 
              ? 'Create your first assessment to get started.'
              : 'Try adjusting your search terms or filters.'
            }
          </p>
          {assessments.length === 0 && (
            <button
              onClick={handleCreateAssessment}
              className="glass-button bg-gradient-primary text-white hover-lift"
            >
              <Sparkles className="h-5 w-5 mr-2" />
              Create First Assessment
            </button>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredAssessments.map((assessment) => (
            <div key={assessment.id} className="glass-card p-6 hover-lift group">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2 group-hover:text-gradient transition-all">
                    {assessment.title}
                  </h3>
                  <p className="text-gray-600 text-sm line-clamp-2">
                    {assessment.description}
                  </p>
                </div>
              </div>
              
              <div className="flex items-center space-x-2 mb-4">
                <span className={`px-3 py-1 rounded-full text-xs font-medium text-white ${
                  assessment.assessment_type === 'quiz' ? 'bg-gradient-primary' :
                  assessment.assessment_type === 'test' ? 'bg-gradient-success' :
                  'bg-gradient-secondary'
                }`}>
                  {assessment.assessment_type.charAt(0).toUpperCase() + assessment.assessment_type.slice(1)}
                </span>
                <span className="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-xs">
                  {assessment.curriculum_title}
                </span>
              </div>
              
              <div className="grid grid-cols-3 gap-4 text-sm text-gray-500 mb-4">
                <div className="flex items-center">
                  <Clock className="h-4 w-4 mr-1" />
                  <span>{assessment.time_limit}min</span>
                </div>
                <div className="flex items-center">
                  <Target className="h-4 w-4 mr-1" />
                  <span>{assessment.questions_count} questions</span>
                </div>
                <div className="flex items-center">
                  <Users className="h-4 w-4 mr-1" />
                  <span>{assessment.attempts_count} attempts</span>
                </div>
              </div>
              
              <div className="mb-4">
                <div className="flex justify-between text-sm text-gray-600 mb-1">
                  <span>Average Score</span>
                  <span>{assessment.average_score}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-gradient-primary h-2 rounded-full transition-all duration-500" 
                    style={{ width: `${assessment.average_score}%` }}
                  ></div>
                </div>
              </div>
              
              <div className="flex space-x-2">
                <button
                  onClick={() => handleTakeAssessment(assessment)}
                  className="flex-1 glass-button bg-gradient-primary text-white text-sm"
                >
                  <Play className="h-4 w-4 mr-1" />
                  Take
                </button>
                <button
                  onClick={() => handleViewResults(assessment)}
                  className="flex-1 glass-button bg-gradient-success text-white text-sm"
                >
                  <BarChart3 className="h-4 w-4 mr-1" />
                  Results
                </button>
                <button
                  onClick={() => handleEditAssessment(assessment)}
                  className="flex-1 glass-button bg-gradient-secondary text-white text-sm"
                >
                  <Eye className="h-4 w-4 mr-1" />
                  Edit
                </button>
              </div>
              
              <div className="mt-4 pt-4 border-t border-white/20">
                <div className="text-xs text-gray-500">
                  Created {new Date(assessment.created_at).toLocaleDateString()}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Quick Actions */}
      {curricula.length > 0 && (
        <div className="glass-card p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <Zap className="h-5 w-5 mr-2 text-yellow-500" />
            AI Quick Actions
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {curricula.slice(0, 3).map(curriculum => (
              <button
                key={curriculum.id}
                onClick={() => handleGenerateAssessment(curriculum.id)}
                className="glass-card p-4 hover-lift text-left group"
              >
                <div className="flex items-center mb-2">
                  <Sparkles className="h-5 w-5 text-purple-500 mr-2" />
                  <div className="font-medium text-gray-900 group-hover:text-gradient transition-all">
                    Generate Assessment
                  </div>
                </div>
                <div className="text-sm text-gray-600">for {curriculum.title}</div>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default AssessmentList;