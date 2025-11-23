import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ModuleCard from '../components/ModuleCard';
import AssessmentCard from '../components/AssessmentCard';
import ExportOptions from '../components/ExportOptions';
import { useToast } from '../components/Toast';
import { curriculumAPI, assessmentAPI } from '../services/api';
import { BookOpen, Target, Calendar, Users, Plus, ArrowLeft } from 'lucide-react';

const CurriculumPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const toast = useToast();
  const [curriculum, setCurriculum] = useState(null);
  const [modules, setModules] = useState([]);
  const [assessments, setAssessments] = useState([]);
  const [expandedModules, setExpandedModules] = useState({});
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      fetchCurriculumData();
    }
  }, [id]);

  const fetchCurriculumData = async () => {
    try {
      setLoading(true);
      
      // Fetch curriculum details
      const curriculumResponse = await curriculumAPI.getById(id);
      setCurriculum(curriculumResponse.data);
      
      // Extract modules from curriculum metadata
      const weeklyModules = curriculumResponse.data.metadata?.weekly_modules || [];
      const allModules = [];
      
      weeklyModules.forEach((week, weekIndex) => {
        week.content_blocks?.forEach((block, blockIndex) => {
          allModules.push({
            ...block,
            id: `${weekIndex}-${blockIndex}`,
            week_number: week.week_number,
            sequence_order: blockIndex + 1,
            learning_outcomes: week.learning_outcomes || []
          });
        });
      });
      
      setModules(allModules);
      
      // Fetch assessments (mock data for now)
      setAssessments([
        {
          id: 1,
          title: 'Week 1 Knowledge Check',
          description: 'Assessment covering basic concepts',
          assessment_type: 'quiz',
          total_points: 50,
          time_limit: 30,
          questions: Array(10).fill({}),
          attempts_count: 0
        },
        {
          id: 2,
          title: 'Mid-Course Evaluation',
          description: 'Comprehensive assessment of learning progress',
          assessment_type: 'test',
          total_points: 100,
          time_limit: 60,
          questions: Array(20).fill({}),
          attempts_count: 0
        }
      ]);
      
    } catch (error) {
      console.error('Failed to fetch curriculum data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleModuleToggle = (moduleId) => {
    setExpandedModules(prev => ({
      ...prev,
      [moduleId]: !prev[moduleId]
    }));
  };

  const handleModuleStart = async (module) => {
    console.log('Starting module:', module);
    toast.info('Module started', `Beginning ${module.title}`);
    // Implement module start logic
  };

  const handleAssessmentTake = async (assessment) => {
    console.log('Taking assessment:', assessment);
    toast.info('Starting assessment', `Navigating to ${assessment.title}`);
    // Navigate to assessment page
    navigate(`/assessment/${assessment.id}`);
  };

  const handleAssessmentView = (assessment) => {
    console.log('Viewing assessment:', assessment);
    // Navigate to assessment details
  };

  const handleGenerateAssessment = async () => {
    try {
      toast.info('Generating assessment', 'This may take a few moments...');
      const response = await assessmentAPI.generate(id, 'mixed');
      console.log('Generated assessment:', response.data);
      toast.success('Assessment generated successfully', 'New assessment has been added to your curriculum');
      // Refresh assessments
      fetchCurriculumData();
    } catch (error) {
      console.error('Failed to generate assessment:', error);
      toast.error('Failed to generate assessment', 'Please try again later');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!curriculum) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Curriculum Not Found</h2>
          <p className="text-gray-600 mb-4">The curriculum you're looking for doesn't exist.</p>
          <button
            onClick={() => navigate('/curriculum')}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Back to Curricula
          </button>
        </div>
      </div>
    );
  }

  const weeklyModules = curriculum.metadata?.weekly_modules || [];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/curriculum')}
                className="p-2 text-gray-400 hover:text-gray-600 rounded-full hover:bg-gray-100"
              >
                <ArrowLeft className="h-5 w-5" />
              </button>
              
              <div>
                <h1 className="text-2xl font-bold text-gray-900">{curriculum.title}</h1>
                <p className="text-gray-600 mt-1">{curriculum.description}</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-3">
              <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                {curriculum.subject}
              </span>
              <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                {curriculum.grade_level}
              </span>
            </div>
          </div>
          
          {/* Curriculum Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mt-6">
            <div className="bg-blue-50 rounded-lg p-4">
              <div className="flex items-center">
                <BookOpen className="h-6 w-6 text-blue-600 mr-2" />
                <div>
                  <div className="text-lg font-semibold text-blue-900">{weeklyModules.length}</div>
                  <div className="text-sm text-blue-700">Weeks</div>
                </div>
              </div>
            </div>
            
            <div className="bg-green-50 rounded-lg p-4">
              <div className="flex items-center">
                <Target className="h-6 w-6 text-green-600 mr-2" />
                <div>
                  <div className="text-lg font-semibold text-green-900">{modules.length}</div>
                  <div className="text-sm text-green-700">Modules</div>
                </div>
              </div>
            </div>
            
            <div className="bg-purple-50 rounded-lg p-4">
              <div className="flex items-center">
                <Calendar className="h-6 w-6 text-purple-600 mr-2" />
                <div>
                  <div className="text-lg font-semibold text-purple-900">{assessments.length}</div>
                  <div className="text-sm text-purple-700">Assessments</div>
                </div>
              </div>
            </div>
            
            <div className="bg-orange-50 rounded-lg p-4">
              <div className="flex items-center">
                <Users className="h-6 w-6 text-orange-600 mr-2" />
                <div>
                  <div className="text-lg font-semibold text-orange-900">0</div>
                  <div className="text-sm text-orange-700">Students</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4">
          <nav className="flex space-x-8">
            {[
              { id: 'overview', label: 'Overview' },
              { id: 'modules', label: 'Learning Modules' },
              { id: 'assessments', label: 'Assessments' },
              { id: 'export', label: 'Export & Share' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="space-y-8">
            {/* Learning Objectives */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Learning Objectives</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {curriculum.metadata?.learning_objectives?.map((objective, index) => (
                  <div key={index} className="flex items-start space-x-3">
                    <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                      <span className="text-blue-600 text-sm font-medium">{index + 1}</span>
                    </div>
                    <p className="text-gray-700">{objective}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Weekly Overview */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Weekly Overview</h2>
              <div className="space-y-4">
                {weeklyModules.map((week, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="text-lg font-medium text-gray-900">
                        Week {week.week_number}: {week.title}
                      </h3>
                      <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-sm">
                        {week.bloom_focus}
                      </span>
                    </div>
                    <p className="text-gray-600 mb-3">{week.description}</p>
                    <div className="text-sm text-gray-500">
                      {week.content_blocks?.length || 0} modules • 
                      {week.content_blocks?.reduce((total, block) => total + (block.estimated_duration || 0), 0)} minutes total
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Modules Tab */}
        {activeTab === 'modules' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-gray-900">Learning Modules</h2>
              <span className="text-gray-600">{modules.length} modules total</span>
            </div>
            
            {weeklyModules.map((week) => (
              <div key={week.week_number} className="space-y-4">
                <h3 className="text-xl font-semibold text-gray-900 border-b border-gray-200 pb-2">
                  Week {week.week_number}: {week.title}
                </h3>
                
                <div className="space-y-4">
                  {week.content_blocks?.map((block, blockIndex) => {
                    const moduleId = `${week.week_number}-${blockIndex}`;
                    return (
                      <ModuleCard
                        key={moduleId}
                        module={{
                          ...block,
                          id: moduleId,
                          learning_outcomes: week.learning_outcomes
                        }}
                        weekNumber={week.week_number}
                        isExpanded={expandedModules[moduleId]}
                        onToggle={() => handleModuleToggle(moduleId)}
                        onStart={handleModuleStart}
                      />
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Assessments Tab */}
        {activeTab === 'assessments' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-gray-900">Assessments</h2>
              <button
                onClick={handleGenerateAssessment}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                <Plus className="h-4 w-4" />
                <span>Generate Assessment</span>
              </button>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {assessments.map((assessment) => (
                <AssessmentCard
                  key={assessment.id}
                  assessment={assessment}
                  onTake={handleAssessmentTake}
                  onView={handleAssessmentView}
                />
              ))}
            </div>
            
            {assessments.length === 0 && (
              <div className="text-center py-12">
                <div className="text-gray-400 text-6xl mb-4">📝</div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">No Assessments Yet</h3>
                <p className="text-gray-600 mb-4">Generate AI-powered assessments for this curriculum.</p>
                <button
                  onClick={handleGenerateAssessment}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  Generate First Assessment
                </button>
              </div>
            )}
          </div>
        )}

        {/* Export Tab */}
        {activeTab === 'export' && (
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Export & Share</h2>
            <ExportOptions 
              curriculumId={curriculum.id} 
              curriculumTitle={curriculum.title} 
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default CurriculumPage;