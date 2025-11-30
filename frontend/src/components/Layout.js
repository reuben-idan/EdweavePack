import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { useTheme } from '../contexts/ThemeContext';
import { toast } from 'react-toastify';
import { BookOpen, LogOut, BarChart3, FileText, Upload, Home, User, Users, Moon, Sun } from 'lucide-react';

const Layout = ({ children }) => {
  const { user, logout } = useAuth();
  const { isDark, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    toast.success('Logged out successfully', { position: 'top-right' });
    navigate('/login');
  };

  const isActive = (path) => location.pathname === path;

  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: Home },
    { path: '/curriculum', label: 'Curriculum', icon: BookOpen },
    { path: '/students', label: 'Students', icon: Users },
    { path: '/assessments', label: 'Assessments', icon: FileText },
    { path: '/upload', label: 'Upload', icon: Upload },
  ];

  return (
    <div className="min-h-screen animated-gradient bg-edu-gradient">
      {/* Navigation */}
      <nav className="glass-nav sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              {/* Logo */}
              <Link to="/dashboard" className="flex items-center space-x-3 hover-lift">
                <img 
                  src="/images/Edweave Pack Logo.png" 
                  alt="EdweavePack" 
                  className="h-10 w-10 rounded-xl"
                />
                <span className="text-xl font-bold text-gradient">EdweavePack</span>
              </Link>
              
              {/* Navigation Items */}
              <div className="ml-10 flex space-x-2">
                {navItems.map(({ path, label, icon: Icon }) => (
                  <Link
                    key={path}
                    to={path}
                    className={`flex items-center space-x-2 px-4 py-2 rounded-xl text-sm font-medium transition-all duration-300 ${
                      isActive(path)
                        ? 'bg-edu-primary/20 text-visible shadow-lg'
                        : 'text-visible hover:bg-edu-primary/10'
                    }`}
                  >
                    <Icon className="h-4 w-4" />
                    <span>{label}</span>
                  </Link>
                ))}
              </div>
            </div>
            
            {/* User Menu */}
            <div className="flex items-center space-x-4">
              <button
                onClick={toggleTheme}
                className="glass-button p-2 text-visible hover:bg-edu-primary/10"
                title={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
              >
                {isDark ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
              </button>
              
              <div className="flex items-center space-x-3 glass-card px-4 py-2">
                <User className="h-5 w-5 text-visible" />
                <div className="flex flex-col">
                  <span className="text-sm text-visible font-medium">
                    {user?.name || user?.full_name || 'User'}
                  </span>
                  {user?.institution && (
                    <span className="text-xs text-visible opacity-75">
                      {user.institution}
                    </span>
                  )}
                </div>
              </div>
              
              <button
                onClick={handleLogout}
                className="flex items-center space-x-2 glass-button text-visible hover:bg-red-500/20"
              >
                <LogOut className="h-4 w-4" />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </nav>
      
      {/* Main Content */}
      <main className="min-h-screen">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          {children}
        </div>
      </main>
    </div>
  );
};

export default Layout;