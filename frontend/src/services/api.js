import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  register: (userData) => api.post('/api/auth/register', userData),
  login: (credentials) => api.post('/api/auth/token', credentials, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  }),
  getProfile: () => api.get('/api/auth/me'),
};

// Curriculum API
export const curriculumAPI = {
  create: (data) => api.post('/api/curriculum/', data),
  getAll: () => api.get('/api/curriculum/'),
  getLearningPaths: (id) => api.get(`/api/curriculum/${id}/learning-paths`),
  uploadContent: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/api/curriculum/upload', formData);
  },
};

// Assessment API
export const assessmentAPI = {
  get: (id) => api.get(`/api/assessment/${id}`),
  getQuestions: (id) => api.get(`/api/assessment/${id}/questions`),
  submit: (id, answers) => api.post(`/api/assessment/${id}/submit`, answers),
};

// Analytics API
export const analyticsAPI = {
  getDashboard: () => api.get('/api/analytics/dashboard'),
};

export default api;