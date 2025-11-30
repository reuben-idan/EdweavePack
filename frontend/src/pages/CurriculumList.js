import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { curriculumAPI } from '../services/api';
import { toast } from 'react-toastify';
import { BookOpen, Plus, Search, Filter, Calendar, Users, Target, Sparkles } from 'lucide-react';

const CurriculumList = () => {
  const navigate = useNavigate();
  const [curricula, setCurricula] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterSubject, setFilterSubject] = useState('');

  useEffect(() => {
    fetchCurricula();
  }, []);

  const fetchCurricula = async () => {
    try {
      setLoading(true);
      const response = await curriculumAPI.getCurricula();
      setCurricula(response.data.curricula || []);
      toast.success('AI-enhanced curricula loaded successfully');
    } catch (error) {
      console.error('Failed to fetch curricula:', error);
      toast.error('Failed to load curricula. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const filteredCurricula = (Array.isArray(curricula) ? curricula : []).filter(curriculum => {
    const matchesSearch = curriculum.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         curriculum.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesSubject = !filterSubject || curriculum.subject === filterSubject;
    return matchesSearch && matchesSubject;
  });

  const subjects = [...new Set((Array.isArray(curricula) ? curricula : []).map(c => c.subject))];

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="glass-card p-8 text-center">
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-gray-700 font-medium">Loading curricula...</p>
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
              AI-Enhanced Curricula
              <span className="ml-3 px-3 py-1 bg-blue-500 text-white text-sm rounded-full">Amazon Q Powered</span>
            </h1>
            <p className="text-gray-600">🤖 Manage your AI-powered educational content with adaptive learning paths</p>
          </div>
          
          <div className="flex space-x-3">
            <button
              onClick={() => {
                toast.info('Opening AI upload wizard...');
                navigate('/upload');
              }}
              className="glass-button bg-gradient-secondary text-white hover-lift pulse-glow"
            >
              <Sparkles className="h-5 w-5 mr-2" />
              AI Upload
            </button>
            <button
              onClick={() => {
                toast.info('Opening curriculum builder...');
                navigate('/curriculum/create');
              }}
              className="glass-button bg-gradient-primary text-white hover-lift pulse-glow"
            >
              <Plus className="h-5 w-5 mr-2" />
              Create Manual
            </button>
          </div>
        </div>
        
        {/* Search and Filter */}
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search AI-enhanced curricula..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="glass-input w-full pl-12 pr-4 py-3 text-gray-900 placeholder-gray-500"
            />
          </div>
          
          <div className="relative">
            <Filter className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <select
              value={filterSubject}
              onChange={(e) => setFilterSubject(e.target.value)}
              className="glass-input pl-12 pr-8 py-3 text-gray-900 min-w-[200px]"
            >
              <option value="">All Subjects</option>
              {subjects.map(subject => (
                <option key={subject} value={subject}>{subject}</option>
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
              <BookOpen className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <div className="text-2xl font-bold text-gray-900">{Array.isArray(curricula) ? curricula.length : 0}</div>
              <div className="text-sm text-gray-600">Total Curricula</div>
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
                {(Array.isArray(curricula) ? curricula : []).reduce((sum, c) => sum + (c.metadata?.learning_objectives?.length || 0), 0)}
              </div>
              <div className="text-sm text-gray-600">Learning Objectives</div>
            </div>
          </div>
        </div>
        
        <div className="glass-card p-6 hover-lift">
          <div className="flex items-center">
            <div className="p-3 bg-gradient-secondary rounded-xl">
              <Calendar className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <div className="text-2xl font-bold text-gray-900">
                {(Array.isArray(curricula) ? curricula : []).reduce((sum, c) => sum + (c.metadata?.weekly_modules?.length || 0), 0)}
              </div>
              <div className="text-sm text-gray-600">Total Weeks</div>
            </div>
          </div>
        </div>
        
        <div className="glass-card p-6 hover-lift">
          <div className="flex items-center">
            <div className="p-3 bg-gradient-warning rounded-xl">
              <Users className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <div className="text-2xl font-bold text-gray-900">0</div>
              <div className="text-sm text-gray-600">Active Students</div>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      {filteredCurricula.length === 0 ? (
        <div className="glass-card p-12 text-center">
          <div className="float mb-6">
            <BookOpen className="h-16 w-16 text-gray-400 mx-auto" />
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            {!Array.isArray(curricula) || curricula.length === 0 ? 'No AI curricula yet' : 'No curricula match your search'}
          </h3>
          <p className="text-gray-600 mb-6">
            {!Array.isArray(curricula) || curricula.length === 0 
              ? 'Create your first Amazon Q-powered curriculum to get started with AI-enhanced education.'
              : 'Try adjusting your search terms or filters.'
            }
          </p>
          {(!Array.isArray(curricula) || curricula.length === 0) && (
            <div className="flex justify-center space-x-4">
              <button
                onClick={() => {
                  toast.info('Starting AI curriculum generation...');
                  navigate('/upload');
                }}
                className="glass-button bg-gradient-secondary text-white hover-lift"
              >
                <Sparkles className="h-5 w-5 mr-2" />
                🤖 AI Generate
              </button>
              <button
                onClick={() => {
                  toast.info('Let\'s create your first curriculum!');
                  navigate('/curriculum/create');
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
          {filteredCurricula.map((curriculum) => (
            <div
              key={curriculum.id}
              className="glass-card p-6 hover-lift cursor-pointer group"
              onClick={() => {
                toast.info(`Opening ${curriculum.title}...`);
                navigate(`/curriculum/${curriculum.id}`);
              }}
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2 group-hover:text-gradient transition-all flex items-center">
                    {curriculum.title}
                    {curriculum.amazon_q_powered && (
                      <span className="ml-2 px-2 py-1 bg-blue-500 text-white text-xs rounded-full">🤖</span>
                    )}
                  </h3>
                  <p className="text-gray-600 text-sm line-clamp-2">
                    {curriculum.description}
                  </p>
                </div>
              </div>
              
              {curriculum.ai_enhanced && (
                <div className="mb-4 p-2 bg-blue-50 rounded border border-blue-200">
                  <p className="text-xs text-blue-800">
                    ✅ AI Content Analysis • ✅ Adaptive Learning • ✅ Auto Assessment
                  </p>
                </div>
              )}
              
              <div className="flex items-center space-x-2 mb-4">
                <span className="px-3 py-1 bg-gradient-primary text-white rounded-full text-xs font-medium">
                  {curriculum.subject}
                </span>
                <span className="px-3 py-1 bg-gradient-success text-white rounded-full text-xs font-medium">
                  {curriculum.grade_level}
                </span>
              </div>
              
              <div className="grid grid-cols-3 gap-4 text-sm text-gray-500 mb-4">
                <div className="flex items-center">
                  <Calendar className="h-4 w-4 mr-1" />
                  <span>{curriculum.metadata?.weekly_modules?.length || 0} weeks</span>
                </div>
                <div className="flex items-center">
                  <Target className="h-4 w-4 mr-1" />
                  <span>{curriculum.metadata?.learning_objectives?.length || 0} objectives</span>
                </div>
                <div className="flex items-center">
                  <Users className="h-4 w-4 mr-1" />
                  <span>0 students</span>
                </div>
              </div>
              
              <div className="pt-4 border-t border-white/20">
                <div className="text-xs text-gray-500">
                  Created {new Date(curriculum.created_at).toLocaleDateString()}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CurriculumList;