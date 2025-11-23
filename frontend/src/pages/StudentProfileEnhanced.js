import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { 
  ArrowLeft, Save, User, Mail, Calendar, Target, BookOpen, Settings,
  Eye, EyeOff, Lock, Bell, Shield, Palette, Globe, Download, Upload,
  Camera, Edit3, Check, X, AlertCircle, CheckCircle, Star, Trophy,
  BarChart3, Clock, Brain, Heart, Zap, Award, Phone, MapPin
} from 'lucide-react';
import { useStudentAuth } from '../hooks/useStudentAuth';

const StudentProfileEnhanced = () => {
  const navigate = useNavigate();
  const { student, updateProfile, changePassword } = useStudentAuth();
  const [activeTab, setActiveTab] = useState('profile');
  const [loading, setLoading] = useState(false);
  const [showPasswordForm, setShowPasswordForm] = useState(false);
  
  // Profile form data
  const [profileData, setProfileData] = useState({
    name: '',
    email: '',
    phone: '',
    dateOfBirth: '',
    address: '',
    bio: '',
    learningStyle: 'visual',
    targetExams: [],
    academicGoals: '',
    subjects: [],
    studyHours: 2,
    preferredStudyTime: 'morning'
  });

  // Password form data
  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });

  // Settings data
  const [settings, setSettings] = useState({
    notifications: {
      email: true,
      push: true,
      studyReminders: true,
      quizReminders: true,
      achievements: true,
      weeklyReports: true
    },
    privacy: {
      profileVisibility: 'private',
      showProgress: false,
      showAchievements: true
    },
    preferences: {
      theme: 'auto',
      language: 'en',
      timezone: 'UTC',
      dateFormat: 'MM/DD/YYYY'
    }
  });

  const [showPassword, setShowPassword] = useState({
    current: false,
    new: false,
    confirm: false
  });

  const learningStyles = [
    { id: 'visual', label: 'Visual Learner', icon: '👁️', desc: 'Learn through images, diagrams, and charts' },
    { id: 'auditory', label: 'Auditory Learner', icon: '👂', desc: 'Learn through listening and discussion' },
    { id: 'reading', label: 'Reading/Writing', icon: '📚', desc: 'Learn through text and written materials' },
    { id: 'kinesthetic', label: 'Kinesthetic Learner', icon: '🤲', desc: 'Learn through hands-on activities' }
  ];

  const examOptions = [
    'BECE', 'WASSCE', 'SAT', 'ACT', 'IGCSE', 'A-Levels', 'IB', 'JAMB', 'NECO', 'University Entrance'
  ];

  const subjectOptions = [
    'Mathematics', 'Physics', 'Chemistry', 'Biology', 'English', 'Literature',
    'History', 'Geography', 'Economics', 'Computer Science', 'Art', 'Music'
  ];

  useEffect(() => {
    if (student) {
      loadProfileData();
    }
  }, [student]);

  const loadProfileData = () => {
    // Load existing profile data
    setProfileData({
      name: student.name || '',
      email: student.email || '',
      phone: student.phone || '',
      dateOfBirth: student.dateOfBirth || '',
      address: student.address || '',
      bio: student.bio || '',
      learningStyle: student.learningStyle || 'visual',
      targetExams: student.targetExams || [],
      academicGoals: student.academicGoals || '',
      subjects: student.subjects || [],
      studyHours: student.studyHours || 2,
      preferredStudyTime: student.preferredStudyTime || 'morning'
    });
  };

  const handleProfileChange = (field, value) => {
    setProfileData(prev => ({ ...prev, [field]: value }));
  };

  const handleArrayToggle = (field, value) => {
    setProfileData(prev => ({
      ...prev,
      [field]: prev[field].includes(value)
        ? prev[field].filter(item => item !== value)
        : [...prev[field], value]
    }));
  };

  const handleSettingsChange = (category, field, value) => {
    setSettings(prev => ({
      ...prev,
      [category]: {
        ...prev[category],
        [field]: value
      }
    }));
  };

  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const result = await updateProfile(profileData);
      if (result.success) {
        toast.success('Profile updated successfully!');
      }
    } catch (error) {
      toast.error('Failed to update profile');
    } finally {
      setLoading(false);
    }
  };

  const handlePasswordSubmit = async (e) => {
    e.preventDefault();
    
    if (passwordData.newPassword !== passwordData.confirmPassword) {
      toast.error('New passwords do not match');
      return;
    }
    
    if (passwordData.newPassword.length < 6) {
      toast.error('Password must be at least 6 characters');
      return;
    }
    
    setLoading(true);
    
    try {
      const result = await changePassword({
        currentPassword: passwordData.currentPassword,
        newPassword: passwordData.newPassword
      });
      
      if (result.success) {
        setPasswordData({ currentPassword: '', newPassword: '', confirmPassword: '' });
        setShowPasswordForm(false);
        toast.success('Password updated successfully!');
      }
    } catch (error) {
      toast.error('Failed to update password');
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: 'profile', label: 'Profile', icon: User },
    { id: 'academic', label: 'Academic', icon: BookOpen },
    { id: 'security', label: 'Security', icon: Shield },
    { id: 'notifications', label: 'Notifications', icon: Bell },
    { id: 'preferences', label: 'Preferences', icon: Settings }
  ];

  return (
    <div className="min-h-screen animated-gradient">
      {/* Header */}
      <div className="glass-nav sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/student/dashboard')}
                className="glass-button p-3 hover-lift"
              >
                <ArrowLeft className="h-5 w-5 text-white" />
              </button>
              <div>
                <h1 className="text-xl font-bold text-white">Profile & Settings</h1>
                <p className="text-white/80 text-sm">Manage your account and preferences</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <button
                onClick={handleProfileSubmit}
                disabled={loading}
                className="premium-button disabled:opacity-50"
              >
                {loading ? (
                  <div className="spinner w-4 h-4 mr-2" />
                ) : (
                  <Save className="h-4 w-4 mr-2" />
                )}
                Save Changes
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar Navigation */}
          <div className="lg:col-span-1">
            <div className="glass-card p-6 sticky top-24">
              {/* Profile Summary */}
              <div className="text-center mb-6">
                <div className="relative inline-block">
                  <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-2xl mb-3">
                    {student?.name?.charAt(0)?.toUpperCase() || 'S'}
                  </div>
                  <button className="absolute bottom-0 right-0 bg-blue-500 text-white p-1 rounded-full hover:bg-blue-600 transition-colors">
                    <Camera className="h-3 w-3" />
                  </button>
                </div>
                <h3 className="font-semibold text-white">{student?.name}</h3>
                <p className="text-blue-200 text-sm">{student?.email}</p>
              </div>

              {/* Navigation Tabs */}
              <nav className="space-y-2">
                {tabs.map((tab) => {
                  const TabIcon = tab.icon;
                  return (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-all ${
                        activeTab === tab.id
                          ? 'bg-blue-500/20 text-blue-400 border border-blue-400'
                          : 'text-white/80 hover:bg-white/10 hover:text-white'
                      }`}
                    >
                      <TabIcon className="h-5 w-5" />
                      <span className="font-medium">{tab.label}</span>
                    </button>
                  );
                })}
              </nav>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            <form onSubmit={handleProfileSubmit} className="space-y-8">
              {/* Profile Tab */}
              {activeTab === 'profile' && (
                <div className="space-y-6">
                  <div className="glass-card p-6">
                    <h2 className="text-xl font-semibold text-white mb-6 flex items-center">
                      <User className="h-6 w-6 mr-2 text-blue-400" />
                      Personal Information
                    </h2>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <label className="block text-sm font-medium text-blue-200 mb-2">Full Name</label>
                        <input
                          type="text"
                          value={profileData.name}
                          onChange={(e) => handleProfileChange('name', e.target.value)}
                          className="glass-input w-full"
                          placeholder="Enter your full name"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-blue-200 mb-2">Email Address</label>
                        <input
                          type="email"
                          value={profileData.email}
                          onChange={(e) => handleProfileChange('email', e.target.value)}
                          className="glass-input w-full"
                          placeholder="Enter your email"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-blue-200 mb-2">Phone Number</label>
                        <input
                          type="tel"
                          value={profileData.phone}
                          onChange={(e) => handleProfileChange('phone', e.target.value)}
                          className="glass-input w-full"
                          placeholder="Enter your phone number"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-blue-200 mb-2">Date of Birth</label>
                        <input
                          type="date"
                          value={profileData.dateOfBirth}
                          onChange={(e) => handleProfileChange('dateOfBirth', e.target.value)}
                          className="glass-input w-full"
                        />
                      </div>
                    </div>

                    <div className="mt-6">
                      <label className="block text-sm font-medium text-blue-200 mb-2">Address</label>
                      <input
                        type="text"
                        value={profileData.address}
                        onChange={(e) => handleProfileChange('address', e.target.value)}
                        className="glass-input w-full"
                        placeholder="Enter your address"
                      />
                    </div>

                    <div className="mt-6">
                      <label className="block text-sm font-medium text-blue-200 mb-2">Bio</label>
                      <textarea
                        value={profileData.bio}
                        onChange={(e) => handleProfileChange('bio', e.target.value)}
                        className="glass-input w-full h-24 resize-none"
                        placeholder="Tell us about yourself..."
                      />
                    </div>
                  </div>
                </div>
              )}

              {/* Academic Tab */}
              {activeTab === 'academic' && (
                <div className="space-y-6">
                  <div className="glass-card p-6">
                    <h2 className="text-xl font-semibold text-white mb-6 flex items-center">
                      <BookOpen className="h-6 w-6 mr-2 text-green-400" />
                      Academic Profile
                    </h2>
                    
                    {/* Learning Style */}
                    <div className="mb-6">
                      <label className="block text-sm font-medium text-blue-200 mb-4">Learning Style</label>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {learningStyles.map(style => (
                          <label key={style.id} className={`glass-card p-4 cursor-pointer hover-lift transition-all ${
                            profileData.learningStyle === style.id ? 'ring-2 ring-blue-400 bg-blue-500/10' : ''
                          }`}>
                            <input
                              type="radio"
                              name="learningStyle"
                              value={style.id}
                              checked={profileData.learningStyle === style.id}
                              onChange={(e) => handleProfileChange('learningStyle', e.target.value)}
                              className="sr-only"
                            />
                            <div className="flex items-start space-x-3">
                              <span className="text-2xl">{style.icon}</span>
                              <div>
                                <div className="font-medium text-white">{style.label}</div>
                                <div className="text-sm text-blue-200">{style.desc}</div>
                              </div>
                            </div>
                          </label>
                        ))}
                      </div>
                    </div>

                    {/* Target Exams */}
                    <div className="mb-6">
                      <label className="block text-sm font-medium text-blue-200 mb-4">Target Exams</label>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                        {examOptions.map(exam => (
                          <button
                            key={exam}
                            type="button"
                            onClick={() => handleArrayToggle('targetExams', exam)}
                            className={`glass-card p-3 text-sm font-medium transition-all ${
                              profileData.targetExams.includes(exam)
                                ? 'bg-blue-500/20 text-blue-400 ring-1 ring-blue-400'
                                : 'text-white hover:bg-white/10'
                            }`}
                          >
                            {exam}
                          </button>
                        ))}
                      </div>
                    </div>

                    {/* Subjects */}
                    <div className="mb-6">
                      <label className="block text-sm font-medium text-blue-200 mb-4">Subjects of Interest</label>
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                        {subjectOptions.map(subject => (
                          <button
                            key={subject}
                            type="button"
                            onClick={() => handleArrayToggle('subjects', subject)}
                            className={`glass-card p-3 text-sm font-medium transition-all ${
                              profileData.subjects.includes(subject)
                                ? 'bg-green-500/20 text-green-400 ring-1 ring-green-400'
                                : 'text-white hover:bg-white/10'
                            }`}
                          >
                            {subject}
                          </button>
                        ))}
                      </div>
                    </div>

                    {/* Study Preferences */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <label className="block text-sm font-medium text-blue-200 mb-2">Daily Study Hours</label>
                        <select
                          value={profileData.studyHours}
                          onChange={(e) => handleProfileChange('studyHours', parseInt(e.target.value))}
                          className="glass-input w-full"
                        >
                          <option value={1}>1 hour</option>
                          <option value={2}>2 hours</option>
                          <option value={3}>3 hours</option>
                          <option value={4}>4 hours</option>
                          <option value={5}>5+ hours</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-blue-200 mb-2">Preferred Study Time</label>
                        <select
                          value={profileData.preferredStudyTime}
                          onChange={(e) => handleProfileChange('preferredStudyTime', e.target.value)}
                          className="glass-input w-full"
                        >
                          <option value="morning">Morning (6AM - 12PM)</option>
                          <option value="afternoon">Afternoon (12PM - 6PM)</option>
                          <option value="evening">Evening (6PM - 10PM)</option>
                          <option value="night">Night (10PM - 2AM)</option>
                        </select>
                      </div>
                    </div>

                    {/* Academic Goals */}
                    <div className="mt-6">
                      <label className="block text-sm font-medium text-blue-200 mb-2">Academic Goals</label>
                      <textarea
                        value={profileData.academicGoals}
                        onChange={(e) => handleProfileChange('academicGoals', e.target.value)}
                        className="glass-input w-full h-24 resize-none"
                        placeholder="Describe your academic goals and what you want to achieve..."
                      />
                    </div>
                  </div>
                </div>
              )}

              {/* Security Tab */}
              {activeTab === 'security' && (
                <div className="space-y-6">
                  <div className="glass-card p-6">
                    <h2 className="text-xl font-semibold text-white mb-6 flex items-center">
                      <Shield className="h-6 w-6 mr-2 text-red-400" />
                      Security Settings
                    </h2>
                    
                    {/* Password Section */}
                    <div className="mb-6">
                      <div className="flex items-center justify-between mb-4">
                        <div>
                          <h3 className="font-medium text-white">Password</h3>
                          <p className="text-sm text-blue-200">Keep your account secure with a strong password</p>
                        </div>
                        <button
                          type="button"
                          onClick={() => setShowPasswordForm(!showPasswordForm)}
                          className="glass-button bg-blue-500/20 text-blue-400"
                        >
                          {showPasswordForm ? 'Cancel' : 'Change Password'}
                        </button>
                      </div>

                      {showPasswordForm && (
                        <div className="glass-card p-4 space-y-4">
                          <div>
                            <label className="block text-sm font-medium text-blue-200 mb-2">Current Password</label>
                            <div className="relative">
                              <input
                                type={showPassword.current ? 'text' : 'password'}
                                value={passwordData.currentPassword}
                                onChange={(e) => setPasswordData(prev => ({ ...prev, currentPassword: e.target.value }))}
                                className="glass-input w-full pr-10"
                                placeholder="Enter current password"
                              />
                              <button
                                type="button"
                                onClick={() => setShowPassword(prev => ({ ...prev, current: !prev.current }))}
                                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-blue-300"
                              >
                                {showPassword.current ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                              </button>
                            </div>
                          </div>

                          <div>
                            <label className="block text-sm font-medium text-blue-200 mb-2">New Password</label>
                            <div className="relative">
                              <input
                                type={showPassword.new ? 'text' : 'password'}
                                value={passwordData.newPassword}
                                onChange={(e) => setPasswordData(prev => ({ ...prev, newPassword: e.target.value }))}
                                className="glass-input w-full pr-10"
                                placeholder="Enter new password"
                              />
                              <button
                                type="button"
                                onClick={() => setShowPassword(prev => ({ ...prev, new: !prev.new }))}
                                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-blue-300"
                              >
                                {showPassword.new ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                              </button>
                            </div>
                          </div>

                          <div>
                            <label className="block text-sm font-medium text-blue-200 mb-2">Confirm New Password</label>
                            <div className="relative">
                              <input
                                type={showPassword.confirm ? 'text' : 'password'}
                                value={passwordData.confirmPassword}
                                onChange={(e) => setPasswordData(prev => ({ ...prev, confirmPassword: e.target.value }))}
                                className="glass-input w-full pr-10"
                                placeholder="Confirm new password"
                              />
                              <button
                                type="button"
                                onClick={() => setShowPassword(prev => ({ ...prev, confirm: !prev.confirm }))}
                                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-blue-300"
                              >
                                {showPassword.confirm ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                              </button>
                            </div>
                          </div>

                          <button
                            type="button"
                            onClick={handlePasswordSubmit}
                            disabled={loading}
                            className="premium-button w-full disabled:opacity-50"
                          >
                            {loading ? 'Updating...' : 'Update Password'}
                          </button>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* Notifications Tab */}
              {activeTab === 'notifications' && (
                <div className="space-y-6">
                  <div className="glass-card p-6">
                    <h2 className="text-xl font-semibold text-white mb-6 flex items-center">
                      <Bell className="h-6 w-6 mr-2 text-yellow-400" />
                      Notification Preferences
                    </h2>
                    
                    <div className="space-y-6">
                      {Object.entries(settings.notifications).map(([key, value]) => (
                        <div key={key} className="flex items-center justify-between">
                          <div>
                            <div className="font-medium text-white capitalize">
                              {key.replace(/([A-Z])/g, ' $1').trim()}
                            </div>
                            <div className="text-sm text-blue-200">
                              {key === 'email' && 'Receive notifications via email'}
                              {key === 'push' && 'Receive push notifications in browser'}
                              {key === 'studyReminders' && 'Get reminded about study sessions'}
                              {key === 'quizReminders' && 'Get notified about upcoming quizzes'}
                              {key === 'achievements' && 'Celebrate your achievements'}
                              {key === 'weeklyReports' && 'Receive weekly progress reports'}
                            </div>
                          </div>
                          <button
                            type="button"
                            onClick={() => handleSettingsChange('notifications', key, !value)}
                            className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                              value ? 'bg-blue-500' : 'bg-gray-600'
                            }`}
                          >
                            <span
                              className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                                value ? 'translate-x-6' : 'translate-x-1'
                              }`}
                            />
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* Preferences Tab */}
              {activeTab === 'preferences' && (
                <div className="space-y-6">
                  <div className="glass-card p-6">
                    <h2 className="text-xl font-semibold text-white mb-6 flex items-center">
                      <Settings className="h-6 w-6 mr-2 text-purple-400" />
                      App Preferences
                    </h2>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <label className="block text-sm font-medium text-blue-200 mb-2">Theme</label>
                        <select
                          value={settings.preferences.theme}
                          onChange={(e) => handleSettingsChange('preferences', 'theme', e.target.value)}
                          className="glass-input w-full"
                        >
                          <option value="auto">Auto (System)</option>
                          <option value="light">Light</option>
                          <option value="dark">Dark</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-blue-200 mb-2">Language</label>
                        <select
                          value={settings.preferences.language}
                          onChange={(e) => handleSettingsChange('preferences', 'language', e.target.value)}
                          className="glass-input w-full"
                        >
                          <option value="en">English</option>
                          <option value="es">Spanish</option>
                          <option value="fr">French</option>
                          <option value="de">German</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-blue-200 mb-2">Timezone</label>
                        <select
                          value={settings.preferences.timezone}
                          onChange={(e) => handleSettingsChange('preferences', 'timezone', e.target.value)}
                          className="glass-input w-full"
                        >
                          <option value="UTC">UTC</option>
                          <option value="America/New_York">Eastern Time</option>
                          <option value="America/Chicago">Central Time</option>
                          <option value="America/Denver">Mountain Time</option>
                          <option value="America/Los_Angeles">Pacific Time</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-blue-200 mb-2">Date Format</label>
                        <select
                          value={settings.preferences.dateFormat}
                          onChange={(e) => handleSettingsChange('preferences', 'dateFormat', e.target.value)}
                          className="glass-input w-full"
                        >
                          <option value="MM/DD/YYYY">MM/DD/YYYY</option>
                          <option value="DD/MM/YYYY">DD/MM/YYYY</option>
                          <option value="YYYY-MM-DD">YYYY-MM-DD</option>
                        </select>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StudentProfileEnhanced;