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
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-center space-x-4">
            <button
              onClick={() => navigate('/student/dashboard')}
              className="glass-button p-3 hover:scale-105 transition-all duration-300"
            >
              <ArrowLeft className="h-5 w-5" style={{color: 'var(--text-primary)'}} />
            </button>
            <div>
              <h1 className="text-xl font-bold" style={{color: 'var(--text-primary)'}}>Profile Settings</h1>
              <p className="text-sm font-medium" style={{color: 'var(--text-secondary)'}}>Manage your learning preferences</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 py-8">
        {/* Profile Header */}
        <div className="edu-card p-8 mb-8 animate-slide-up">
          <div className="flex flex-col md:flex-row items-center space-y-6 md:space-y-0 md:space-x-8">
            <div className="relative">
              <div className="w-32 h-32 bg-gradient-primary rounded-3xl flex items-center justify-center text-white text-4xl font-bold shadow-edu-lg">
                {formData.name.charAt(0).toUpperCase()}
              </div>
              <button className="absolute bottom-2 right-2 p-3 glass-button rounded-full hover:scale-110 transition-all duration-300">
                <Camera className="h-4 w-4 text-accent" />
              </button>
            </div>
            <div className="text-center md:text-left flex-1">
              <h1 className="text-3xl font-bold mb-2" style={{color: 'var(--text-primary)'}}>{formData.name}</h1>
              <p className="font-medium mb-4" style={{color: 'var(--text-secondary)'}}>{formData.email}</p>
              <div className="flex flex-wrap gap-3 justify-center md:justify-start">
                <span className="edu-button px-4 py-2 rounded-full text-sm font-semibold">
                  <Star className="h-4 w-4 inline mr-2" />
                  Level: Intermediate
                </span>
                <span className="edu-button-success px-4 py-2 rounded-full text-sm font-semibold">
                  <Award className="h-4 w-4 inline mr-2" />
                  85% Average
                </span>
                <span className="edu-button-secondary px-4 py-2 rounded-full text-sm font-semibold">
                  <Clock className="h-4 w-4 inline mr-2" />
                  12 Day Streak
                </span>
              </div>
            </div>
          </div>
        </div>
        <form onSubmit={handleSubmit} className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-8">
          {/* Personal Information */}
          <div className="edu-card p-8 animate-slide-up">
            <div className="flex items-center space-x-4 mb-8">
              <div className="edu-icon edu-icon-primary">
                <User className="h-6 w-6 text-white" />
              </div>
              <h2 className="text-2xl font-bold" style={{color: 'var(--text-primary)'}}>Personal Information</h2>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="edu-label">Full Name</label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className="edu-input"
                  placeholder="Enter your full name"
                  required
                />
              </div>

              <div>
                <label className="edu-label">Email Address</label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="edu-input"
                  placeholder="Enter your email"
                  required
                />
              </div>

              <div>
                <label className="edu-label">Age</label>
                <input
                  type="number"
                  name="age"
                  value={formData.age}
                  onChange={handleChange}
                  className="edu-input"
                  placeholder="Enter your age"
                  min="10"
                  max="100"
                />
              </div>

              <div>
                <label className="edu-label">Target Exam Date</label>
                <input
                  type="date"
                  name="examDate"
                  value={formData.examDate}
                  onChange={handleChange}
                  className="edu-input"
                />
              </div>
            </div>
          </div>

          {/* Learning Preferences */}
          <div className="edu-card p-8 animate-slide-up">
            <div className="flex items-center space-x-4 mb-8">
              <div className="edu-icon edu-icon-success">
                <BookOpen className="h-6 w-6 text-white" />
              </div>
              <h2 className="text-2xl font-bold" style={{color: 'var(--text-primary)'}}>Learning Preferences</h2>
            </div>
            
            <div className="space-y-6">
              {/* Learning Style */}
              <div>
                <label className="edu-label text-lg mb-6">Learning Style</label>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {learningStyles.map(style => (
                    <label key={style.id} className={`glass-card p-6 cursor-pointer transition-all duration-300 ${
                      formData.learningStyle === style.id 
                        ? 'border-2 border-edu-primary shadow-edu-lg transform scale-105' 
                        : 'hover:shadow-edu'
                    }`}>
                      <input
                        type="radio"
                        name="learningStyle"
                        value={style.id}
                        checked={formData.learningStyle === style.id}
                        onChange={handleChange}
                        className="sr-only"
                      />
                      <div className="flex items-start space-x-4" style={{color: formData.learningStyle === style.id ? 'var(--edu-primary)' : 'var(--text-primary)'}}>
                        <div className={`w-6 h-6 rounded-full border-2 mt-1 flex items-center justify-center transition-all ${
                          formData.learningStyle === style.id 
                            ? 'border-edu-primary bg-gradient-primary' 
                            : 'border-gray-300'
                        }`}>
                          {formData.learningStyle === style.id && <div className="w-3 h-3 bg-white rounded-full"></div>}
                        </div>
                        <div>
                          <div className="font-bold text-lg">{style.label}</div>
                          <div className="text-sm font-medium" style={{color: 'var(--text-secondary)'}}>{style.desc}</div>
                        </div>
                      </div>
                    </label>
                  ))}
                </div>
              </div>

              {/* Target Exams */}
              <div>
                <label className="edu-label text-lg mb-6">Target Exams</label>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  {examOptions.map(exam => (
                    <button
                      key={exam}
                      type="button"
                      onClick={() => handleExamToggle(exam)}
                      className={`p-4 text-base font-bold transition-all duration-300 rounded-2xl ${
                        formData.targetExams.includes(exam)
                          ? 'edu-button transform scale-105'
                          : 'glass-button hover:scale-105'
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
          <div className="edu-card p-8 animate-slide-up">
            <div className="flex items-center space-x-4 mb-8">
              <div className="edu-icon edu-icon-secondary">
                <Target className="h-6 w-6 text-white" />
              </div>
              <h2 className="text-2xl font-bold" style={{color: 'var(--text-primary)'}}>Academic Goals</h2>
            </div>
            
            <div>
              <label className="edu-label">Describe Your Goals</label>
              <textarea
                name="academicGoals"
                value={formData.academicGoals}
                onChange={handleChange}
                className="edu-input resize-none"
                rows={5}
                placeholder="Describe your academic goals and what you want to achieve..."
              />
            </div>
          </div>

          </div>

          {/* Right Sidebar */}
          <div className="space-y-6">
            <div className="edu-card p-6 animate-bounce-in">
              <h3 className="text-xl font-bold mb-6" style={{color: 'var(--text-primary)'}}>Learning Stats</h3>
              <div className="space-y-4">
                <div className="edu-button p-4 rounded-2xl flex items-center justify-between">
                  <span className="font-bold text-white">Completed Lessons</span>
                  <span className="font-bold text-white text-xl">24/48</span>
                </div>
                <div className="edu-button-success p-4 rounded-2xl flex items-center justify-between">
                  <span className="font-bold text-white">Average Score</span>
                  <span className="font-bold text-white text-xl">85%</span>
                </div>
                <div className="edu-button-warning p-4 rounded-2xl flex items-center justify-between">
                  <span className="font-bold text-white">Study Streak</span>
                  <span className="font-bold text-white text-xl">12 days</span>
                </div>
              </div>
            </div>

            <div className="space-y-3">
              <button
                type="submit"
                disabled={loading}
                className="w-full edu-button py-4 font-bold rounded-2xl transition-all duration-300 hover:scale-105"
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
                className="w-full glass-button py-3 font-medium rounded-2xl transition-all duration-300 hover:scale-105"
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