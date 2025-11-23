import React, { useState } from 'react';
import { Clock, Target, Activity, BookOpen, ChevronDown, ChevronUp, Play } from 'lucide-react';

const ModuleCard = ({ module, weekNumber, isExpanded, onToggle, onStart }) => {
  const [isStarting, setIsStarting] = useState(false);

  const handleStart = async () => {
    setIsStarting(true);
    try {
      if (onStart) {
        await onStart(module);
      }
    } catch (error) {
      console.error('Failed to start module:', error);
    } finally {
      setIsStarting(false);
    }
  };

  const getBloomLevelColor = (level) => {
    const colors = {
      'Remember': 'bg-red-100 text-red-800',
      'Understand': 'bg-orange-100 text-orange-800',
      'Apply': 'bg-yellow-100 text-yellow-800',
      'Analyze': 'bg-green-100 text-green-800',
      'Evaluate': 'bg-blue-100 text-blue-800',
      'Create': 'bg-purple-100 text-purple-800'
    };
    return colors[level] || 'bg-gray-100 text-gray-800';
  };

  const formatDuration = (minutes) => {
    if (minutes < 60) {
      return `${minutes} min`;
    }
    const hours = Math.floor(minutes / 60);
    const remainingMinutes = minutes % 60;
    return remainingMinutes > 0 ? `${hours}h ${remainingMinutes}m` : `${hours}h`;
  };

  return (
    <div className="bg-white rounded-lg shadow-md border border-gray-200 overflow-hidden">
      {/* Header */}
      <div 
        className="p-4 cursor-pointer hover:bg-gray-50 transition-colors"
        onClick={onToggle}
      >
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <div className="flex items-center space-x-3 mb-2">
              <span className="text-sm font-medium text-gray-500">
                Week {weekNumber} • Module {module.sequence_order}
              </span>
              
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${getBloomLevelColor(module.bloom_level)}`}>
                {module.bloom_level}
              </span>
            </div>
            
            <h3 className="text-lg font-semibold text-gray-900 mb-1">
              {module.title}
            </h3>
            
            <p className="text-gray-600 text-sm line-clamp-2">
              {module.description}
            </p>
          </div>
          
          <div className="flex items-center space-x-3 ml-4">
            <div className="flex items-center text-sm text-gray-500">
              <Clock className="h-4 w-4 mr-1" />
              <span>{formatDuration(module.estimated_duration)}</span>
            </div>
            
            {isExpanded ? (
              <ChevronUp className="h-5 w-5 text-gray-400" />
            ) : (
              <ChevronDown className="h-5 w-5 text-gray-400" />
            )}
          </div>
        </div>
      </div>

      {/* Expanded Content */}
      {isExpanded && (
        <div className="border-t border-gray-200">
          {/* Content Details */}
          <div className="p-4 space-y-4">
            {/* Learning Objectives */}
            {module.learning_outcomes && module.learning_outcomes.length > 0 && (
              <div>
                <h4 className="flex items-center text-sm font-medium text-gray-900 mb-2">
                  <Target className="h-4 w-4 mr-2" />
                  Learning Objectives
                </h4>
                <ul className="space-y-1">
                  {module.learning_outcomes.map((objective, index) => (
                    <li key={index} className="text-sm text-gray-600 flex items-start">
                      <span className="w-1.5 h-1.5 bg-blue-500 rounded-full mt-2 mr-2 flex-shrink-0" />
                      {objective}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Activities */}
            {module.activities && module.activities.length > 0 && (
              <div>
                <h4 className="flex items-center text-sm font-medium text-gray-900 mb-2">
                  <Activity className="h-4 w-4 mr-2" />
                  Activities
                </h4>
                <div className="flex flex-wrap gap-2">
                  {module.activities.map((activity, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm"
                    >
                      {activity}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Resources */}
            {module.resources && module.resources.length > 0 && (
              <div>
                <h4 className="flex items-center text-sm font-medium text-gray-900 mb-2">
                  <BookOpen className="h-4 w-4 mr-2" />
                  Resources
                </h4>
                <ul className="space-y-1">
                  {module.resources.map((resource, index) => (
                    <li key={index} className="text-sm text-gray-600 flex items-center">
                      <span className="w-1.5 h-1.5 bg-green-500 rounded-full mr-2" />
                      {resource}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Content Data */}
            {module.content_data && (
              <div>
                <h4 className="text-sm font-medium text-gray-900 mb-2">
                  Module Content
                </h4>
                <div className="bg-gray-50 rounded-md p-3">
                  <p className="text-sm text-gray-700">
                    {typeof module.content_data === 'string' 
                      ? module.content_data 
                      : JSON.stringify(module.content_data, null, 2)
                    }
                  </p>
                </div>
              </div>
            )}
          </div>

          {/* Action Bar */}
          <div className="px-4 py-3 bg-gray-50 border-t flex items-center justify-between">
            <div className="flex items-center space-x-4 text-sm text-gray-500">
              <span>Estimated Duration: {formatDuration(module.estimated_duration)}</span>
              <span>•</span>
              <span>Bloom Level: {module.bloom_level}</span>
            </div>
            
            <button
              onClick={handleStart}
              disabled={isStarting}
              className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 transition-colors"
            >
              {isStarting ? (
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" />
              ) : (
                <Play className="h-4 w-4" />
              )}
              <span>{isStarting ? 'Starting...' : 'Start Module'}</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ModuleCard;