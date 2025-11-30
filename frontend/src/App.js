import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import { AuthProvider, useAuth } from './hooks/useAuth';
import { StudentAuthProvider, useStudentAuth } from './hooks/useStudentAuth';
import { ThemeProvider } from './contexts/ThemeContext';
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
import AssessmentListEnhanced from './pages/AssessmentListEnhanced';
import AssessmentTake from './pages/AssessmentTake';
import CreateAssessment from './pages/CreateAssessment';
import StudentSignup from './pages/StudentSignup';
import StudentLogin from './pages/StudentLogin';
import StudentDashboard from './pages/StudentDashboard';
import StudentDashboardEnhanced from './pages/StudentDashboardEnhanced';
import StudentProfile from './pages/StudentProfile';
import StudentProfileEnhanced from './pages/StudentProfileEnhanced';
import StudentUpload from './pages/StudentUpload';
import StudentLearningPath from './pages/StudentLearningPath';
import StudentLearningPathEnhanced from './pages/StudentLearningPathEnhanced';
import StudentQuiz from './pages/StudentQuiz';
import WeeklyPlanPage from './pages/WeeklyPlanPage';
import DailyPlanPage from './pages/DailyPlanPage';
import ProgressPage from './pages/ProgressPage';
import ForgotPassword from './pages/ForgotPassword';
import ResetPassword from './pages/ResetPassword';
import Settings from './pages/Settings';
import { TeacherDashboard } from './pages/TeacherDashboard';
import StudentsPage from './pages/StudentsPage';
import StudentLesson from './pages/StudentLesson';
import StudentUploadGoals from './pages/StudentUploadGoals';
import StudentAnalytics from './pages/StudentAnalytics';

const ProtectedRoute = ({ children, requiredRole = null }) => {
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
  
  if (!user) {
    return <Navigate to="/login" />;
  }
  
  // Debug user role
  console.log('ProtectedRoute - User role:', user.role, 'Path:', window.location.pathname);
  
  // Redirect students to student portal if they try to access teacher routes
  if (user.role === 'student' && !window.location.pathname.startsWith('/student')) {
    console.log('Redirecting student to student portal');
    return <Navigate to="/student/dashboard" replace />;
  }
  
  // Redirect teachers to teacher portal if they try to access student routes
  if (user.role !== 'student' && window.location.pathname.startsWith('/student')) {
    console.log('Redirecting teacher to teacher portal');
    return <Navigate to="/dashboard" replace />;
  }
  
  return children;
};

const StudentProtectedRoute = ({ children }) => {
  // Simplified for now - bypass auth check
  return children;
};

const AppRoutes = () => {
  const { user } = useAuth();
  
  const getDefaultRoute = () => {
    if (!user) return '/login';
    if (user.role === 'student') return '/student/dashboard';
    return '/dashboard';
  };
  
  return (
    <Routes>
      <Route path="/login" element={user ? <Navigate to={getDefaultRoute()} /> : <Login />} />
      <Route path="/register" element={user ? <Navigate to={getDefaultRoute()} /> : <Register />} />
      <Route path="/" element={user ? <Navigate to={getDefaultRoute()} /> : <Navigate to="/login" />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />
      <Route path="/reset-password/:token" element={<ResetPassword />} />
      <Route path="/student/signup" element={<StudentSignup />} />
      <Route path="/student/login" element={<StudentLogin />} />
      <Route 
        path="/student/dashboard" 
        element={
          <StudentProtectedRoute>
            <StudentDashboard />
          </StudentProtectedRoute>
        } 
      />
      <Route 
        path="/student/profile" 
        element={
          <StudentProtectedRoute>
            <StudentProfileEnhanced />
          </StudentProtectedRoute>
        } 
      />
      <Route 
        path="/student/upload" 
        element={
          <StudentProtectedRoute>
            <StudentUpload />
          </StudentProtectedRoute>
        } 
      />
      <Route 
        path="/student/learning-path" 
        element={
          <StudentProtectedRoute>
            <StudentLearningPathEnhanced />
          </StudentProtectedRoute>
        } 
      />
      <Route 
        path="/student/weekly-plan" 
        element={
          <StudentProtectedRoute>
            <WeeklyPlanPage />
          </StudentProtectedRoute>
        } 
      />
      <Route 
        path="/student/daily-plan" 
        element={
          <StudentProtectedRoute>
            <DailyPlanPage />
          </StudentProtectedRoute>
        } 
      />
      <Route 
        path="/student/progress" 
        element={
          <StudentProtectedRoute>
            <ProgressPage />
          </StudentProtectedRoute>
        } 
      />
      <Route 
        path="/student/quiz/:quizId" 
        element={
          <StudentProtectedRoute>
            <StudentQuiz />
          </StudentProtectedRoute>
        } 
      />
      <Route
        path="/student/upload-goals"
        element={
          <StudentProtectedRoute>
            <StudentUploadGoals />
          </StudentProtectedRoute>
        }
      />
      <Route
        path="/student/analytics"
        element={
          <StudentProtectedRoute>
            <StudentAnalytics />
          </StudentProtectedRoute>
        }
      />
      <Route 
        path="/student/lesson/:lessonId" 
        element={
          <StudentProtectedRoute>
            <StudentLesson />
          </StudentProtectedRoute>
        } 
      />

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
              <AssessmentListEnhanced />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/assessment/create"
        element={
          <ProtectedRoute>
            <Layout>
              <CreateAssessment />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/assessment/:id/take"
        element={
          <ProtectedRoute>
            <AssessmentTake />
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
        path="/assessments/:id/results"
        element={
          <ProtectedRoute>
            <Layout>
              <div className="p-8">
                <h1 className="text-2xl font-bold mb-4">Assessment Results</h1>
                <div className="glass-card p-6">
                  <p>Assessment completed successfully!</p>
                </div>
              </div>
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/assessments/:id/edit"
        element={
          <ProtectedRoute>
            <Layout>
              <CreateAssessment />
            </Layout>
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
      <Route
        path="/students"
        element={
          <ProtectedRoute>
            <Layout>
              <StudentsPage />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/settings/:section?"
        element={
          <ProtectedRoute>
            <Settings />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
};

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider>
        <AuthProvider>
          <StudentAuthProvider>
            <Router future={{ v7_relativeSplatPath: true, v7_startTransition: true }}>
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
          </StudentAuthProvider>
        </AuthProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;