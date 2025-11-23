import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { ArrowLeft, Save, User, Mail, Calendar, Target, BookOpen, Settings, Camera, Edit3, Award, Brain, Clock, Star } from 'lucide-react';
import { getStudentName } from '../utils/studentUtils';

const StudentProfile = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    age: '',
    learningStyle: '',
    targetExams: [],
    academicGoals: '',
    examDate: ''
  });

  const learningStyles = [
    { id: 'visual', label: 'Visual', desc: 'Learn through images, diagrams, and charts' },
    { id: 'auditory', label: 'Auditory', desc: 'Learn through listening and discussion' },
    { id: 'reading', label: 'Reading/Writing', desc: 'Learn through text and written materials' },
    { id: 'kinesthetic', label: 'Kinesthetic', desc: 'Learn through hands-on activities' }
  ];

  const examOptions = ['BECE', 'WASSCE', 'SAT', 'IGCSE', 'University Exams', 'Other'];

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      // Mock profile data
      const mockProfile = {
        name: getStudentName(),
        email: 'alex@student.com',
        age: '16',
        learningStyle: 'visual',
        targetExams: ['WASSCE', 'SAT'],
        academicGoals: 'Achieve excellent grades in mathematics and science subjects',
        examDate: '2024-06-15'
      };
      
      setFormData(mockProfile);
    } catch (error) {
      toast.error('Failed to load profile data');
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleExamToggle = (exam) => {
    setFormData(prev => ({
      ...prev,
      targetExams: prev.targetExams.includes(exam)
        ? prev.targetExams.filter(e => e !== exam)
        : [...prev.targetExams, exam]
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      setLoading(true);
      toast.info('Updating your profile...');
      
      // Mock API call
      console.log('Profile update:', formData);
      
      toast.success('Profile updated successfully!');
      navigate('/student/dashboard');
      
    } catch (error) {
      toast.error('Failed to update profile. Please try again.');
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
              <h1 className="text-xl font-bold text-white">Profile Settings</h1>
              <p className="text-white/80 text-sm">Manage your learning preferences</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 py-8">
        {/* Profile Header */}
        <div className="glass-card p-8 mb-8">
          <div className="flex flex-col md:flex-row items-center space-y-6 md:space-y-0 md:space-x-8">
            <div className="relative">
              <div className="w-32 h-32 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white text-4xl font-bold">
                {formData.name.charAt(0).toUpperCase()}
              </div>
              <button className="absolute bottom-2 right-2 glass-button p-2 bg-white/90 hover:bg-white">
                <Camera className="h-4 w-4 text-gray-600" />
              </button>
            </div>
            <div className="text-center md:text-left flex-1">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">{formData.name}</h1>
              <p className="text-gray-600 mb-4">{formData.email}</p>
              <div className="flex flex-wrap gap-2 justify-center md:justify-start">
                <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                  <Star className="h-3 w-3 inline mr-1" />
                  Level: Intermediate
                </span>
                <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                  <Award className="h-3 w-3 inline mr-1" />
                  85% Average
                </span>
                <span className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm font-medium">
                  <Clock className="h-3 w-3 inline mr-1" />
                  12 Day Streak
                </span>
              </div>
            </div>
          </div>
        </div>
        <form onSubmit={handleSubmit} className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-8">
          {/* Personal Information */}
          <div className="glass-card p-8">
            <div className="flex items-center space-x-3 mb-6">
              <User className="h-6 w-6 text-blue-600" />
              <h2 className="text-xl font-semibold text-gray-900">Personal Information</h2>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Full Name</label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className="glass-input w-full px-4 py-3 text-gray-900"
                  placeholder="Enter your full name"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="glass-input w-full px-4 py-3 text-gray-900"
                  placeholder="Enter your email"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Age</label>
                <input
                  type="number"
                  name="age"
                  value={formData.age}
                  onChange={handleChange}
                  className="glass-input w-full px-4 py-3 text-gray-900"
                  placeholder="Enter your age"
                  min="10"
                  max="100"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Target Exam Date</label>
                <input
                  type="date"
                  name="examDate"
                  value={formData.examDate}
                  onChange={handleChange}
                  className="glass-input w-full px-4 py-3 text-gray-900"
                />
              </div>
            </div>
          </div>

          {/* Learning Preferences */}
          <div className="glass-card p-8">
            <div className="flex items-center space-x-3 mb-6">
              <BookOpen className="h-6 w-6 text-green-600" />
              <h2 className="text-xl font-semibold text-gray-900">Learning Preferences</h2>
            </div>
            
            <div className="space-y-6">
              {/* Learning Style */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-4">Learning Style</label>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {learningStyles.map(style => (
                    <label key={style.id} className="glass-card p-4 cursor-pointer hover-lift">
                      <input
                        type="radio"
                        name="learningStyle"
                        value={style.id}
                        checked={formData.learningStyle === style.id}
                        onChange={handleChange}
                        className="sr-only"
                      />
                      <div className={`flex items-start space-x-3 ${formData.learningStyle === style.id ? 'text-blue-600' : 'text-gray-700'}`}>
                        <div className={`w-4 h-4 rounded-full border-2 mt-1 ${formData.learningStyle === style.id ? 'border-blue-600 bg-blue-600' : 'border-gray-300'}`}>
                          {formData.learningStyle === style.id && <div className="w-2 h-2 bg-white rounded-full m-0.5"></div>}
                        </div>
                        <div>
                          <div className="font-medium">{style.label}</div>
                          <div className="text-sm text-gray-500">{style.desc}</div>
                        </div>
                      </div>
                    </label>
                  ))}
                </div>
              </div>

              {/* Target Exams */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-4">Target Exams</label>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  {examOptions.map(exam => (
                    <button
                      key={exam}
                      type="button"
                      onClick={() => handleExamToggle(exam)}
                      className={`glass-card p-3 text-sm font-medium transition-all ${
                        formData.targetExams.includes(exam)
                          ? 'bg-gradient-primary text-white'
                          : 'text-gray-700 hover:bg-white/50'
                      }`}
                    >
                      {exam}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Academic Goals */}
          <div className="glass-card p-8">
            <div className="flex items-center space-x-3 mb-6">
              <Target className="h-6 w-6 text-purple-600" />
              <h2 className="text-xl font-semibold text-gray-900">Academic Goals</h2>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Describe Your Goals</label>
              <textarea
                name="academicGoals"
                value={formData.academicGoals}
                onChange={handleChange}
                className="glass-input w-full px-4 py-3 text-gray-900"
                rows={4}
                placeholder="Describe your academic goals and what you want to achieve..."
              />
            </div>
          </div>

          </div>

          {/* Right Sidebar */}
          <div className="space-y-6">
            <div className="glass-card p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Learning Stats</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Completed Lessons</span>
                  <span className="font-semibold text-blue-600">24/48</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Average Score</span>
                  <span className="font-semibold text-green-600">85%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Study Streak</span>
                  <span className="font-semibold text-orange-600">12 days</span>
                </div>
              </div>
            </div>

            <div className="space-y-3">
              <button
                type="submit"
                disabled={loading}
                className="w-full glass-button bg-gradient-primary text-white hover-lift py-4"
              >
                {loading ? (
                  <div className="spinner w-5 h-5 mx-auto"></div>
                ) : (
                  <>
                    <Save className="h-5 w-5 mr-2" />
                    Save Changes
                  </>
                )}
              </button>
              <button
                type="button"
                onClick={() => navigate('/student/dashboard')}
                className="w-full glass-button text-gray-700 hover:bg-white/50"
              >
                <ArrowLeft className="h-4 w-4 mr-2" />
                Back to Dashboard
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default StudentProfile;