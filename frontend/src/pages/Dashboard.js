import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { analyticsAPI } from '../services/api';

const Dashboard = () => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const response = await analyticsAPI.getDashboard();
        setAnalytics(response.data);
      } catch (error) {
        console.error('Failed to fetch analytics:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-blue-500/30 border-t-blue-500 rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-semibold text-gray-800 mb-2">Dashboard</h1>
          <p className="text-gray-600">Welcome to your AI-powered curriculum builder</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="backdrop-blur-xl bg-white/20 border border-white/30 rounded-3xl p-6 shadow-xl hover:shadow-2xl transition-all duration-300">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-blue-600 rounded-2xl flex items-center justify-center mr-4">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-600">Total Curricula</p>
                <p className="text-2xl font-semibold text-gray-800">{analytics?.total_curricula || 0}</p>
              </div>
            </div>
          </div>

          <div className="backdrop-blur-xl bg-white/20 border border-white/30 rounded-3xl p-6 shadow-xl hover:shadow-2xl transition-all duration-300">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-purple-600 rounded-2xl flex items-center justify-center mr-4">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-600">Total Assessments</p>
                <p className="text-2xl font-semibold text-gray-800">{analytics?.total_assessments || 0}</p>
              </div>
            </div>
          </div>

          <div className="backdrop-blur-xl bg-white/20 border border-white/30 rounded-3xl p-6 shadow-xl hover:shadow-2xl transition-all duration-300">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-gradient-to-r from-green-500 to-green-600 rounded-2xl flex items-center justify-center mr-4">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-600">Subjects Covered</p>
                <p className="text-2xl font-semibold text-gray-800">{analytics?.subject_distribution?.length || 0}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="backdrop-blur-xl bg-white/20 border border-white/30 rounded-3xl p-6 shadow-xl mb-8">
          <h3 className="text-lg font-semibold text-gray-800 mb-6">Quick Actions</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Link
              to="/curriculum/create"
              className="group flex items-center p-6 bg-white/30 backdrop-blur-sm border border-white/40 rounded-2xl hover:bg-white/40 hover:shadow-lg transition-all duration-200 transform hover:-translate-y-1"
            >
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl flex items-center justify-center mr-4 group-hover:scale-110 transition-transform duration-200">
                <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
              </div>
              <span className="font-medium text-gray-800">Create New Curriculum</span>
            </Link>
            
            <Link
              to="/curriculum"
              className="group flex items-center p-6 bg-white/30 backdrop-blur-sm border border-white/40 rounded-2xl hover:bg-white/40 hover:shadow-lg transition-all duration-200 transform hover:-translate-y-1"
            >
              <div className="w-10 h-10 bg-gradient-to-r from-green-500 to-blue-600 rounded-xl flex items-center justify-center mr-4 group-hover:scale-110 transition-transform duration-200">
                <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <span className="font-medium text-gray-800">View All Curricula</span>
            </Link>
          </div>
        </div>

        {/* Recent Curricula */}
        {analytics?.recent_curricula?.length > 0 && (
          <div className="backdrop-blur-xl bg-white/20 border border-white/30 rounded-3xl p-6 shadow-xl">
            <h3 className="text-lg font-semibold text-gray-800 mb-6">Recent Curricula</h3>
            <div className="space-y-4">
              {analytics.recent_curricula.map((curriculum) => (
                <div key={curriculum.id} className="flex items-center justify-between p-4 bg-white/30 backdrop-blur-sm border border-white/40 rounded-2xl hover:bg-white/40 transition-all duration-200">
                  <div>
                    <h4 className="font-medium text-gray-800">{curriculum.title}</h4>
                    <p className="text-sm text-gray-600">{curriculum.subject}</p>
                  </div>
                  <span className="text-xs text-gray-500 bg-white/50 px-3 py-1 rounded-full">
                    {new Date(curriculum.created_at).toLocaleDateString()}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;