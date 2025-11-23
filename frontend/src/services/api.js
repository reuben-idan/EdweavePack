import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  // Check for both teacher and student tokens
  const token = localStorage.getItem('token') || localStorage.getItem('studentToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('studentToken');
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (userData) => {
    console.log('API: Sending registration request:', userData);
    return api.post('/api/auth/register', userData)
      .then(response => {
        console.log('API: Registration response:', response);
        return response;
      })
      .catch(error => {
        console.error('API: Registration error:', error);
        console.error('API: Error response:', error.response);
        throw error;
      });
  },
  login: (credentials) => api.post('/api/auth/token', credentials, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  }),
  getProfile: () => api.get('/api/auth/me'),
  forgotPassword: (data) => api.post('/api/auth/forgot-password', data),
  resetPassword: (data) => api.post('/api/auth/reset-password', data),
  updateProfile: (data) => api.put('/api/auth/profile', data),
  updatePassword: (data) => api.put('/api/auth/password', data)
};

// Files API
export const filesAPI = {
  upload: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/api/files/upload', formData);
  },
  uploadUrl: (url) => {
    const formData = new FormData();
    formData.append('url', url);
    return api.post('/api/files/upload-url', formData);
  },
  getAll: () => api.get('/api/files/'),
  getById: (id) => api.get(`/api/files/${id}`),
  delete: (id) => api.delete(`/api/files/${id}`),
};

// Tasks API
export const tasksAPI = {
  getStatus: (taskId) => api.get(`/api/tasks/status/${taskId}`),
  getActive: () => api.get('/api/tasks/active'),
  cancel: (taskId) => api.post(`/api/tasks/cancel/${taskId}`),
};

// Curriculum API
export const curriculumAPI = {
  create: (data) => api.post('/api/curriculum/', data),
  getAll: () => api.get('/api/curriculum/'),
  getById: (id) => api.get(`/api/curriculum/${id}`),
  getLearningPaths: (id) => api.get(`/api/curriculum/${id}/learning-paths`),
  adaptLevel: (id, level) => api.post(`/api/curriculum/enhanced/${id}/adapt-level`, { target_level: level }),
  exportPDF: (id) => api.get(`/api/curriculum/enhanced/${id}/export/pdf`, { responseType: 'blob' }),
  exportDOCX: (id) => api.get(`/api/curriculum/enhanced/${id}/export/docx`, { responseType: 'blob' }),
  share: (id) => api.post(`/api/curriculum/enhanced/${id}/share`),
};

// Assessment API
export const assessmentAPI = {
  get: (id) => api.get(`/api/assessment/${id}`),
  getQuestions: (id) => api.get(`/api/assessment/${id}/questions`),
  submit: (id, answers) => api.post(`/api/assessment/${id}/submit`, { answers }),
  generate: (curriculumId, type) => api.post('/api/assessment/generate', { curriculum_id: curriculumId, assessment_type: type }),
};

// Analytics API
export const analyticsAPI = {
  getDashboard: () => api.get('/api/analytics/dashboard'),
  getClassPerformance: (curriculumId) => api.get('/api/analytics/class-performance', { params: { curriculum_id: curriculumId } }),
  getMisconceptions: () => api.get('/api/analytics/misconceptions'),
  getStudentProgress: (studentId) => api.get(`/api/analytics/progress-tracking/${studentId}`),
};

// Students API
export const studentsAPI = {
  create: (data) => api.post('/api/learning-paths/students', data),
  getAll: () => api.get('/api/learning-paths/students'),
  getById: (id) => api.get(`/api/learning-paths/students/${id}`),
  update: (id, data) => api.put(`/api/learning-paths/students/${id}`, data),
  delete: (id) => api.delete(`/api/learning-paths/students/${id}`),
  getAnalytics: (id) => api.get(`/api/learning-paths/analytics/${id}`),
  generatePath: (studentId, curriculumId) => api.post(`/api/learning-paths/personalized/${studentId}/${curriculumId}`),
  getPath: (studentId, curriculumId) => api.get(`/api/learning-paths/personalized/${studentId}/${curriculumId}`),
  getProgress: (id) => api.get(`/api/analytics/progress-tracking/${id}`),
  bulkImport: (data) => api.post('/api/learning-paths/students/bulk-import', data),
  export: (format = 'csv') => api.get(`/api/learning-paths/students/export?format=${format}`, { responseType: 'blob' }),
};

export default api;