import axios from 'axios';
import { authAPI, curriculumAPI, assessmentAPI } from '../services/api';

jest.mock('axios');
const mockedAxios = axios;

describe('API Services', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorage.clear();
  });

  describe('Auth API', () => {
    test('register calls correct endpoint', async () => {
      const mockResponse = { data: { access_token: 'token' } };
      mockedAxios.create.mockReturnValue({
        post: jest.fn().mockResolvedValue(mockResponse),
        interceptors: {
          request: { use: jest.fn() },
          response: { use: jest.fn() }
        }
      });

      const userData = {
        email: 'test@example.com',
        password: 'password123',
        full_name: 'Test User'
      };

      await authAPI.register(userData);
      
      expect(mockedAxios.create().post).toHaveBeenCalledWith('/api/auth/register', userData);
    });

    test('login calls correct endpoint with form data', async () => {
      const mockResponse = { data: { access_token: 'token' } };
      mockedAxios.create.mockReturnValue({
        post: jest.fn().mockResolvedValue(mockResponse),
        interceptors: {
          request: { use: jest.fn() },
          response: { use: jest.fn() }
        }
      });

      const credentials = { username: 'test@example.com', password: 'password123' };
      
      await authAPI.login(credentials);
      
      expect(mockedAxios.create().post).toHaveBeenCalledWith(
        '/api/auth/token', 
        credentials,
        { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
      );
    });
  });

  describe('Curriculum API', () => {
    test('create curriculum calls correct endpoint', async () => {
      const mockResponse = { data: { id: 1, title: 'Test Curriculum' } };
      mockedAxios.create.mockReturnValue({
        post: jest.fn().mockResolvedValue(mockResponse),
        interceptors: {
          request: { use: jest.fn() },
          response: { use: jest.fn() }
        }
      });

      const curriculumData = {
        title: 'Test Curriculum',
        subject: 'Math',
        grade_level: '10'
      };

      await curriculumAPI.create(curriculumData);
      
      expect(mockedAxios.create().post).toHaveBeenCalledWith('/api/curriculum/', curriculumData);
    });

    test('getAll curricula calls correct endpoint', async () => {
      const mockResponse = { data: [] };
      mockedAxios.create.mockReturnValue({
        get: jest.fn().mockResolvedValue(mockResponse),
        interceptors: {
          request: { use: jest.fn() },
          response: { use: jest.fn() }
        }
      });

      await curriculumAPI.getAll();
      
      expect(mockedAxios.create().get).toHaveBeenCalledWith('/api/curriculum/');
    });
  });

  describe('Assessment API', () => {
    test('generate assessment calls correct endpoint', async () => {
      const mockResponse = { data: { id: 1, title: 'Generated Assessment' } };
      mockedAxios.create.mockReturnValue({
        post: jest.fn().mockResolvedValue(mockResponse),
        interceptors: {
          request: { use: jest.fn() },
          response: { use: jest.fn() }
        }
      });

      await assessmentAPI.generate(1, 'quiz');
      
      expect(mockedAxios.create().post).toHaveBeenCalledWith(
        '/api/assessment/generate',
        { curriculum_id: 1, assessment_type: 'quiz' }
      );
    });

    test('submit assessment calls correct endpoint', async () => {
      const mockResponse = { data: { score: 85 } };
      mockedAxios.create.mockReturnValue({
        post: jest.fn().mockResolvedValue(mockResponse),
        interceptors: {
          request: { use: jest.fn() },
          response: { use: jest.fn() }
        }
      });

      const answers = { '1': 'A', '2': 'B' };
      
      await assessmentAPI.submit(1, answers);
      
      expect(mockedAxios.create().post).toHaveBeenCalledWith(
        '/api/assessment/1/submit',
        { answers }
      );
    });
  });
});