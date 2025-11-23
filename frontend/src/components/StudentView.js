import React, { useState, useEffect } from 'react';
import { Play, CheckCircle, Clock, BookOpen, Award } from 'lucide-react';

const StudentView = ({ studentId, curriculumId }) => {
  const [learningPath, setLearningPath] = useState(null);
  const [currentWeek, setCurrentWeek] = useState(1);
  const [progress, setProgress] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLearningPath();
  }, [studentId, curriculumId]);

  const fetchLearningPath = async () => {
    try {
      // Simulated API call
      const mockPath = {
        student_name: "Alex Johnson",
        curriculum_title: "Introduction to Biology",
        weekly_modules: [
          {
            week_number: 1,
            title: "Cell Structure",
            bloom_focus: "Remember & Understand",
            content_blocks: [
              {
                title: "What is a Cell?",
                description: "Basic cell components and functions",
                estimated_duration: 30,
                activities: ["Interactive diagram", "Video tour"],
                completed: true
              },
              {
                title: "Cell Parts",
                description: "Identifying organelles and their roles",
                estimated_duration: 45,
                activities: ["Labeling exercise", "Memory game"],
                completed: false
              }
            ]
          },
          {
            week_number: 2,
            title: "Cell Functions",
            bloom_focus: "Apply",
            content_blocks: [
              {
                title: "How Cells Work",
                description: "Cell processes and energy",
                estimated_duration: 40,
                activities: ["Simulation", "Experiment"],
                completed: false
              }
            ]
          }
        ]
      };
      
      setLearningPath(mockPath);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch learning path:', error);
      setLoading(false);
    }
  };

  const markBlockComplete = (weekNum, blockIndex) => {
    setProgress(prev => ({
      ...prev,
      [`${weekNum}-${blockIndex}`]: true
    }));
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      {/* Header */}
      <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              Welcome back, {learningPath?.student_name}!
            </h1>
            <p className="text-gray-600 mt-1">{learningPath?.curriculum_title}</p>
          </div>
          <div className="flex items-center space-x-2 bg-green-100 px-4 py-2 rounded-full">
            <Award className="h-5 w-5 text-green-600" />
            <span className="text-green-800 font-medium">Level 3</span>
          </div>
        </div>
      </div>

      {/* Progress Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-white rounded-lg p-4 shadow-md">
          <div className="flex items-center">
            <CheckCircle className="h-8 w-8 text-green-500 mr-3" />
            <div>
              <p className="text-sm text-gray-600">Completed</p>
              <p className="text-xl font-bold text-gray-900">3/8</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-lg p-4 shadow-md">
          <div className="flex items-center">
            <Clock className="h-8 w-8 text-blue-500 mr-3" />
            <div>
              <p className="text-sm text-gray-600">Time Spent</p>
              <p className="text-xl font-bold text-gray-900">2.5h</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-lg p-4 shadow-md">
          <div className="flex items-center">
            <BookOpen className="h-8 w-8 text-purple-500 mr-3" />
            <div>
              <p className="text-sm text-gray-600">Current Week</p>
              <p className="text-xl font-bold text-gray-900">Week {currentWeek}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Weekly Modules */}
      <div className="space-y-6">
        {learningPath?.weekly_modules?.map((week) => (
          <div key={week.week_number} className="bg-white rounded-xl shadow-lg overflow-hidden">
            <div className="bg-gradient-to-r from-indigo-500 to-purple-600 p-6 text-white">
              <h2 className="text-xl font-bold">Week {week.week_number}: {week.title}</h2>
              <p className="text-indigo-100 mt-1">Focus: {week.bloom_focus}</p>
            </div>
            
            <div className="p-6">
              <div className="space-y-4">
                {week.content_blocks?.map((block, index) => (
                  <div 
                    key={index}
                    className={`border rounded-lg p-4 transition-all duration-200 ${
                      block.completed || progress[`${week.week_number}-${index}`]
                        ? 'bg-green-50 border-green-200'
                        : 'bg-gray-50 border-gray-200 hover:border-indigo-300'
                    }`}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center mb-2">
                          {block.completed || progress[`${week.week_number}-${index}`] ? (
                            <CheckCircle className="h-5 w-5 text-green-500 mr-2" />
                          ) : (
                            <Play className="h-5 w-5 text-indigo-500 mr-2" />
                          )}
                          <h3 className="font-semibold text-gray-900">{block.title}</h3>
                          <span className="ml-2 text-sm text-gray-500">
                            {block.estimated_duration} min
                          </span>
                        </div>
                        
                        <p className="text-gray-600 mb-3">{block.description}</p>
                        
                        <div className="flex flex-wrap gap-2">
                          {block.activities?.map((activity, actIndex) => (
                            <span 
                              key={actIndex}
                              className="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-sm"
                            >
                              {activity}
                            </span>
                          ))}
                        </div>
                      </div>
                      
                      <button
                        onClick={() => markBlockComplete(week.week_number, index)}
                        disabled={block.completed || progress[`${week.week_number}-${index}`]}
                        className={`ml-4 px-4 py-2 rounded-lg font-medium transition-colors ${
                          block.completed || progress[`${week.week_number}-${index}`]
                            ? 'bg-green-100 text-green-700 cursor-not-allowed'
                            : 'bg-indigo-600 text-white hover:bg-indigo-700'
                        }`}
                      >
                        {block.completed || progress[`${week.week_number}-${index}`] 
                          ? 'Completed' 
                          : 'Start'
                        }
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Mobile-friendly bottom navigation */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-4 md:hidden">
        <div className="flex justify-around">
          <button className="flex flex-col items-center text-indigo-600">
            <BookOpen className="h-6 w-6" />
            <span className="text-xs mt-1">Learn</span>
          </button>
          <button className="flex flex-col items-center text-gray-400">
            <CheckCircle className="h-6 w-6" />
            <span className="text-xs mt-1">Progress</span>
          </button>
          <button className="flex flex-col items-center text-gray-400">
            <Award className="h-6 w-6" />
            <span className="text-xs mt-1">Achievements</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default StudentView;