import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Register from '../pages/Register';
import { authAPI } from '../services/api';

jest.mock('../services/api');
jest.mock('../hooks/useAuth', () => ({
  useAuth: () => ({
    register: jest.fn(),
    loading: false
  })
}));

const renderWithRouter = (component) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  );
};

describe('Register Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders registration form', () => {
    renderWithRouter(<Register />);
    
    expect(screen.getByLabelText(/full name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/institution/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /create account/i })).toBeInTheDocument();
  });

  test('shows validation errors for empty fields', async () => {
    renderWithRouter(<Register />);
    
    const submitButton = screen.getByRole('button', { name: /create account/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/full name is required/i)).toBeInTheDocument();
      expect(screen.getByText(/email is required/i)).toBeInTheDocument();
      expect(screen.getByText(/password is required/i)).toBeInTheDocument();
    });
  });

  test('validates password length', async () => {
    renderWithRouter(<Register />);
    
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: '123' }
    });
    
    const submitButton = screen.getByRole('button', { name: /create account/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/password must be at least 6 characters/i)).toBeInTheDocument();
    });
  });

  test('submits form with valid data', async () => {
    const mockRegister = jest.fn().mockResolvedValue({
      data: { access_token: 'test-token', token_type: 'bearer' }
    });
    authAPI.register = mockRegister;

    renderWithRouter(<Register />);
    
    fireEvent.change(screen.getByLabelText(/full name/i), {
      target: { value: 'Test User' }
    });
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'test@example.com' }
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'password123' }
    });
    fireEvent.change(screen.getByLabelText(/institution/i), {
      target: { value: 'Test School' }
    });
    
    fireEvent.click(screen.getByRole('button', { name: /create account/i }));

    await waitFor(() => {
      expect(mockRegister).toHaveBeenCalledWith(
        expect.objectContaining({
          full_name: 'Test User',
          email: 'test@example.com',
          password: 'password123',
          institution: 'Test School'
        })
      );
    });
  });
});