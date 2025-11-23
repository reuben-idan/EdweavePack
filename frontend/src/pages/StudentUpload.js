import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { ArrowLeft, Upload, Target, Calendar, BookOpen, TrendingUp, TrendingDown, FileText, Save } from 'lucide-react';

const StudentUpload = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [formData, setFormData] = useState({
    goals: '',
    examType: '',
    subjectFocus: [],
    timeline: '',
    strengths: '',
    weaknesses: '',
    additionalNotes: ''
  });

  const examTypes = ['BECE', 'WASSCE', 'SAT', 'IGCSE', 'University Exams', 'Other'];
  const subjects = [
    'Mathematics', 'English', 'Physics', 'Chemistry', 'Biology', 
    'History', 'Geography', 'Economics', 'Literature', 'Computer Science'
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubjectToggle = (subject) => {
    setFormData(prev => ({
      ...prev,
      subjectFocus: prev.subjectFocus.includes(subject)
        ? prev.subjectFocus.filter(s => s !== subject)
        : [...prev.subjectFocus, subject]
    }));
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.type !== 'application/pdf') {
        toast.error('Please upload PDF files only');
        return;
      }
      if (file.size > 10 * 1024 * 1024) {
        toast.error('File size must be less than 10MB');
        return;
      }
      setUploadedFile(file);
      toast.success(`${file.name} uploaded successfully`);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.goals || !formData.examType || formData.subjectFocus.length === 0) {
      toast.error('Please fill in all required fields');
      return;
    }

    try {
      setLoading(true);
      toast.info('Processing your learning inputs...');
      
      const submitData = {
        ...formData,
        studyMaterial: uploadedFile ? uploadedFile.name : null
      };
      
      console.log('Student learning inputs:', submitData);
      
      toast.success('Learning inputs saved successfully! AI will create your personalized plan.');
      navigate('/student/dashboard');
      
    } catch (error) {
      toast.error('Failed to save learning inputs. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen animated-gradient">
      {/* Header */}
      <div className="glass-nav sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center space-x-4">
            <button
              onClick={() => navigate('/student/dashboard')}
              className="glass-button p-3 hover-lift"
            >
              <ArrowLeft className="h-5 w-5 text-white" />
            </button>
            <div>
              <h1 className="text-xl font-bold text-white">Learning Inputs</h1>
              <p className="text-white/80 text-sm">Tell us about your learning goals and preferences</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-8">
        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Goals */}
          <div className="glass-card p-8">
            <div className="flex items-center space-x-3 mb-6">
              <Target className="h-6 w-6 text-blue-600" />
              <h2 className="text-xl font-semibold text-gray-900">Learning Goals</h2>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                What are your specific learning goals? *
              </label>
              <textarea
                name="goals"
                value={formData.goals}
                onChange={handleChange}
                className="glass-input w-full px-4 py-3 text-gray-900"
                rows={4}
                placeholder="e.g., Score 90% in mathematics, improve problem-solving skills, prepare for university entrance..."
                required
              />
            </div>
          </div>

          {/* Exam & Subject Focus */}
          <div className="glass-card p-8">
            <div className="flex items-center space-x-3 mb-6">
              <BookOpen className="h-6 w-6 text-green-600" />
              <h2 className="text-xl font-semibold text-gray-900">Exam & Subject Focus</h2>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Target Exam Type *</label>
                <select
                  name="examType"
                  value={formData.examType}
                  onChange={handleChange}
                  className="glass-input w-full px-4 py-3 text-gray-900"
                  required
                >
                  <option value="">Select exam type</option>
                  {examTypes.map(exam => (
                    <option key={exam} value={exam}>{exam}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Timeline *</label>
                <input
                  type="date"
                  name="timeline"
                  value={formData.timeline}
                  onChange={handleChange}
                  className="glass-input w-full px-4 py-3 text-gray-900"
                  required
                />
              </div>
            </div>

            <div className="mt-6">
              <label className="block text-sm font-medium text-gray-700 mb-4">Subject Focus Areas *</label>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                {subjects.map(subject => (
                  <button
                    key={subject}
                    type="button"
                    onClick={() => handleSubjectToggle(subject)}
                    className={`glass-card p-3 text-sm font-medium transition-all ${
                      formData.subjectFocus.includes(subject)
                        ? 'bg-gradient-primary text-white'
                        : 'text-gray-700 hover:bg-white/50'
                    }`}
                  >
                    {subject}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Strengths & Weaknesses */}
          <div className="glass-card p-8">
            <div className="flex items-center space-x-3 mb-6">
              <div className="flex space-x-2">
                <TrendingUp className="h-6 w-6 text-green-600" />
                <TrendingDown className="h-6 w-6 text-red-600" />
              </div>
              <h2 className="text-xl font-semibold text-gray-900">Strengths & Weaknesses</h2>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <TrendingUp className="inline h-4 w-4 text-green-600 mr-1" />
                  Your Strengths
                </label>
                <textarea
                  name="strengths"
                  value={formData.strengths}
                  onChange={handleChange}
                  className="glass-input w-full px-4 py-3 text-gray-900"
                  rows={4}
                  placeholder="e.g., Good at algebra, strong memory, quick learner..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  <TrendingDown className="inline h-4 w-4 text-red-600 mr-1" />
                  Areas for Improvement
                </label>
                <textarea
                  name="weaknesses"
                  value={formData.weaknesses}
                  onChange={handleChange}
                  className="glass-input w-full px-4 py-3 text-gray-900"
                  rows={4}
                  placeholder="e.g., Struggle with geometry, need more practice with essays..."
                />
              </div>
            </div>
          </div>

          {/* Study Materials Upload */}
          <div className="glass-card p-8">
            <div className="flex items-center space-x-3 mb-6">
              <FileText className="h-6 w-6 text-purple-600" />
              <h2 className="text-xl font-semibold text-gray-900">Study Materials (Optional)</h2>
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Upload Study Materials (PDF only, max 10MB)
                </label>
                <div className="glass-card p-6 border-2 border-dashed border-gray-300 hover:border-blue-400 transition-colors">
                  <div className="text-center">
                    <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <div className="text-sm text-gray-600 mb-4">
                      {uploadedFile ? (
                        <div className="text-green-600 font-medium">
                          ✓ {uploadedFile.name} uploaded
                        </div>
                      ) : (
                        'Click to upload or drag and drop your study materials'
                      )}
                    </div>
                    <input
                      type="file"
                      accept=".pdf"
                      onChange={handleFileUpload}
                      className="hidden"
                      id="file-upload"
                    />
                    <label
                      htmlFor="file-upload"
                      className="glass-button bg-gradient-primary text-white cursor-pointer"
                    >
                      Choose File
                    </label>
                  </div>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Additional Notes</label>
                <textarea
                  name="additionalNotes"
                  value={formData.additionalNotes}
                  onChange={handleChange}
                  className="glass-input w-full px-4 py-3 text-gray-900"
                  rows={3}
                  placeholder="Any additional information about your learning preferences, study habits, or specific needs..."
                />
              </div>
            </div>
          </div>

          {/* Submit */}
          <div className="flex space-x-4">
            <button
              type="button"
              onClick={() => navigate('/student/dashboard')}
              className="flex-1 glass-button text-gray-700 hover:bg-white/50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex-1 glass-button bg-gradient-primary text-white hover-lift"
            >
              {loading ? (
                <div className="spinner w-5 h-5 mx-auto"></div>
              ) : (
                <>
                  <Save className="h-5 w-5 mr-2" />
                  Save Learning Inputs
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default StudentUpload;