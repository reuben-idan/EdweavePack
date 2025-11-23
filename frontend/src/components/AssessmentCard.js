import React, { useState } from 'react';
import { FileText, Clock, Award, Users, Play, Eye, BarChart3, CheckCircle } from 'lucide-react';
import { assessmentAPI } from '../services/api';

const AssessmentCard = ({ assessment, onTake, onView, onViewResults }) => {
  const [isLoading, setIsLoading] = useState(false);

  const handleTakeAssessment = async () => {
    setIsLoading(true);
    try {
      if (onTake) {
        await onTake(assessment);
      }
    } catch (error) {
      console.error('Failed to start assessment:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const getAssessmentTypeIcon = (type) => {
    switch (type) {
      case 'quiz':
        return <FileText className="h-5 w-5" />;
      case 'test':
        return <Award className="h-5 w-5" />;
      case 'assignment':
        return <CheckCircle className="h-5 w-5" />;
      default:
        return <FileText className="h-5 w-5" />;
    }
  };

  const getAssessmentTypeColor = (type) => {
    switch (type) {
      case 'quiz':
        return 'bg-blue-100 text-blue-800';
      case 'test':
        return 'bg-purple-100 text-purple-800';
      case 'assignment':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const formatDuration = (minutes) => {
    if (!minutes) return 'No time limit';
    if (minutes < 60) return `${minutes} min`;
    const hours = Math.floor(minutes / 60);
    const remainingMinutes = minutes % 60;
    return remainingMinutes > 0 ? `${hours}h ${remainingMinutes}m` : `${hours}h`;
  };

  return (
    <div className="bg-white rounded-lg shadow-md border border-gray-200 overflow-hidden hover:shadow-lg transition-shadow duration-200">
      {/* Header */}
      <div className="p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div className={`p-2 rounded-lg ${getAssessmentTypeColor(assessment.assessment_type)}`}>
              {getAssessmentTypeIcon(assessment.assessment_type)}
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-gray-900">
                {assessment.title}
              </h3>
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getAssessmentTypeColor(assessment.assessment_type)}`}>
                {assessment.assessment_type.charAt(0).toUpperCase() + assessment.assessment_type.slice(1)}
              </span>
            </div>
          </div>
        </div>

        <p className="text-gray-600 text-sm mb-4 line-clamp-2">
          {assessment.description || 'No description available'}
        </p>

        {/* Assessment Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div className="text-center">
            <div className="flex items-center justify-center mb-1">
              <Award className="h-4 w-4 text-yellow-500 mr-1" />
            </div>
            <div className="text-lg font-semibold text-gray-900">
              {assessment.total_points || 0}
            </div>
            <div className="text-xs text-gray-500">Points</div>
          </div>

          <div className="text-center">
            <div className="flex items-center justify-center mb-1">
              <Clock className="h-4 w-4 text-blue-500 mr-1" />
            </div>
            <div className="text-lg font-semibold text-gray-900">
              {assessment.time_limit || '∞'}
            </div>
            <div className="text-xs text-gray-500">
              {assessment.time_limit ? 'Minutes' : 'No Limit'}
            </div>
          </div>

          <div className="text-center">
            <div className="flex items-center justify-center mb-1">
              <FileText className="h-4 w-4 text-green-500 mr-1" />
            </div>
            <div className="text-lg font-semibold text-gray-900">
              {assessment.questions?.length || 0}
            </div>
            <div className="text-xs text-gray-500">Questions</div>
          </div>

          <div className="text-center">
            <div className="flex items-center justify-center mb-1">
              <Users className="h-4 w-4 text-purple-500 mr-1" />
            </div>
            <div className="text-lg font-semibold text-gray-900">
              {assessment.attempts_count || 0}
            </div>
            <div className="text-xs text-gray-500">Attempts</div>
          </div>
        </div>

        {/* Assessment Info */}
        <div className="bg-gray-50 rounded-lg p-3 mb-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
            <div className="flex items-center">
              <Clock className="h-4 w-4 text-gray-400 mr-2" />
              <span className="text-gray-600">
                Duration: {formatDuration(assessment.time_limit)}
              </span>
            </div>
            
            <div className="flex items-center">
              <Award className="h-4 w-4 text-gray-400 mr-2" />
              <span className="text-gray-600">
                Total Points: {assessment.total_points || 0}
              </span>
            </div>
          </div>
        </div>

        {/* Performance Summary (if available) */}
        {assessment.performance_summary && (
          <div className="bg-blue-50 rounded-lg p-3 mb-4">
            <h4 className="text-sm font-medium text-blue-900 mb-2">
              Class Performance
            </h4>
            <div className="grid grid-cols-3 gap-3 text-sm">
              <div className="text-center">
                <div className="text-lg font-semibold text-blue-900">
                  {assessment.performance_summary.average_score || 0}%
                </div>
                <div className="text-blue-700">Average</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold text-blue-900">
                  {assessment.performance_summary.completion_rate || 0}%
                </div>
                <div className="text-blue-700">Completed</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold text-blue-900">
                  {assessment.performance_summary.pass_rate || 0}%
                </div>
                <div className="text-blue-700">Passed</div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div className="px-6 py-4 bg-gray-50 border-t">
        <div className="flex space-x-2">
          <button
            onClick={handleTakeAssessment}
            disabled={isLoading}
            className="flex-1 flex items-center justify-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 transition-colors"
          >
            {isLoading ? (
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" />
            ) : (
              <Play className="h-4 w-4" />
            )}
            <span>{isLoading ? 'Loading...' : 'Take Assessment'}</span>
          </button>

          <button
            onClick={() => onView && onView(assessment)}
            className="px-4 py-2 text-gray-600 bg-white border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
          >
            <Eye className="h-4 w-4" />
          </button>

          {assessment.attempts_count > 0 && (
            <button
              onClick={() => onViewResults && onViewResults(assessment)}
              className="px-4 py-2 text-gray-600 bg-white border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
            >
              <BarChart3 className="h-4 w-4" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default AssessmentCard;