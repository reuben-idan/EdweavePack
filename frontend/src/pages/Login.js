import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { toast } from 'react-toastify';
import { Eye, EyeOff, Mail, Lock, ArrowRight } from 'lucide-react';

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

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
      
      const userData = await login(formData);
      toast.success('Welcome back to EdweavePack!');
      
      // Navigate based on user role
      if (userData.role === 'student') {
        navigate('/student/dashboard');
      } else {
        navigate('/dashboard');
      }
      
    } catch (error) {
      toast.error('Invalid credentials. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen animated-gradient flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        {/* Logo and Header */}
        <div className="text-center">
          <div className="flex justify-center mb-6">
            <img 
              src="/images/Edweave Pack Logo.png" 
              alt="EdweavePack" 
              className="h-16 w-16 rounded-2xl float pulse-glow"
            />
          </div>
          <h2 className="text-3xl font-bold text-white mb-2">
            Welcome Back
          </h2>
          <p className="text-white/80">
            Sign in to your EdweavePack account
          </p>
        </div>

        {/* Login Form */}
        <div className="glass-card p-8">
          <form className="space-y-6" onSubmit={handleSubmit}>
            {/* Email Field */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                Email Address
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Mail className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={formData.email}
                  onChange={handleChange}
                  className="glass-input w-full pl-10 pr-4 py-3 text-gray-900 placeholder-gray-500"
                  placeholder="Enter your email"
                />
              </div>
            </div>

            {/* Password Field */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  autoComplete="current-password"
                  required
                  value={formData.password}
                  onChange={handleChange}
                  className="glass-input w-full pl-10 pr-12 py-3 text-gray-900 placeholder-gray-500"
                  placeholder="Enter your password"
                />
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? (
                    <EyeOff className="h-5 w-5 text-gray-400 hover:text-gray-600" />
                  ) : (
                    <Eye className="h-5 w-5 text-gray-400 hover:text-gray-600" />
                  )}
                </button>
              </div>
            </div>

            {/* Submit Button */}
            <div>
              <button
                type="submit"
                disabled={loading}
                className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-xl text-white bg-gradient-primary hover:scale-105 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300"
              >
                {loading ? (
                  <div className="spinner w-5 h-5"></div>
                ) : (
                  <>
                    <span>Sign In</span>
                    <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                  </>
                )}
              </button>
            </div>

            {/* Links */}
            <div className="space-y-4">
              <div className="text-center">
                <Link
                  to="/forgot-password"
                  className="text-sm text-indigo-600 hover:text-indigo-500 font-medium transition-colors"
                >
                  Forgot your password?
                </Link>
              </div>
              <div className="text-center">
                <p className="text-sm text-gray-600">
                  Don't have an account?{' '}
                  <Link
                    to="/register"
                    className="font-medium text-indigo-600 hover:text-indigo-500 transition-colors"
                  >
                    Create one now
                  </Link>
                </p>
              </div>
            </div>
          </form>
        </div>

        {/* Features Preview */}
        <div className="glass-card p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 text-center">
            What's New in EdweavePack
          </h3>
          <div className="space-y-3">
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 bg-gradient-primary rounded-full"></div>
              <span className="text-sm text-gray-600">AI-powered curriculum generation</span>
            </div>
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 bg-gradient-secondary rounded-full"></div>
              <span className="text-sm text-gray-600">Smart assessment creation</span>
            </div>
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 bg-gradient-success rounded-full"></div>
              <span className="text-sm text-gray-600">Real-time analytics dashboard</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;