import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { Eye, EyeOff, Mail, Lock, ArrowRight, BookOpen, AlertCircle, CheckCircle } from 'lucide-react';
import { useStudentAuth } from '../hooks/useStudentAuth';
import { setStudentName } from '../utils/studentUtils';

const StudentLogin = () => {
  const navigate = useNavigate();
  const { login, loading, isAuthenticated } = useStudentAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [errors, setErrors] = useState({});
  const [rememberMe, setRememberMe] = useState(false);
  
  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/student/dashboard');
    }
  }, [isAuthenticated, navigate]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }
    
    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      toast.error('Please fix the errors below');
      return;
    }

    const result = await login(formData);
    
    if (result.success) {
      // Extract name from email or set default
      const studentName = formData.email.split('@')[0].replace(/[._]/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
      setStudentName(studentName);
      
      // Save remember me preference
      if (rememberMe) {
        localStorage.setItem('rememberStudentEmail', formData.email);
      } else {
        localStorage.removeItem('rememberStudentEmail');
      }
      
      navigate('/student/dashboard');
    }
  };
  
  // Load remembered email on component mount
  useEffect(() => {
    const rememberedEmail = localStorage.getItem('rememberStudentEmail');
    if (rememberedEmail) {
      setFormData(prev => ({ ...prev, email: rememberedEmail }));
      setRememberMe(true);
    }
  }, []);

  return (
    <div className="min-h-screen animated-gradient flex items-center justify-center py-12 px-4">
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <div className="text-center">
          <img 
            src="/images/Edweave Pack Logo.png" 
            alt="EdweavePack" 
            className="h-16 w-16 rounded-2xl float pulse-glow mx-auto mb-6"
          />
          <h2 className="text-3xl font-bold text-white mb-2">Student Portal</h2>
          <p className="text-white/80">Sign in to continue your learning journey</p>
        </div>

        {/* Login Form */}
        <div className="glass-card p-8">
          <form className="space-y-6" onSubmit={handleSubmit}>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className={`glass-input w-full pl-10 pr-4 py-3 text-gray-900 ${
                    errors.email ? 'border-red-500 focus:border-red-500' : ''
                  }`}
                  placeholder="Enter your student email"
                  autoComplete="email"
                />
                {errors.email && (
                  <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                    <AlertCircle className="h-5 w-5 text-red-500" />
                  </div>
                )}
              </div>
              {errors.email && (
                <p className="mt-1 text-sm text-red-600 flex items-center">
                  <AlertCircle className="h-4 w-4 mr-1" />
                  {errors.email}
                </p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  className={`glass-input w-full pl-10 pr-12 py-3 text-gray-900 ${
                    errors.password ? 'border-red-500 focus:border-red-500' : ''
                  }`}
                  placeholder="Enter your password"
                  autoComplete="current-password"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2"
                >
                  {showPassword ? <EyeOff className="h-5 w-5 text-gray-400" /> : <Eye className="h-5 w-5 text-gray-400" />}
                </button>
              </div>
              {errors.password && (
                <p className="mt-1 text-sm text-red-600 flex items-center">
                  <AlertCircle className="h-4 w-4 mr-1" />
                  {errors.password}
                </p>
              )}
            </div>
            
            {/* Remember Me & Forgot Password */}
            <div className="flex items-center justify-between">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  className="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
                />
                <span className="ml-2 text-sm text-gray-600">Remember me</span>
              </label>
              <Link
                to="/student/forgot-password"
                className="text-sm text-blue-600 hover:text-blue-500 font-medium"
              >
                Forgot password?
              </Link>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full glass-button bg-gradient-primary text-white hover-lift disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
            >
              {loading ? (
                <div className="flex items-center justify-center">
                  <div className="spinner w-5 h-5 mr-2"></div>
                  <span>Signing you in...</span>
                </div>
              ) : (
                <div className="flex items-center justify-center">
                  <span>Sign In to Student Portal</span>
                  <ArrowRight className="ml-2 h-4 w-4" />
                </div>
              )}
            </button>
          </form>
        </div>

        {/* Links */}
        <div className="glass-card p-6 space-y-4">
          <div className="text-center">
            <p className="text-sm text-gray-600">
              New to EdweavePack?{' '}
              <Link to="/student/signup" className="font-medium text-indigo-600 hover:text-indigo-500">
                Create student account
              </Link>
            </p>
          </div>
          
          <div className="text-center border-t border-gray-200 pt-4">
            <p className="text-sm text-gray-600">
              Are you a teacher?{' '}
              <Link to="/login" className="font-medium text-indigo-600 hover:text-indigo-500">
                Teacher Portal
              </Link>
            </p>
          </div>
        </div>

        {/* Student Benefits */}
        <div className="glass-card p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 text-center">
            Your Learning Journey Awaits
          </h3>
          <div className="space-y-3">
            <div className="flex items-center space-x-3">
              <BookOpen className="h-5 w-5 text-blue-600" />
              <span className="text-sm text-gray-600">Personalized learning paths</span>
            </div>
            <div className="flex items-center space-x-3">
              <div className="w-5 h-5 bg-gradient-success rounded-full flex items-center justify-center">
                <div className="w-2 h-2 bg-white rounded-full"></div>
              </div>
              <span className="text-sm text-gray-600">Track your progress</span>
            </div>
            <div className="flex items-center space-x-3">
              <div className="w-5 h-5 bg-gradient-secondary rounded-full flex items-center justify-center">
                <div className="w-2 h-2 bg-white rounded-full"></div>
              </div>
              <span className="text-sm text-gray-600">Practice with AI-generated questions</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StudentLogin;