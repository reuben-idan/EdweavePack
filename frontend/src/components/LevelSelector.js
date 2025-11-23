import React, { useState, useEffect } from 'react';
import { GraduationCap, Users, BookOpen, Lightbulb } from 'lucide-react';

const LevelSelector = ({ onLevelSelect, selectedLevel }) => {
  const [levels, setLevels] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchEducationLevels();
  }, []);

  const fetchEducationLevels = async () => {
    try {
      const response = await fetch('/api/curriculum/enhanced/templates/levels');
      const data = await response.json();
      setLevels(data.available_levels);
    } catch (error) {
      console.error('Failed to fetch education levels:', error);
      // Fallback data
      setLevels({
        "K-2": {
          duration_range: "15-30 minutes",
          assessment_types: ["visual", "hands_on", "simple_mcq"],
          bloom_focus: ["Remember", "Understand"],
          instruction_style: "concrete_examples"
        },
        "3-5": {
          duration_range: "20-45 minutes",
          assessment_types: ["mcq", "short_answer", "project"],
          bloom_focus: ["Remember", "Understand", "Apply"],
          instruction_style: "guided_discovery"
        },
        "6-8": {
          duration_range: "30-60 minutes",
          assessment_types: ["mcq", "short_answer", "essay", "project"],
          bloom_focus: ["Understand", "Apply", "Analyze"],
          instruction_style: "inquiry_based"
        },
        "9-12": {
          duration_range: "45-90 minutes",
          assessment_types: ["mcq", "essay", "project", "presentation"],
          bloom_focus: ["Apply", "Analyze", "Evaluate", "Create"],
          instruction_style: "problem_based"
        },
        "University": {
          duration_range: "60-180 minutes",
          assessment_types: ["essay", "research_paper", "thesis", "coding"],
          bloom_focus: ["Analyze", "Evaluate", "Create"],
          instruction_style: "self_directed"
        }
      });
    } finally {
      setLoading(false);
    }
  };

  const getLevelIcon = (level) => {
    switch (level) {
      case 'K-2':
      case '3-5':
        return <Users className="h-6 w-6" />;
      case '6-8':
        return <BookOpen className="h-6 w-6" />;
      case '9-12':
        return <Lightbulb className="h-6 w-6" />;
      case 'University':
        return <GraduationCap className="h-6 w-6" />;
      default:
        return <BookOpen className="h-6 w-6" />;
    }
  };

  const getLevelColor = (level) => {
    switch (level) {
      case 'K-2':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case '3-5':
        return 'bg-green-100 text-green-800 border-green-200';
      case '6-8':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case '9-12':
        return 'bg-purple-100 text-purple-800 border-purple-200';
      case 'University':
        return 'bg-indigo-100 text-indigo-800 border-indigo-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  if (loading) {
    return (
      <div className="animate-pulse">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[1, 2, 3, 4, 5].map(i => (
            <div key={i} className="h-32 bg-gray-200 rounded-lg"></div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-900">Select Education Level</h3>
      <p className="text-gray-600">Choose the appropriate level to customize curriculum content and activities.</p>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {Object.entries(levels).map(([level, details]) => (
          <button
            key={level}
            onClick={() => onLevelSelect(level)}
            className={`p-4 rounded-lg border-2 transition-all duration-200 text-left ${
              selectedLevel === level
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-200 hover:border-gray-300 bg-white'
            }`}
          >
            <div className="flex items-start space-x-3">
              <div className={`p-2 rounded-lg ${getLevelColor(level)}`}>
                {getLevelIcon(level)}
              </div>
              
              <div className="flex-1 min-w-0">
                <h4 className="font-semibold text-gray-900">{level}</h4>
                <p className="text-sm text-gray-600 mt-1">
                  Duration: {details.duration_range}
                </p>
                <p className="text-sm text-gray-600">
                  Style: {details.instruction_style.replace('_', ' ')}
                </p>
                
                <div className="mt-2">
                  <p className="text-xs text-gray-500 mb-1">Bloom's Focus:</p>
                  <div className="flex flex-wrap gap-1">
                    {details.bloom_focus.slice(0, 2).map((focus, index) => (
                      <span
                        key={index}
                        className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs"
                      >
                        {focus}
                      </span>
                    ))}
                    {details.bloom_focus.length > 2 && (
                      <span className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs">
                        +{details.bloom_focus.length - 2}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
};

export default LevelSelector;