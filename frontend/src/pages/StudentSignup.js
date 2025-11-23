import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { Eye, EyeOff, Mail, Lock, User, Calendar, Target, BookOpen } from 'lucide-react';

const StudentSignup = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    age: '',
    learningStyle: '',
    targetExams: [],
    academicGoals: '',
    examDate: ''
  });
  const [showPassword, setShowPassword] = useState(false);

  const learningStyles = [
    { id: 'visual', label: 'Visual', desc: 'Learn through images, diagrams, and charts' },
    { id: 'auditory', label: 'Auditory', desc: 'Learn through listening and discussion' },
    { id: 'reading', label: 'Reading/Writing', desc: 'Learn through text and written materials' },
    { id: 'kinesthetic', label: 'Kinesthetic', desc: 'Learn through hands-on activities' }
  ];

  const examOptions = ['BECE', 'WASSCE', 'SAT', 'IGCSE', 'University Exams', 'Other'];

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

  const handleNext = () => {
    if (step === 1) {
      if (!formData.name || !formData.email || !formData.password) {
        toast.error('Please fill in all required fields');
        return;
      }
      if (formData.password !== formData.confirmPassword) {
        toast.error('Passwords do not match');
        return;
      }
      if (formData.password.length < 6) {
        toast.error('Password must be at least 6 characters');
        return;
      }
    }
    setStep(step + 1);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.learningStyle || formData.targetExams.length === 0) {
      toast.error('Please complete your learning profile');
      return;
    }

    try {
      setLoading(true);
      toast.info('Creating your student account...');
      
      // Mock API call
      console.log('Student signup:', formData);
      
      toast.success('Welcome to EdweavePack! Your student account is ready.');
      navigate('/student/dashboard');
      
    } catch (error) {
      toast.error('Failed to create account. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen animated-gradient flex items-center justify-center py-12 px-4">
      <div className="max-w-2xl w-full">
        {/* Header */}
        <div className="text-center mb-8">
          <img 
            src="/images/Edweave Pack Logo.png" 
            alt="EdweavePack" 
            className="h-16 w-16 rounded-2xl float pulse-glow mx-auto mb-6"
          />
          <h2 className="text-3xl font-bold text-white mb-2">Join as Student</h2>
          <p className="text-white/80">Create your personalized learning journey</p>
        </div>

        {/* Progress Indicator */}
        <div className="glass-card p-4 mb-8">
          <div className="flex items-center justify-between">
            <div className={`flex items-center space-x-2 ${step >= 1 ? 'text-blue-600' : 'text-gray-400'}`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${step >= 1 ? 'bg-gradient-primary text-white' : 'bg-gray-200'}`}>1</div>
              <span className="text-sm font-medium">Account Info</span>
            </div>
            <div className="flex-1 h-1 mx-4 bg-gray-200 rounded">
              <div className={`h-1 bg-gradient-primary rounded transition-all duration-300 ${step >= 2 ? 'w-full' : 'w-0'}`}></div>
            </div>
            <div className={`flex items-center space-x-2 ${step >= 2 ? 'text-blue-600' : 'text-gray-400'}`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${step >= 2 ? 'bg-gradient-primary text-white' : 'bg-gray-200'}`}>2</div>
              <span className="text-sm font-medium">Learning Profile</span>
            </div>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Step 1: Account Information */}
          {step === 1 && (
            <div className="glass-card p-8 space-y-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-6">Account Information</h3>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Full Name</label>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    className="glass-input w-full pl-10 pr-4 py-3 text-gray-900"
                    placeholder="Enter your full name"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    className="glass-input w-full pl-10 pr-4 py-3 text-gray-900"
                    placeholder="Enter your email"
                    required
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Password</label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                    <input
                      type={showPassword ? 'text' : 'password'}
                      name="password"
                      value={formData.password}
                      onChange={handleChange}
                      className="glass-input w-full pl-10 pr-12 py-3 text-gray-900"
                      placeholder="Create password"
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-1/2 transform -translate-y-1/2"
                    >
                      {showPassword ? <EyeOff className="h-5 w-5 text-gray-400" /> : <Eye className="h-5 w-5 text-gray-400" />}
                    </button>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Confirm Password</label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                    <input
                      type="password"
                      name="confirmPassword"
                      value={formData.confirmPassword}
                      onChange={handleChange}
                      className="glass-input w-full pl-10 pr-4 py-3 text-gray-900"
                      placeholder="Confirm password"
                      required
                    />
                  </div>
                </div>
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

              <button
                type="button"
                onClick={handleNext}
                className="w-full glass-button bg-gradient-primary text-white hover-lift"
              >
                Continue to Learning Profile
              </button>
            </div>
          )}

          {/* Step 2: Learning Profile */}
          {step === 2 && (
            <div className="glass-card p-8 space-y-8">
              <h3 className="text-xl font-semibold text-gray-900 mb-6">Learning Profile</h3>
              
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
                <label className="block text-sm font-medium text-gray-700 mb-4">Target Exams (Select all that apply)</label>
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

              {/* Academic Goals */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Academic Goals</label>
                <textarea
                  name="academicGoals"
                  value={formData.academicGoals}
                  onChange={handleChange}
                  className="glass-input w-full px-4 py-3 text-gray-900"
                  rows={3}
                  placeholder="Describe your academic goals and what you want to achieve..."
                />
              </div>

              {/* Exam Date */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Target Exam Date (Optional)</label>
                <div className="relative">
                  <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                  <input
                    type="date"
                    name="examDate"
                    value={formData.examDate}
                    onChange={handleChange}
                    className="glass-input w-full pl-10 pr-4 py-3 text-gray-900"
                  />
                </div>
              </div>

              <div className="flex space-x-4">
                <button
                  type="button"
                  onClick={() => setStep(1)}
                  className="flex-1 glass-button text-gray-700 hover:bg-white/50"
                >
                  Back
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="flex-1 glass-button bg-gradient-primary text-white hover-lift"
                >
                  {loading ? <div className="spinner w-5 h-5 mx-auto"></div> : 'Create Account'}
                </button>
              </div>
            </div>
          )}
        </form>

        {/* Login Link */}
        <div className="glass-card p-6 text-center mt-6">
          <p className="text-sm text-gray-600">
            Already have a student account?{' '}
            <Link to="/student/login" className="font-medium text-indigo-600 hover:text-indigo-500">
              Sign in here
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default StudentSignup;