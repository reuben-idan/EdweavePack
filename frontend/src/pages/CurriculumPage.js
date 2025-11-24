import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import ModuleCard from '../components/ModuleCard';
import AssessmentCard from '../components/AssessmentCard';
import ExportOptions from '../components/ExportOptions';
import { curriculumAPI, assessmentAPI } from '../services/api';
import { BookOpen, Target, Calendar, Users, Plus, ArrowLeft, Sparkles } from 'lucide-react';

const CurriculumPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
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
      
      // Mock curriculum with generated modules from uploaded content
      const mockCurriculum = {
        id: id,
        title: "Curriculum from Uploaded Materials",
        description: "Generated from your uploaded content",
        subject: "Content-Based Learning",
        grade_level: "Intermediate",
        metadata: {
          weekly_modules: [
            {
              week_number: 1,
              title: "Introduction from Your Materials",
              description: "Key concepts extracted from uploaded files",
              bloom_focus: "Remember & Understand",
              learning_outcomes: [
                "Understand main concepts from uploaded content",
                "Identify key topics in your materials",
                "Recall important information from source files"
              ],
              content_blocks: [
                {
                  title: "Content Overview",
                  content_type: "lecture",
                  estimated_duration: 45,
                  description: "Introduction based on your uploaded materials",
                  content: "This module contains concepts extracted from your uploaded files. The AI has identified key themes and structured them into learning objectives."
                },
                {
                  title: "Key Concepts Identified",
                  content_type: "reading",
                  estimated_duration: 30,
                  description: "Main topics found in your content",
                  content: "Important concepts and terminology extracted from your uploaded materials for structured learning."
                }
              ]
            },
            {
              week_number: 2,
              title: "Deep Dive into Your Content",
              description: "Detailed exploration of uploaded material themes",
              bloom_focus: "Apply & Analyze",
              learning_outcomes: [
                "Apply concepts from uploaded materials",
                "Analyze relationships in your content",
                "Synthesize information from multiple sources"
              ],
              content_blocks: [
                {
                  title: "Content Analysis Activity",
                  content_type: "activity",
                  estimated_duration: 60,
                  description: "Interactive analysis of your materials",
                  content: "Hands-on activities based on the specific content you uploaded, designed to reinforce learning."
                },
                {
                  title: "Practical Applications",
                  content_type: "discussion",
                  estimated_duration: 45,
                  description: "Real-world applications of your content",
                  content: "Discussion topics and case studies derived from your uploaded materials."
                }
              ]
            }
          ],
          learning_objectives: [
            "Master key concepts from uploaded materials",
            "Apply knowledge extracted from your content",
            "Demonstrate understanding through assessments",
            "Connect theory to practical applications"
          ]
        }
      };
      
      setCurriculum(mockCurriculum);
      
      // Extract modules from curriculum metadata
      const weeklyModules = mockCurriculum.metadata?.weekly_modules || [];
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
      
      toast.success('Curriculum loaded successfully');
      
    } catch (error) {
      console.error('Failed to fetch curriculum data:', error);
      toast.error('Failed to load curriculum. Please check your connection and try again.');
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
    toast.info(`Starting ${module.title}...`);
    // Implement module start logic
  };

  const handleAssessmentTake = async (assessment) => {
    console.log('Taking assessment:', assessment);
    toast.info(`Loading ${assessment.title}...`);
    // Navigate to assessment page
    navigate(`/assessment/${assessment.id}`);
  };

  const handleAssessmentView = (assessment) => {
    console.log('Viewing assessment:', assessment);
    toast.info('Opening assessment details...');
    // Navigate to assessment details
  };

  const handleGenerateAssessment = async () => {
    try {
      toast.info('AI is generating assessment questions...', { autoClose: 6000 });
      const response = await assessmentAPI.generate(id, 'mixed');
      console.log('Generated assessment:', response.data);
      toast.success('Assessment generated successfully!');
      // Refresh assessments
      fetchCurriculumData();
    } catch (error) {
      console.error('Failed to generate assessment:', error);
      toast.error('Failed to generate assessment. Please try again.');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="glass-card p-8 text-center">
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-gray-700 font-medium">Loading curriculum...</p>
        </div>
      </div>
    );
  }

  if (!curriculum) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="glass-card p-8 text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Curriculum Not Found</h2>
          <p className="text-gray-600 mb-4">The curriculum you're looking for doesn't exist.</p>
          <button
            onClick={() => {
              navigate('/curriculum');
              toast.info('Returning to curriculum list...');
            }}
            className="glass-button bg-gradient-primary text-white"
          >
            Back to Curricula
          </button>
        </div>
      </div>
    );
  }

  const weeklyModules = curriculum.metadata?.weekly_modules || [];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="glass-card p-8">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-4">
            <button
              onClick={() => {
                navigate('/curriculum');
                toast.info('Returning to curriculum list...');
              }}
              className="glass-button p-3 hover-lift"
            >
              <ArrowLeft className="h-5 w-5" />
            </button>
            
            <div>
              <h1 className="text-3xl font-bold text-gradient mb-2">{curriculum.title}</h1>
              <p className="text-gray-600">{curriculum.description}</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            <span className="px-4 py-2 bg-gradient-primary text-white rounded-full text-sm font-medium">
              {curriculum.subject}
            </span>
            <span className="px-4 py-2 bg-gradient-success text-white rounded-full text-sm font-medium">
              {curriculum.grade_level}
            </span>
          </div>
        </div>
        
        {/* Curriculum Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="glass-card p-6 hover-lift">
            <div className="flex items-center">
              <div className="p-3 bg-gradient-primary rounded-xl">
                <BookOpen className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <div className="text-2xl font-bold text-gray-900">{weeklyModules.length}</div>
                <div className="text-sm text-gray-600">Weeks</div>
              </div>
            </div>
          </div>
          
          <div className="glass-card p-6 hover-lift">
            <div className="flex items-center">
              <div className="p-3 bg-gradient-success rounded-xl">
                <Target className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <div className="text-2xl font-bold text-gray-900">{modules.length}</div>
                <div className="text-sm text-gray-600">Modules</div>
              </div>
            </div>
          </div>
          
          <div className="glass-card p-6 hover-lift">
            <div className="flex items-center">
              <div className="p-3 bg-gradient-secondary rounded-xl">
                <Calendar className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <div className="text-2xl font-bold text-gray-900">{assessments.length}</div>
                <div className="text-sm text-gray-600">Assessments</div>
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
                <div className="text-sm text-gray-600">Students</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="glass-card p-2">
        <nav className="flex space-x-2">
          {[
            { id: 'overview', label: 'Overview' },
            { id: 'modules', label: 'Learning Modules' },
            { id: 'assessments', label: 'Assessments' },
            { id: 'export', label: 'Export & Share' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-6 py-3 rounded-xl font-medium text-sm transition-all duration-300 ${
                activeTab === tab.id
                  ? 'bg-gradient-primary text-white shadow-lg'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-white/50'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Content */}
      <div>
        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="space-y-8">
            {/* Learning Objectives */}
            <div className="glass-card p-8">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Learning Objectives</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {curriculum.metadata?.learning_objectives?.map((objective, index) => (
                  <div key={index} className="flex items-start space-x-4">
                    <div className="w-8 h-8 bg-gradient-primary rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                      <span className="text-white text-sm font-medium">{index + 1}</span>
                    </div>
                    <p className="text-gray-700 leading-relaxed">{objective}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Weekly Overview */}
            <div className="glass-card p-8">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Weekly Overview</h2>
              <div className="space-y-6">
                {weeklyModules.map((week, index) => (
                  <div key={index} className="glass-card p-6 hover-lift">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-lg font-medium text-gray-900">
                        Week {week.week_number}: {week.title}
                      </h3>
                      <span className="px-3 py-1 bg-gradient-primary text-white rounded-full text-sm">
                        {week.bloom_focus}
                      </span>
                    </div>
                    <p className="text-gray-600 mb-4">{week.description}</p>
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
          <div className="space-y-8">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-gradient">Learning Modules</h2>
              <span className="text-gray-600">{modules.length} modules total</span>
            </div>
            
            {weeklyModules.map((week) => (
              <div key={week.week_number} className="space-y-6">
                <div className="glass-card p-6">
                  <h3 className="text-xl font-semibold text-gradient mb-2">
                    Week {week.week_number}: {week.title}
                  </h3>
                  <p className="text-gray-600">{week.description}</p>
                </div>
                
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
          <div className="space-y-8">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-gradient">Assessments</h2>
              <button
                onClick={handleGenerateAssessment}
                className="glass-button bg-gradient-primary text-white hover-lift pulse-glow"
              >
                <Sparkles className="h-5 w-5 mr-2" />
                Generate Assessment
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
              <div className="glass-card p-12 text-center">
                <div className="float mb-6">
                  <div className="text-6xl">📝</div>
                </div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">No Assessments Yet</h3>
                <p className="text-gray-600 mb-6">Generate AI-powered assessments for this curriculum.</p>
                <button
                  onClick={handleGenerateAssessment}
                  className="glass-button bg-gradient-primary text-white hover-lift"
                >
                  <Sparkles className="h-5 w-5 mr-2" />
                  Generate First Assessment
                </button>
              </div>
            )}
          </div>
        )}

        {/* Export Tab */}
        {activeTab === 'export' && (
          <div className="glass-card p-8">
            <h2 className="text-2xl font-bold text-gradient mb-6">Export & Share</h2>
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