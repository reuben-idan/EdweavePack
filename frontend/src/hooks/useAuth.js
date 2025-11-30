import { useState, useEffect, createContext, useContext } from 'react';
import { authAPI } from '../services/api';
import { ENABLE_LOGGING } from '../config';

// Secure logging function
const secureLog = (message) => {
  if (ENABLE_LOGGING) {
    console.log(message);
  }
};

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      authAPI.getProfile()
        .then(response => setUser(response.data))
        .catch(() => localStorage.removeItem('token'))
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (credentials) => {
    let retries = 3;
    let lastError;
    
    while (retries > 0) {
      try {
        const formData = new URLSearchParams();
        formData.append('username', credentials.email?.trim());
        formData.append('password', credentials.password);
        
        const response = await authAPI.login(formData);
        const { access_token } = response.data;
        
        localStorage.setItem('token', access_token);
        
        // Get user profile with retry
        let profileRetries = 2;
        let userResponse;
        
        while (profileRetries > 0) {
          try {
            userResponse = await authAPI.getProfile();
            break;
          } catch (profileError) {
            profileRetries--;
            if (profileRetries === 0) throw profileError;
            await new Promise(resolve => setTimeout(resolve, 1000));
          }
        }
        
        setUser(userResponse.data);
        return userResponse.data;
        
      } catch (error) {
        lastError = error;
        retries--;
        
        // Don't retry on auth errors
        if (error.response?.status && [401, 403].includes(error.response.status)) {
          throw error;
        }
        
        if (retries === 0) throw error;
        
        console.log(`Login attempt failed, retrying... (${retries} attempts left)`);
        await new Promise(resolve => setTimeout(resolve, 1000 * (4 - retries)));
      }
    }
    
    throw lastError;
  };

  const register = async (userData) => {
    let retries = 3;
    let lastError;
    
    while (retries > 0) {
      try {
        // Validate user data before sending
        const validatedData = {
          email: userData.email?.trim(),
          password: userData.password,
          full_name: userData.full_name?.trim(),
          institution: userData.institution?.trim(),
          role: userData.role || 'teacher'
        };
        
        secureLog('Processing registration request');
        const response = await authAPI.register(validatedData);
        secureLog('Registration completed successfully');
        
        const { access_token } = response.data;
        
        localStorage.setItem('token', access_token);
        
        // Get user profile with retry
        let profileRetries = 2;
        let userResponse;
        
        while (profileRetries > 0) {
          try {
            userResponse = await authAPI.getProfile();
            break;
          } catch (profileError) {
            profileRetries--;
            if (profileRetries === 0) throw profileError;
            await new Promise(resolve => setTimeout(resolve, 1000));
          }
        }
        
        setUser(userResponse.data);
        return userResponse.data;
        
      } catch (error) {
        lastError = error;
        retries--;
        
        // Don't retry on validation errors (400) or auth errors (401, 403)
        if (error.response?.status && [400, 401, 403].includes(error.response.status)) {
          secureLog('Registration validation error');
          throw error;
        }
        
        // Don't retry if no more attempts
        if (retries === 0) {
          secureLog('Registration failed after all retries');
          throw error;
        }
        
        // Wait before retry
        secureLog(`Registration attempt failed, retrying... (${retries} attempts left)`);
        await new Promise(resolve => setTimeout(resolve, 1000 * (4 - retries)));
      }
    }
    
    throw lastError;
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  const updateProfile = async (profileData) => {
    try {
      const response = await authAPI.updateProfile(profileData);
      if (response.data?.user) {
        setUser(response.data.user);
      }
      return { success: true };
    } catch (error) {
      console.error('Profile update failed:', error);
      return { success: false, error: error.message };
    }
  };

  const changePassword = async (passwordData) => {
    try {
      await authAPI.updatePassword(passwordData);
      return { success: true };
    } catch (error) {
      console.error('Password change failed:', error);
      return { success: false, error: error.message };
    }
  };

  const value = {
    user,
    login,
    register,
    logout,
    updateProfile,
    changePassword,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};