import React, { createContext, useContext, useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import { authAPI } from '../services/api';

const StudentAuthContext = createContext();

export const useStudentAuth = () => {
  const context = useContext(StudentAuthContext);
  if (!context) {
    throw new Error('useStudentAuth must be used within a StudentAuthProvider');
  }
  return context;
};

export const StudentAuthProvider = ({ children }) => {
  const [student, setStudent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const token = localStorage.getItem('studentToken');
      if (token) {
        // Verify token with backend
        const response = await authAPI.getProfile();
        if (response.data) {
          setStudent(response.data);
          setIsAuthenticated(true);
        } else {
          // Invalid token
          localStorage.removeItem('studentToken');
          setStudent(null);
          setIsAuthenticated(false);
        }
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      localStorage.removeItem('studentToken');
      setStudent(null);
      setIsAuthenticated(false);
    } finally {
      setLoading(false);
    }
  };

  const login = async (credentials) => {
    try {
      setLoading(true);
      
      // Convert to form data for OAuth2
      const formData = new URLSearchParams();
      formData.append('username', credentials.email);
      formData.append('password', credentials.password);

      const response = await authAPI.login(formData);
      
      if (response.data && response.data.access_token) {
        localStorage.setItem('studentToken', response.data.access_token);
        
        // Get student profile
        const profileResponse = await authAPI.getProfile();
        if (profileResponse.data) {
          setStudent(profileResponse.data);
          setIsAuthenticated(true);
          toast.success('Welcome back! Ready to continue learning?');
          return { success: true };
        } else {
          throw new Error('Invalid account');
        }
      } else {
        throw new Error('Invalid response from server');
      }
    } catch (error) {
      console.error('Login failed:', error);
      const errorMessage = error.response?.data?.detail || 'Login failed. Please check your credentials.';
      toast.error(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const register = async (studentData) => {
    try {
      setLoading(true);
      
      const registrationData = {
        email: studentData.email,
        password: studentData.password,
        full_name: studentData.name,
        role: 'student',
        institution: 'Student Portal',
        // Additional student-specific data
        age: studentData.age,
        learning_style: studentData.learningStyle,
        target_exams: studentData.targetExams,
        academic_goals: studentData.academicGoals,
        exam_date: studentData.examDate
      };

      const response = await authAPI.register(registrationData);
      
      if (response.data && response.data.access_token) {
        localStorage.setItem('studentToken', response.data.access_token);
        
        // Get student profile
        const profileResponse = await authAPI.getProfile();
        if (profileResponse.data) {
          setStudent(profileResponse.data);
          setIsAuthenticated(true);
          toast.success('Welcome to EdweavePack! Your learning journey begins now.');
          return { success: true };
        }
      }
      
      throw new Error('Registration failed');
    } catch (error) {
      console.error('Registration failed:', error);
      const errorMessage = error.response?.data?.detail || 'Registration failed. Please try again.';
      toast.error(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const updateProfile = async (profileData) => {
    try {
      setLoading(true);
      
      const response = await authAPI.updateProfile({
        fullName: profileData.name,
        email: profileData.email,
        institution: 'Student Portal'
      });
      
      if (response.data && response.data.user) {
        setStudent(response.data.user);
        toast.success('Profile updated successfully!');
        return { success: true };
      }
      
      throw new Error('Profile update failed');
    } catch (error) {
      console.error('Profile update failed:', error);
      const errorMessage = error.response?.data?.detail || 'Failed to update profile.';
      toast.error(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const changePassword = async (passwordData) => {
    try {
      setLoading(true);
      
      const response = await authAPI.updatePassword({
        current_password: passwordData.currentPassword,
        new_password: passwordData.newPassword
      });
      
      if (response.data) {
        toast.success('Password updated successfully!');
        return { success: true };
      }
      
      throw new Error('Password update failed');
    } catch (error) {
      console.error('Password update failed:', error);
      const errorMessage = error.response?.data?.detail || 'Failed to update password.';
      toast.error(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('studentToken');
    setStudent(null);
    setIsAuthenticated(false);
    toast.success('Logged out successfully');
  };

  const forgotPassword = async (email) => {
    try {
      setLoading(true);
      
      const response = await authAPI.forgotPassword({ email });
      
      if (response.data) {
        toast.success('Password reset instructions sent to your email');
        return { success: true };
      }
      
      throw new Error('Failed to send reset email');
    } catch (error) {
      console.error('Forgot password failed:', error);
      const errorMessage = error.response?.data?.detail || 'Failed to send reset email.';
      toast.error(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const resetPassword = async (token, newPassword) => {
    try {
      setLoading(true);
      
      const response = await authAPI.resetPassword({
        token,
        password: newPassword
      });
      
      if (response.data) {
        toast.success('Password reset successfully! You can now log in.');
        return { success: true };
      }
      
      throw new Error('Password reset failed');
    } catch (error) {
      console.error('Password reset failed:', error);
      const errorMessage = error.response?.data?.detail || 'Password reset failed.';
      toast.error(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const value = {
    student,
    loading,
    isAuthenticated,
    login,
    register,
    updateProfile,
    changePassword,
    logout,
    forgotPassword,
    resetPassword,
    checkAuthStatus
  };

  return (
    <StudentAuthContext.Provider value={value}>
      {children}
    </StudentAuthContext.Provider>
  );
};

export default StudentAuthProvider;