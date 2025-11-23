import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { toast } from 'react-toastify';
import { BookOpen, LogOut, BarChart3, FileText, Upload, Home, User, Users } from 'lucide-react';

const Layout = ({ children }) => {
  const { user, logout } = useAuth();
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
    <div className="min-h-screen animated-gradient">
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
                        ? 'bg-white/20 text-white shadow-lg'
                        : 'text-white/80 hover:text-white hover:bg-white/10'
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
              <div className="flex items-center space-x-3 glass-card px-4 py-2">
                <User className="h-5 w-5 text-white/80" />
                <span className="text-sm text-white font-medium">
                  {user?.name || user?.email || 'User'}
                </span>
              </div>
              
              <button
                onClick={handleLogout}
                className="flex items-center space-x-2 glass-button text-white/80 hover:text-white hover:bg-red-500/20"
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