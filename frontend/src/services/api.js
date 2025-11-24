import axios from 'axios';

const API_BASE_URL = 'http://edweavepack-alb-1353441079.eu-north-1.elb.amazonaws.com';

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

// Enhanced response interceptor with retry logic
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // Handle network errors with retry
    if (!error.response) {
      console.error('Network Error: Unable to connect to API server');
      
      // Retry logic for network errors
      if (!originalRequest._retry && originalRequest._retryCount < 3) {
        originalRequest._retry = true;
        originalRequest._retryCount = (originalRequest._retryCount || 0) + 1;
        
        // Wait before retry
        await new Promise(resolve => setTimeout(resolve, 1000 * originalRequest._retryCount));
        return api(originalRequest);
      }
      
      error.message = 'Unable to connect to server. Please check your connection and try again.';
    } else if (error.response?.status === 401) {
      // Clear tokens on authentication failure
      localStorage.removeItem('token');
      localStorage.removeItem('studentToken');
      
      // Redirect to login if not already there
      if (!window.location.pathname.includes('/login')) {
        window.location.href = '/login';
      }
    } else if (error.response?.status >= 500) {
      error.message = 'Server error. Please try again later.';
    }
    
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (userData) => {
    // Sending registration request
    
    // Validate required fields
    const requiredFields = ['email', 'password', 'full_name', 'role'];
    for (const field of requiredFields) {
      if (!userData[field]) {
        throw new Error(`${field.replace('_', ' ')} is required`);
      }
    }
    
    // Ensure role is valid
    const validRoles = ['teacher', 'student', 'administrator', 'curriculum_designer'];
    if (!validRoles.includes(userData.role)) {
      userData.role = 'teacher'; // Default fallback
    }
    
    return api.post('/api/auth/register', userData)
      .then(response => {
        // Registration successful
        return response;
      })
      .catch(error => {
        // Registration error occurred
        
        if (!error.response) {
          const networkError = new Error('Unable to connect to server. Please check your internet connection and try again.');
          networkError.isNetworkError = true;
          throw networkError;
        }
        
        // Handle specific error cases
        if (error.response.status === 400) {
          const detail = error.response.data?.detail || 'Registration failed due to invalid data';
          const validationError = new Error(detail);
          validationError.isValidationError = true;
          throw validationError;
        }
        
        if (error.response.status >= 500) {
          const serverError = new Error('Server error occurred. Please try again in a moment.');
          serverError.isServerError = true;
          throw serverError;
        }
        
        throw error;
      });
  },
  login: (credentials) => {
    return api.post('/api/auth/token', credentials, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
    .catch(error => {
      console.error('API: Login error:', error);
      
      if (!error.response) {
        const networkError = new Error('Unable to connect to server. Please check your internet connection.');
        networkError.isNetworkError = true;
        throw networkError;
      }
      
      if (error.response.status === 401) {
        const authError = new Error('Invalid email or password. Please check your credentials.');
        authError.isAuthError = true;
        throw authError;
      }
      
      if (error.response.status >= 500) {
        const serverError = new Error('Server error occurred. Please try again.');
        serverError.isServerError = true;
        throw serverError;
      }
      
      throw error;
    });
  },
  getProfile: () => {
    return api.get('/api/auth/me')
      .catch(error => {
        console.error('API: Profile fetch error:', error);
        
        if (!error.response) {
          const networkError = new Error('Unable to fetch profile. Please check your connection.');
          networkError.isNetworkError = true;
          throw networkError;
        }
        
        if (error.response.status === 401) {
          // Token expired or invalid
          localStorage.removeItem('token');
          localStorage.removeItem('studentToken');
          const authError = new Error('Session expired. Please log in again.');
          authError.isAuthError = true;
          throw authError;
        }
        
        throw error;
      });
  },
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
    return api.post('/api/files/simple-upload', formData);
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
  uploadContent: (file) => {
    // Mock upload - return simulated response
    return Promise.resolve({
      data: {
        filename: file.name,
        content: `Sample content from ${file.name}`,
        full_content: `Detailed curriculum content extracted from ${file.name}. This includes learning objectives, key concepts, and assessment criteria.`,
        status: 'completed'
      }
    });
  },
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