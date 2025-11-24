import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Play, CheckCircle, Clock, BookOpen } from 'lucide-react';

const StudentLesson = () => {
  const { lessonId } = useParams();
  const navigate = useNavigate();
  const [lesson, setLesson] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLesson();
  }, [lessonId]);

  const fetchLesson = async () => {
    try {
      // Mock lesson data
      const mockLesson = {
        id: lessonId,
        title: `Lesson ${lessonId}: Quadratic Functions`,
        subject: 'Mathematics',
        duration: 30,
        difficulty: 'Intermediate',
        content: {
          video: 'https://example.com/video.mp4',
          text: `
            <h2>Introduction to Quadratic Functions</h2>
            <p>A quadratic function is a polynomial function of degree 2. The general form is:</p>
            <p><strong>f(x) = ax² + bx + c</strong></p>
            <p>where a ≠ 0.</p>
            
            <h3>Key Properties:</h3>
            <ul>
              <li>The graph is a parabola</li>
              <li>Has a vertex (maximum or minimum point)</li>
              <li>Axis of symmetry at x = -b/(2a)</li>
            </ul>
            
            <h3>Examples:</h3>
            <p>1. f(x) = x² - 4x + 3</p>
            <p>2. f(x) = -2x² + 8x - 6</p>
          `,
          exercises: [
            { id: 1, question: 'Find the vertex of f(x) = x² - 4x + 3', answer: '(2, -1)' },
            { id: 2, question: 'What is the axis of symmetry for f(x) = 2x² - 8x + 5?', answer: 'x = 2' }
          ]
        },
        completed: false,
        progress: 0
      };
      
      setLesson(mockLesson);
    } catch (error) {
      console.error('Error fetching lesson:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleComplete = () => {
    setLesson(prev => ({ ...prev, completed: true, progress: 100 }));
    navigate('/student/dashboard');
  };

  if (loading) {
    return (
      <div className="min-h-screen animated-gradient flex items-center justify-center">
        <div className="glass-card p-8 text-center">
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-gray-700 font-medium">Loading lesson...</p>
        </div>
      </div>
    );
  }

  if (!lesson) {
    return (
      <div className="min-h-screen animated-gradient flex items-center justify-center">
        <div className="glass-card p-8 text-center">
          <p className="text-gray-700 font-medium">Lesson not found</p>
          <button 
            onClick={() => navigate('/student/dashboard')}
            className="mt-4 glass-button bg-gradient-primary text-white"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen animated-gradient">
      {/* Header */}
      <div className="glass-nav sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => navigate('/student/dashboard')}
              className="glass-button p-3 text-white hover-lift"
            >
              <ArrowLeft className="h-5 w-5" />
            </button>
            
            <div className="text-center">
              <h1 className="text-xl font-bold text-white">{lesson.title}</h1>
              <p className="text-white/80 text-sm">{lesson.subject} • {lesson.duration} min</p>
            </div>
            
            <div className="flex items-center space-x-2">
              <span className="text-white/80 text-sm">{lesson.difficulty}</span>
              {lesson.completed && <CheckCircle className="h-5 w-5 text-green-400" />}
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Lesson Content */}
        <div className="bg-white border-2 border-gray-200 rounded-2xl p-8 mb-8 shadow-sm">
          <div className="flex items-center mb-8 pb-6 border-b border-gray-200">
            <div className="p-4 bg-gradient-primary rounded-xl mr-6">
              <BookOpen className="h-7 w-7 text-white" />
            </div>
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-2">{lesson.title}</h2>
              <div className="flex items-center text-gray-600">
                <Clock className="h-5 w-5 mr-2" />
                <span className="text-lg">{lesson.duration} minutes</span>
              </div>
            </div>
          </div>

          {/* Video Player */}
          <div className="bg-gray-900 rounded-xl mb-6 aspect-video overflow-hidden">
            <video 
              controls 
              className="w-full h-full"
              poster="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 450'%3E%3Crect width='800' height='450' fill='%23374151'/%3E%3Ctext x='400' y='225' text-anchor='middle' fill='white' font-size='24'%3EQuadratic Functions Lesson%3C/text%3E%3C/svg%3E"
            >
              <source src="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4" type="video/mp4" />
              <p className="text-white p-4">Your browser does not support the video tag.</p>
            </video>
          </div>

          {/* Lesson Text Content */}
          <div className="mb-8">
            <div 
              className="prose prose-lg max-w-none text-gray-800 leading-relaxed"
              style={{
                '--tw-prose-headings': '#1f2937',
                '--tw-prose-body': '#374151',
                '--tw-prose-bold': '#111827',
                '--tw-prose-links': '#3b82f6'
              }}
              dangerouslySetInnerHTML={{ __html: lesson.content.text }}
            />
          </div>

          {/* Practice Exercises */}
          <div className="bg-gray-50 border-2 border-gray-200 rounded-xl p-6">
            <h3 className="text-2xl font-semibold text-gray-900 mb-6">Practice Exercises</h3>
            <div className="space-y-6">
              {lesson.content.exercises.map((exercise) => (
                <div key={exercise.id} className="bg-white border border-gray-200 rounded-lg p-5">
                  <p className="font-medium text-gray-900 mb-4 text-lg">{exercise.question}</p>
                  <input
                    type="text"
                    placeholder="Your answer..."
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg bg-white text-gray-800 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"
                  />
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-between">
          <button
            onClick={() => navigate('/student/dashboard')}
            className="glass-button bg-gray-500/20 text-gray-700"
          >
            Back to Dashboard
          </button>
          
          <button
            onClick={handleComplete}
            className="glass-button bg-gradient-success text-white"
          >
            <CheckCircle className="h-4 w-4 mr-2" />
            Mark Complete
          </button>
        </div>
      </div>
    </div>
  );
};

export default StudentLesson;