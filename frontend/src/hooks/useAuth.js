import { useState, useEffect, createContext, useContext } from 'react';
import { authAPI } from '../services/api';

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
    const formData = new URLSearchParams();
    formData.append('username', credentials.email);
    formData.append('password', credentials.password);
    
    const response = await authAPI.login(formData);
    const { access_token } = response.data;
    
    localStorage.setItem('token', access_token);
    const userResponse = await authAPI.getProfile();
    setUser(userResponse.data);
    
    return userResponse.data;
  };

  const register = async (userData) => {
    try {
      console.log('Registering user with data:', userData);
      const response = await authAPI.register(userData);
      console.log('Registration response:', response.data);
      
      const { access_token } = response.data;
      
      localStorage.setItem('token', access_token);
      const userResponse = await authAPI.getProfile();
      setUser(userResponse.data);
      
      return userResponse.data;
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  const value = {
    user,
    login,
    register,
    logout,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};