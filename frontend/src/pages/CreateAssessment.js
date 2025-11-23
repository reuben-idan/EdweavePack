import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { curriculumAPI, assessmentAPI } from '../services/api';
import { useToast } from '../components/Toast';
import { Plus, Trash2, ArrowLeft, Save } from 'lucide-react';

const CreateAssessment = () => {
  const navigate = useNavigate();
  const toast = useToast();
  const [curricula, setCurricula] = useState([]);
  const [loading, setLoading] = useState(false);
  const [assessment, setAssessment] = useState({
    title: '',
    description: '',
    curriculum_id: '',
    assessment_type: 'quiz',
    time_limit: 30,
    instructions: ''
  });
  const [questions, setQuestions] = useState([]);

  useEffect(() => {
    fetchCurricula();
  }, []);

  const fetchCurricula = async () => {
    try {
      const response = await curriculumAPI.getAll();
      setCurricula(response.data);
    } catch (error) {
      toast.error('Failed to load curricula', 'Please refresh the page');
    }
  };

  const addQuestion = () => {
    const newQuestion = {
      id: Date.now(),
      question: '',
      type: 'multiple_choice',
      options: ['', '', '', ''],
      correct_answer: 0,
      points: 5
    };
    setQuestions([...questions, newQuestion]);
    toast.success('Question added', 'New question ready for editing');
  };

  const updateQuestion = (id, field, value) => {
    setQuestions(questions.map(q => 
      q.id === id ? { ...q, [field]: value } : q
    ));
  };

  const updateOption = (questionId, optionIndex, value) => {
    setQuestions(questions.map(q => 
      q.id === questionId 
        ? { ...q, options: q.options.map((opt, idx) => idx === optionIndex ? value : opt) }
        : q
    ));
  };

  const removeQuestion = (id) => {
    setQuestions(questions.filter(q => q.id !== id));
    toast.info('Question removed', 'Question deleted from assessment');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!assessment.title || !assessment.curriculum_id || questions.length === 0) {
      toast.error('Missing information', 'Please fill all required fields and add questions');
      return;
    }

    try {
      setLoading(true);
      toast.info('Creating assessment', 'Processing your assessment...');
      
      const assessmentData = {
        ...assessment,
        questions: questions
      };
      
      // Mock API call
      console.log('Creating assessment:', assessmentData);
      
      toast.success('Assessment created successfully', 'Your assessment is now available');
      navigate('/assessments');
      
    } catch (error) {
      toast.error('Failed to create assessment', 'Please try again');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center space-x-4">
            <button
              onClick={() => navigate('/assessments')}
              className="p-2 text-gray-400 hover:text-gray-600 rounded-full hover:bg-gray-100"
            >
              <ArrowLeft className="h-5 w-5" />
            </button>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Create Assessment</h1>
              <p className="text-gray-600">Build a new assessment for your students</p>
            </div>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Basic Information */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Basic Information</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Assessment Title *
                </label>
                <input
                  type="text"
                  value={assessment.title}
                  onChange={(e) => setAssessment({...assessment, title: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Enter assessment title"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Curriculum *
                </label>
                <select
                  value={assessment.curriculum_id}
                  onChange={(e) => setAssessment({...assessment, curriculum_id: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                >
                  <option value="">Select curriculum</option>
                  {curricula.map(curriculum => (
                    <option key={curriculum.id} value={curriculum.id}>
                      {curriculum.title}
                    </option>
                  ))}
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Assessment Type
                </label>
                <select
                  value={assessment.assessment_type}
                  onChange={(e) => setAssessment({...assessment, assessment_type: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="quiz">Quiz</option>
                  <option value="test">Test</option>
                  <option value="exam">Exam</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Time Limit (minutes)
                </label>
                <input
                  type="number"
                  value={assessment.time_limit}
                  onChange={(e) => setAssessment({...assessment, time_limit: parseInt(e.target.value)})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  min="1"
                />
              </div>
            </div>
            
            <div className="mt-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Description
              </label>
              <textarea
                value={assessment.description}
                onChange={(e) => setAssessment({...assessment, description: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows={3}
                placeholder="Describe the assessment purpose and content"
              />
            </div>
            
            <div className="mt-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Instructions
              </label>
              <textarea
                value={assessment.instructions}
                onChange={(e) => setAssessment({...assessment, instructions: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows={3}
                placeholder="Instructions for students taking the assessment"
              />
            </div>
          </div>

          {/* Questions */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-semibold text-gray-900">Questions ({questions.length})</h2>
              <button
                type="button"
                onClick={addQuestion}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                <Plus className="h-4 w-4" />
                <span>Add Question</span>
              </button>
            </div>
            
            {questions.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <p>No questions added yet. Click "Add Question" to get started.</p>
              </div>
            ) : (
              <div className="space-y-6">
                {questions.map((question, index) => (
                  <div key={question.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-md font-medium text-gray-900">Question {index + 1}</h3>
                      <button
                        type="button"
                        onClick={() => removeQuestion(question.id)}
                        className="text-red-600 hover:text-red-800"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                      <div className="md:col-span-2">
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Question Text
                        </label>
                        <textarea
                          value={question.question}
                          onChange={(e) => updateQuestion(question.id, 'question', e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          rows={2}
                          placeholder="Enter your question"
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Points
                        </label>
                        <input
                          type="number"
                          value={question.points}
                          onChange={(e) => updateQuestion(question.id, 'points', parseInt(e.target.value))}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          min="1"
                        />
                      </div>
                    </div>
                    
                    {question.type === 'multiple_choice' && (
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Answer Options
                        </label>
                        <div className="space-y-2">
                          {question.options.map((option, optionIndex) => (
                            <div key={optionIndex} className="flex items-center space-x-2">
                              <input
                                type="radio"
                                name={`correct-${question.id}`}
                                checked={question.correct_answer === optionIndex}
                                onChange={() => updateQuestion(question.id, 'correct_answer', optionIndex)}
                                className="text-blue-600 focus:ring-blue-500"
                              />
                              <input
                                type="text"
                                value={option}
                                onChange={(e) => updateOption(question.id, optionIndex, e.target.value)}
                                className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                placeholder={`Option ${optionIndex + 1}`}
                              />
                            </div>
                          ))}
                        </div>
                        <p className="text-xs text-gray-500 mt-2">Select the correct answer by clicking the radio button</p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Submit */}
          <div className="flex justify-end space-x-4">
            <button
              type="button"
              onClick={() => navigate('/assessments')}
              className="px-6 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex items-center space-x-2 px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
            >
              <Save className="h-4 w-4" />
              <span>{loading ? 'Creating...' : 'Create Assessment'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateAssessment;