import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { Eye, EyeOff, Mail, Lock, ArrowRight, BookOpen } from 'lucide-react';

const StudentLogin = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.email || !formData.password) {
      toast.error('Please fill in all fields');
      return;
    }

    try {
      setLoading(true);
      toast.info('Signing you in...');
      
      // Mock API call
      console.log('Student login:', formData);
      
      toast.success('Welcome back! Let\'s continue learning.');
      navigate('/student/dashboard');
      
    } catch (error) {
      toast.error('Invalid credentials. Please try again.');
    } finally {
      setLoading(false);
    }
  };

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
                  className="glass-input w-full pl-10 pr-4 py-3 text-gray-900"
                  placeholder="Enter your email"
                  required
                />
              </div>
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
                  className="glass-input w-full pl-10 pr-12 py-3 text-gray-900"
                  placeholder="Enter your password"
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

            <button
              type="submit"
              disabled={loading}
              className="w-full glass-button bg-gradient-primary text-white hover-lift"
            >
              {loading ? (
                <div className="spinner w-5 h-5 mx-auto"></div>
              ) : (
                <>
                  <span>Sign In</span>
                  <ArrowRight className="ml-2 h-4 w-4" />
                </>
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