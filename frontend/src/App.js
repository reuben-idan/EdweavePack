import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import { AuthProvider, useAuth } from './hooks/useAuth';
import Layout from './components/Layout';
import ErrorBoundary from './components/ErrorBoundary';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import UploadPage from './pages/UploadPage';
import CurriculumPage from './pages/CurriculumPage';
import CurriculumList from './pages/CurriculumList';
import CreateCurriculum from './pages/CreateCurriculum';
import AssessmentList from './pages/AssessmentList';
import AssessmentTake from './pages/AssessmentTake';
import CreateAssessment from './pages/CreateAssessment';
import StudentSignup from './pages/StudentSignup';
import StudentLogin from './pages/StudentLogin';
import StudentDashboard from './pages/StudentDashboard';
import StudentProfile from './pages/StudentProfile';
import StudentUpload from './pages/StudentUpload';
import { TeacherDashboard } from './pages/TeacherDashboard';

const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();
  
  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen animated-gradient">
        <div className="glass-card p-8 text-center">
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-white font-medium">Loading EdweavePack...</p>
        </div>
      </div>
    );
  }
  
  return user ? children : <Navigate to="/login" />;
};

const AppRoutes = () => {
  const { user } = useAuth();
  
  return (
    <Routes>
      <Route path="/login" element={user ? <Navigate to="/dashboard" /> : <Login />} />
      <Route path="/register" element={user ? <Navigate to="/dashboard" /> : <Register />} />
      <Route path="/student/signup" element={<StudentSignup />} />
      <Route path="/student/login" element={<StudentLogin />} />
      <Route path="/student/dashboard" element={<StudentDashboard />} />
      <Route path="/student/profile" element={<StudentProfile />} />
      <Route path="/student/upload" element={<StudentUpload />} />
      <Route path="/" element={<Navigate to="/dashboard" />} />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Layout>
              <Dashboard />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/upload"
        element={
          <ProtectedRoute>
            <Layout>
              <UploadPage />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/curriculum"
        element={
          <ProtectedRoute>
            <Layout>
              <CurriculumList />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/curriculum/:id"
        element={
          <ProtectedRoute>
            <Layout>
              <CurriculumPage />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/curriculum/create"
        element={
          <ProtectedRoute>
            <Layout>
              <CreateCurriculum />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/assessments"
        element={
          <ProtectedRoute>
            <Layout>
              <AssessmentList />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/assessments/create"
        element={
          <ProtectedRoute>
            <Layout>
              <CreateAssessment />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/assessment/:id"
        element={
          <ProtectedRoute>
            <AssessmentTake />
          </ProtectedRoute>
        }
      />
      <Route
        path="/teacher"
        element={
          <ProtectedRoute>
            <Layout>
              <TeacherDashboard />
            </Layout>
          </ProtectedRoute>
        }
      />
    </Routes>
  );
};

function App() {
  return (
    <ErrorBoundary>
      <AuthProvider>
        <Router>
          <div className="App">
            <AppRoutes />
            <ToastContainer
              position="top-right"
              autoClose={4000}
              hideProgressBar={false}
              newestOnTop={false}
              closeOnClick
              rtl={false}
              pauseOnFocusLoss
              draggable
              pauseOnHover
              theme="light"
              toastClassName="glass-card"
            />
          </div>
        </Router>
      </AuthProvider>
    </ErrorBoundary>
  );
}

export default App;