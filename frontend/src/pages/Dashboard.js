import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import CurriculumCard from '../components/CurriculumCard';
import AnalyticsChart from '../components/AnalyticsChart';
import { analyticsAPI, curriculumAPI } from '../services/api';
import { BookOpen, FileText, BarChart3, Plus, Upload, Users, TrendingUp } from 'lucide-react';

const Dashboard = () => {
  const [analytics, setAnalytics] = useState(null);
  const [curricula, setCurricula] = useState([]);
  const [performanceData, setPerformanceData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Check if user is authenticated
      const token = localStorage.getItem('token');
      if (!token) {
        console.error('No authentication token found');
        navigate('/login');
        return;
      }
      
      // Set default data immediately
      setAnalytics({
        total_curricula: 0,
        total_assessments: 0,
        total_students: 0,
        average_class_performance: 0,
        subject_distribution: []
      });
      setCurricula([]);
      
      // Try to fetch real data
      try {
        const analyticsResponse = await analyticsAPI.getDashboard();
        setAnalytics(analyticsResponse.data);
      } catch (error) {
        console.error('Analytics API error:', error);
      }
      
      // Try to fetch curricula
      try {
        const curriculaResponse = await curriculumAPI.getAll();
        setCurricula(curriculaResponse.data || []);
      } catch (error) {
        console.error('Curricula API error:', error);
      }
      
      // Fetch performance data
      try {
        const performanceResponse = await analyticsAPI.getClassPerformance();
        setPerformanceData(performanceResponse.data);
      } catch (error) {
        console.log('Performance data not available');
      }
      
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
      setError('Failed to load dashboard data. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  const handleCurriculumView = (curriculum) => {
    navigate(`/curriculum/${curriculum.id}`);
  };
  
  const handleCurriculumEdit = (curriculum) => {
    navigate(`/curriculum/${curriculum.id}/edit`);
  };
  
  const handleCurriculumDelete = async (curriculum) => {
    if (window.confirm(`Are you sure you want to delete "${curriculum.title}"?`)) {
      try {
        // await curriculumAPI.delete(curriculum.id);
        fetchDashboardData();
      } catch (error) {
        console.error('Failed to delete curriculum:', error);
      }
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="text-red-600 mb-4">{error}</div>
          <button
            onClick={() => {
              setError(null);
              fetchDashboardData();
            }}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
          <p className="text-gray-600">Welcome to your AI-powered curriculum builder</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <BookOpen className="h-6 w-6 text-blue-500" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Total Curricula
                    </dt>
                    <dd className="text-2xl font-bold text-gray-900">
                      {analytics?.total_curricula || 0}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <FileText className="h-6 w-6 text-green-500" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Total Assessments
                    </dt>
                    <dd className="text-2xl font-bold text-gray-900">
                      {analytics?.total_assessments || 0}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
          
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <Users className="h-6 w-6 text-purple-500" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Total Students
                    </dt>
                    <dd className="text-2xl font-bold text-gray-900">
                      {analytics?.total_students || 0}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <TrendingUp className="h-6 w-6 text-orange-500" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Avg Performance
                    </dt>
                    <dd className="text-2xl font-bold text-gray-900">
                      {analytics?.average_class_performance || 0}%
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white shadow rounded-lg mb-8">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
              Quick Actions
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <Link
                to="/upload"
                className="flex items-center p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-colors"
              >
                <Upload className="h-6 w-6 text-gray-400 mr-3" />
                <span className="text-sm font-medium text-gray-900">
                  Upload & Create Curriculum
                </span>
              </Link>
              
              <Link
                to="/curriculum"
                className="flex items-center p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-green-500 hover:bg-green-50 transition-colors"
              >
                <BookOpen className="h-6 w-6 text-gray-400 mr-3" />
                <span className="text-sm font-medium text-gray-900">
                  View All Curricula
                </span>
              </Link>
              
              <Link
                to="/students"
                className="flex items-center p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-purple-500 hover:bg-purple-50 transition-colors"
              >
                <Users className="h-6 w-6 text-gray-400 mr-3" />
                <span className="text-sm font-medium text-gray-900">
                  Manage Students
                </span>
              </Link>
            </div>
          </div>
        </div>

        {/* Analytics Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Performance Distribution */}
          {performanceData && (
            <AnalyticsChart
              type="performance"
              data={performanceData.performance_distribution}
              title="Class Performance Distribution"
              height={250}
            />
          )}
          
          {/* Subject Distribution */}
          {analytics?.subject_distribution && (
            <AnalyticsChart
              type="pie"
              data={analytics.subject_distribution.map(item => ({
                name: item.subject,
                value: item.count
              }))}
              title="Curricula by Subject"
              height={250}
            />
          )}
        </div>
        
        {/* Recent Curricula */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg leading-6 font-medium text-gray-900">
                Recent Curricula
              </h3>
              <Link
                to="/curriculum"
                className="text-sm text-blue-600 hover:text-blue-500"
              >
                View all
              </Link>
            </div>
            
            {curricula.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {curricula.slice(0, 6).map((curriculum) => (
                  <CurriculumCard
                    key={curriculum.id}
                    curriculum={curriculum}
                    onView={handleCurriculumView}
                    onEdit={handleCurriculumEdit}
                    onDelete={handleCurriculumDelete}
                  />
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <BookOpen className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">No curricula yet</h3>
                <p className="text-gray-600 mb-4">Get started by creating your first curriculum.</p>
                <Link
                  to="/upload"
                  className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  <Plus className="h-4 w-4 mr-2" />
                  Create First Curriculum
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;