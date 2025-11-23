import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { curriculumAPI } from '../services/api';
import { useToast } from '../components/Toast';
import { BookOpen, Plus, Search, Filter, Calendar, Users, Target } from 'lucide-react';

const CurriculumList = () => {
  const navigate = useNavigate();
  const toast = useToast();
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
      const response = await curriculumAPI.getAll();
      setCurricula(response.data);
      toast.success('Curricula loaded successfully');
    } catch (error) {
      console.error('Failed to fetch curricula:', error);
      toast.error('Failed to load curricula', 'Please try again later');
    } finally {
      setLoading(false);
    }
  };

  const filteredCurricula = curricula.filter(curriculum => {
    const matchesSearch = curriculum.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         curriculum.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesSubject = !filterSubject || curriculum.subject === filterSubject;
    return matchesSearch && matchesSubject;
  });

  const subjects = [...new Set(curricula.map(c => c.subject))];

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Curricula</h1>
              <p className="text-gray-600 mt-1">Manage your educational content and learning paths</p>
            </div>
            
            <button
              onClick={() => navigate('/curriculum/create')}
              className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              <Plus className="h-4 w-4" />
              <span>Create Curriculum</span>
            </button>
          </div>
          
          {/* Search and Filter */}
          <div className="flex items-center space-x-4 mt-6">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search curricula..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <div className="relative">
              <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <select
                value={filterSubject}
                onChange={(e) => setFilterSubject(e.target.value)}
                className="pl-10 pr-8 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">All Subjects</option>
                {subjects.map(subject => (
                  <option key={subject} value={subject}>{subject}</option>
                ))}
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        {filteredCurricula.length === 0 ? (
          <div className="text-center py-12">
            <BookOpen className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              {curricula.length === 0 ? 'No curricula yet' : 'No curricula match your search'}
            </h3>
            <p className="text-gray-600 mb-4">
              {curricula.length === 0 
                ? 'Create your first curriculum to get started with EdweavePack.'
                : 'Try adjusting your search terms or filters.'
              }
            </p>
            {curricula.length === 0 && (
              <button
                onClick={() => navigate('/curriculum/create')}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                Create First Curriculum
              </button>
            )}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredCurricula.map((curriculum) => (
              <div
                key={curriculum.id}
                className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow cursor-pointer"
                onClick={() => navigate(`/curriculum/${curriculum.id}`)}
              >
                <div className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">
                        {curriculum.title}
                      </h3>
                      <p className="text-gray-600 text-sm line-clamp-2">
                        {curriculum.description}
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-4 mb-4">
                    <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs font-medium">
                      {curriculum.subject}
                    </span>
                    <span className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs font-medium">
                      {curriculum.grade_level}
                    </span>
                  </div>
                  
                  <div className="grid grid-cols-3 gap-4 text-sm text-gray-500">
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
                  
                  <div className="mt-4 pt-4 border-t border-gray-200">
                    <div className="text-xs text-gray-500">
                      Created {new Date(curriculum.created_at).toLocaleDateString()}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default CurriculumList;