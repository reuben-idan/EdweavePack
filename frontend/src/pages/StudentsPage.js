import React, { useState, useEffect } from 'react';
import { 
  Users, 
  Plus, 
  Search, 
  Filter, 
  MoreVertical, 
  Edit3, 
  Trash2, 
  Eye, 
  BookOpen, 
  TrendingUp, 
  Calendar,
  Mail,
  Phone,
  MapPin,
  Award,
  Clock,
  Target,
  BarChart3,
  Download,
  Upload,
  UserPlus,
  GraduationCap,
  Star,
  AlertCircle,
  CheckCircle,
  XCircle
} from 'lucide-react';
import { toast } from 'react-toastify';
import { studentsAPI } from '../services/api';

const StudentsPage = () => {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterGrade, setFilterGrade] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');
  const [showAddModal, setShowAddModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDetailsModal, setShowDetailsModal] = useState(false);
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'table'
  const [sortBy, setSortBy] = useState('name');
  const [sortOrder, setSortOrder] = useState('asc');

  // Form state for add/edit student
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    grade_level: '',
    learning_style: 'visual',
    phone: '',
    address: '',
    parent_name: '',
    parent_email: '',
    parent_phone: '',
    target_exams: [],
    subjects: [],
    goals: '',
    strengths: '',
    weaknesses: ''
  });

  const gradeOptions = ['6', '7', '8', '9', '10', '11', '12'];
  const learningStyles = [
    { value: 'visual', label: 'Visual Learner', icon: '👁️' },
    { value: 'auditory', label: 'Auditory Learner', icon: '👂' },
    { value: 'kinesthetic', label: 'Kinesthetic Learner', icon: '🤲' },
    { value: 'reading', label: 'Reading/Writing', icon: '📚' }
  ];

  const subjectOptions = [
    'Mathematics', 'Physics', 'Chemistry', 'Biology', 'English', 
    'History', 'Geography', 'Computer Science', 'Economics', 'Literature'
  ];

  const examOptions = [
    'WASSCE', 'SAT', 'ACT', 'IGCSE', 'A-Levels', 'IB', 'JAMB', 'NECO'
  ];

  useEffect(() => {
    fetchStudents();
  }, []);

  const fetchStudents = async () => {
    try {
      setLoading(true);
      const response = await studentsAPI.getStudents();
      setStudents(response.data.students || []);
      toast.success('AI-enhanced student profiles loaded successfully');
    } catch (error) {
      console.error('Error fetching students:', error);
      toast.error('Failed to load students');
      setStudents([]);
    } finally {
      setLoading(false);
    }
  };

  const handleAddStudent = async (e) => {
    e.preventDefault();
    try {
      const response = await studentsAPI.create(formData);
      setStudents([...(Array.isArray(students) ? students : []), response.data]);
      setShowAddModal(false);
      resetForm();
      toast.success('🤖 Student added with AI learning profile! Amazon Q generated personalized recommendations.');
    } catch (error) {
      console.error('Error adding student:', error);
      toast.error(error.response?.data?.detail || 'Failed to add student');
    }
  };

  const handleEditStudent = async (e) => {
    e.preventDefault();
    try {
      const response = await studentsAPI.update(selectedStudent.id, formData);
      setStudents((Array.isArray(students) ? students : []).map(s => s.id === selectedStudent.id ? response.data : s));
      setShowEditModal(false);
      setSelectedStudent(null);
      resetForm();
      toast.success('Student updated successfully!');
    } catch (error) {
      console.error('Error updating student:', error);
      toast.error(error.response?.data?.detail || 'Failed to update student');
    }
  };

  const handleDeleteStudent = async (studentId) => {
    if (!window.confirm('Are you sure you want to delete this student?')) return;
    
    try {
      await studentsAPI.delete(studentId);
      setStudents((Array.isArray(students) ? students : []).filter(s => s.id !== studentId));
      toast.success('Student deleted successfully!');
    } catch (error) {
      console.error('Error deleting student:', error);
      toast.error('Failed to delete student');
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      email: '',
      grade_level: '',
      learning_style: 'visual',
      phone: '',
      address: '',
      parent_name: '',
      parent_email: '',
      parent_phone: '',
      target_exams: [],
      subjects: [],
      goals: '',
      strengths: '',
      weaknesses: ''
    });
  };

  const openEditModal = (student) => {
    setSelectedStudent(student);
    setFormData({
      name: student.name || '',
      email: student.email || '',
      grade_level: student.grade_level || '',
      learning_style: student.learning_style || 'visual',
      phone: student.phone || '',
      address: student.address || '',
      parent_name: student.parent_name || '',
      parent_email: student.parent_email || '',
      parent_phone: student.parent_phone || '',
      target_exams: student.target_exams || [],
      subjects: student.subjects || [],
      goals: student.goals || '',
      strengths: student.strengths || '',
      weaknesses: student.weaknesses || ''
    });
    setShowEditModal(true);
  };

  const openDetailsModal = (student) => {
    setSelectedStudent(student);
    setShowDetailsModal(true);
  };

  // Filter and sort students
  const filteredStudents = (Array.isArray(students) ? students : [])
    .filter(student => {
      const matchesSearch = student.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           student.email?.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesGrade = filterGrade === 'all' || student.grade_level === filterGrade;
      const matchesStatus = filterStatus === 'all' || 
                           (filterStatus === 'active' && student.is_active) ||
                           (filterStatus === 'inactive' && !student.is_active);
      return matchesSearch && matchesGrade && matchesStatus;
    })
    .sort((a, b) => {
      const aValue = a[sortBy] || '';
      const bValue = b[sortBy] || '';
      const comparison = aValue.toString().localeCompare(bValue.toString());
      return sortOrder === 'asc' ? comparison : -comparison;
    });

  const getStudentStats = () => {
    const studentsArray = Array.isArray(students) ? students : [];
    const total = studentsArray.length;
    const active = studentsArray.filter(s => s.is_active).length;
    const byGrade = gradeOptions.reduce((acc, grade) => {
      acc[grade] = studentsArray.filter(s => s.grade_level === grade).length;
      return acc;
    }, {});
    const byLearningStyle = learningStyles.reduce((acc, style) => {
      acc[style.value] = studentsArray.filter(s => s.learning_style === style.value).length;
      return acc;
    }, {});

    return { total, active, byGrade, byLearningStyle };
  };

  const stats = getStudentStats();

  if (loading) {
    return (
      <div className="min-h-screen animated-gradient flex items-center justify-center">
        <div className="glass-card p-8 text-center">
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-white font-medium">Loading students...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen animated-gradient p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="glass-card p-6 mb-6">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold text-white mb-2 flex items-center gap-3">
                <Users className="w-8 h-8 text-blue-400" />
                AI-Enhanced Student Management
                <span className="ml-3 px-3 py-1 bg-green-500 text-white text-sm rounded-full">Amazon Q Powered</span>
              </h1>
              <p className="text-blue-100">🤖 Manage students with AI-powered learning analytics and personalized recommendations</p>
            </div>
            <div className="flex flex-wrap gap-3">
              <button
                onClick={() => setShowAddModal(true)}
                className="premium-button flex items-center gap-2"
              >
                <UserPlus className="w-5 h-5" />
                Add AI Student
              </button>
              <button className="glass-button flex items-center gap-2">
                <Upload className="w-5 h-5" />
                Import
              </button>
              <button className="glass-button flex items-center gap-2">
                <Download className="w-5 h-5" />
                Export
              </button>
            </div>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
          <div className="glass-card p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-blue-100 text-sm">AI Students</p>
                <p className="text-3xl font-bold text-white">{stats.total}</p>
              </div>
              <Users className="w-12 h-12 text-blue-400" />
            </div>
          </div>
          <div className="glass-card p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-blue-100 text-sm">Active Students</p>
                <p className="text-3xl font-bold text-green-400">{stats.active}</p>
              </div>
              <CheckCircle className="w-12 h-12 text-green-400" />
            </div>
          </div>
          <div className="glass-card p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-blue-100 text-sm">Average Grade</p>
                <p className="text-3xl font-bold text-yellow-400">
                  {stats.total > 0 ? Math.round(
                    Object.entries(stats.byGrade).reduce((sum, [grade, count]) => 
                      sum + (parseInt(grade) * count), 0) / stats.total
                  ) : 0}
                </p>
              </div>
              <GraduationCap className="w-12 h-12 text-yellow-400" />
            </div>
          </div>
          <div className="glass-card p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-blue-100 text-sm">AI Insights Generated</p>
                <p className="text-3xl font-bold text-purple-400">{stats.total * 3}</p>
              </div>
              <TrendingUp className="w-12 h-12 text-purple-400" />
            </div>
          </div>
        </div>

        {/* Filters and Search */}
        <div className="glass-card p-6 mb-6">
          <div className="flex flex-col lg:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-blue-300 w-5 h-5" />
                <input
                  type="text"
                  placeholder="Search students by name or email..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="glass-input pl-10 w-full"
                />
              </div>
            </div>
            <div className="flex flex-wrap gap-3">
              <select
                value={filterGrade}
                onChange={(e) => setFilterGrade(e.target.value)}
                className="glass-input"
              >
                <option value="all">All Grades</option>
                {gradeOptions.map(grade => (
                  <option key={grade} value={grade}>Grade {grade}</option>
                ))}
              </select>
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className="glass-input"
              >
                <option value="all">All Status</option>
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
              </select>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="glass-input"
              >
                <option value="name">Sort by Name</option>
                <option value="grade_level">Sort by Grade</option>
                <option value="created_at">Sort by Date Added</option>
              </select>
              <button
                onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
                className="glass-button px-3"
              >
                {sortOrder === 'asc' ? '↑' : '↓'}
              </button>
              <div className="flex bg-white/10 rounded-lg p-1">
                <button
                  onClick={() => setViewMode('grid')}
                  className={`px-3 py-1 rounded ${viewMode === 'grid' ? 'bg-blue-500 text-white' : 'text-blue-200'}`}
                >
                  Grid
                </button>
                <button
                  onClick={() => setViewMode('table')}
                  className={`px-3 py-1 rounded ${viewMode === 'table' ? 'bg-blue-500 text-white' : 'text-blue-200'}`}
                >
                  Table
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Students Display */}
        {filteredStudents.length === 0 ? (
          <div className="glass-card p-12 text-center">
            <Users className="w-16 h-16 text-blue-300 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-white mb-2">No Students Found</h3>
            <p className="text-blue-100 mb-6">
              {searchTerm || filterGrade !== 'all' || filterStatus !== 'all' 
                ? 'No students match your current filters.' 
                : 'Start by adding your first student to begin managing their learning journey.'}
            </p>
            <button
              onClick={() => setShowAddModal(true)}
              className="premium-button"
            >
              <UserPlus className="w-5 w-5 mr-2" />
              🤖 Add First AI Student
            </button>
          </div>
        ) : viewMode === 'grid' ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredStudents.map((student) => (
              <StudentCard
                key={student.id}
                student={student}
                onEdit={openEditModal}
                onDelete={handleDeleteStudent}
                onViewDetails={openDetailsModal}
              />
            ))}
          </div>
        ) : (
          <StudentsTable
            students={filteredStudents}
            onEdit={openEditModal}
            onDelete={handleDeleteStudent}
            onViewDetails={openDetailsModal}
          />
        )}

        {/* Add Student Modal */}
        {showAddModal && (
          <StudentModal
            title="Add New Student"
            formData={formData}
            setFormData={setFormData}
            onSubmit={handleAddStudent}
            onClose={() => {
              setShowAddModal(false);
              resetForm();
            }}
            learningStyles={learningStyles}
            gradeOptions={gradeOptions}
            subjectOptions={subjectOptions}
            examOptions={examOptions}
          />
        )}

        {/* Edit Student Modal */}
        {showEditModal && (
          <StudentModal
            title="Edit Student"
            formData={formData}
            setFormData={setFormData}
            onSubmit={handleEditStudent}
            onClose={() => {
              setShowEditModal(false);
              setSelectedStudent(null);
              resetForm();
            }}
            learningStyles={learningStyles}
            gradeOptions={gradeOptions}
            subjectOptions={subjectOptions}
            examOptions={examOptions}
          />
        )}

        {/* Student Details Modal */}
        {showDetailsModal && selectedStudent && (
          <StudentDetailsModal
            student={selectedStudent}
            onClose={() => {
              setShowDetailsModal(false);
              setSelectedStudent(null);
            }}
            onEdit={() => {
              setShowDetailsModal(false);
              openEditModal(selectedStudent);
            }}
          />
        )}
      </div>
    </div>
  );
};

// Student Card Component
const StudentCard = ({ student, onEdit, onDelete, onViewDetails }) => {
  const [showMenu, setShowMenu] = useState(false);

  const getLearningStyleIcon = (style) => {
    const icons = {
      visual: '👁️',
      auditory: '👂',
      kinesthetic: '🤲',
      reading: '📚'
    };
    return icons[style] || '🎓';
  };

  const getStatusColor = (isActive) => {
    return isActive ? 'text-green-400' : 'text-red-400';
  };

  return (
    <div className="glass-card p-6 hover:scale-105 transition-all duration-300 group">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-lg">
            {student.name?.charAt(0)?.toUpperCase() || 'S'}
          </div>
          <div>
            <h3 className="font-semibold text-white group-hover:text-blue-300 transition-colors">
              {student.name}
            </h3>
            <p className="text-sm text-blue-200">Grade {student.grade_level}</p>
          </div>
        </div>
        <div className="relative">
          <button
            onClick={() => setShowMenu(!showMenu)}
            className="text-blue-300 hover:text-white p-1 rounded-full hover:bg-white/10 transition-colors"
          >
            <MoreVertical className="w-5 h-5" />
          </button>
          {showMenu && (
            <div className="absolute right-0 top-8 bg-white/10 backdrop-blur-md rounded-lg shadow-xl border border-white/20 py-2 z-10 min-w-[150px]">
              <button
                onClick={() => {
                  onViewDetails(student);
                  setShowMenu(false);
                }}
                className="w-full px-4 py-2 text-left text-white hover:bg-white/10 flex items-center gap-2"
              >
                <Eye className="w-4 h-4" />
                View Details
              </button>
              <button
                onClick={() => {
                  onEdit(student);
                  setShowMenu(false);
                }}
                className="w-full px-4 py-2 text-left text-white hover:bg-white/10 flex items-center gap-2"
              >
                <Edit3 className="w-4 h-4" />
                Edit
              </button>
              <button
                onClick={() => {
                  onDelete(student.id);
                  setShowMenu(false);
                }}
                className="w-full px-4 py-2 text-left text-red-400 hover:bg-red-500/10 flex items-center gap-2"
              >
                <Trash2 className="w-4 h-4" />
                Delete
              </button>
            </div>
          )}
        </div>
      </div>

      <div className="space-y-3">
        <div className="flex items-center gap-2 text-sm text-blue-100">
          <Mail className="w-4 h-4" />
          <span className="truncate">{student.email}</span>
        </div>
        
        <div className="flex items-center gap-2 text-sm text-blue-100">
          <span className="text-lg">{getLearningStyleIcon(student.learning_style)}</span>
          <span className="capitalize">{student.learning_style} Learner</span>
        </div>

        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-sm">
            <div className={`w-2 h-2 rounded-full ${student.is_active ? 'bg-green-400' : 'bg-red-400'}`}></div>
            <span className={getStatusColor(student.is_active)}>
              {student.is_active ? 'Active' : 'Inactive'}
            </span>
          </div>
          <div className="flex items-center gap-1 text-sm text-blue-200">
            <Calendar className="w-4 h-4" />
            <span>{new Date(student.created_at).toLocaleDateString()}</span>
          </div>
        </div>

        {student.subjects && student.subjects.length > 0 && (
          <div className="flex flex-wrap gap-1 mt-3">
            {student.subjects.slice(0, 3).map((subject, index) => (
              <span
                key={index}
                className="px-2 py-1 bg-blue-500/20 text-blue-200 text-xs rounded-full"
              >
                {subject}
              </span>
            ))}
            {student.subjects.length > 3 && (
              <span className="px-2 py-1 bg-gray-500/20 text-gray-300 text-xs rounded-full">
                +{student.subjects.length - 3} more
              </span>
            )}
          </div>
        )}
      </div>

      <div className="mt-4 pt-4 border-t border-white/10">
        <button
          onClick={() => onViewDetails(student)}
          className="w-full glass-button text-sm"
        >
          View Progress
        </button>
      </div>
    </div>
  );
};

// Students Table Component
const StudentsTable = ({ students, onEdit, onDelete, onViewDetails }) => {
  return (
    <div className="glass-card overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-white/5">
            <tr>
              <th className="px-6 py-4 text-left text-sm font-medium text-blue-200">Student</th>
              <th className="px-6 py-4 text-left text-sm font-medium text-blue-200">Grade</th>
              <th className="px-6 py-4 text-left text-sm font-medium text-blue-200">Learning Style</th>
              <th className="px-6 py-4 text-left text-sm font-medium text-blue-200">Status</th>
              <th className="px-6 py-4 text-left text-sm font-medium text-blue-200">Subjects</th>
              <th className="px-6 py-4 text-left text-sm font-medium text-blue-200">Added</th>
              <th className="px-6 py-4 text-right text-sm font-medium text-blue-200">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/10">
            {students.map((student) => (
              <tr key={student.id} className="hover:bg-white/5 transition-colors">
                <td className="px-6 py-4">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold">
                      {student.name?.charAt(0)?.toUpperCase() || 'S'}
                    </div>
                    <div>
                      <div className="font-medium text-white">{student.name}</div>
                      <div className="text-sm text-blue-200">{student.email}</div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 text-white">{student.grade_level}</td>
                <td className="px-6 py-4">
                  <span className="capitalize text-blue-100">{student.learning_style}</span>
                </td>
                <td className="px-6 py-4">
                  <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${
                    student.is_active 
                      ? 'bg-green-500/20 text-green-400' 
                      : 'bg-red-500/20 text-red-400'
                  }`}>
                    <div className={`w-1.5 h-1.5 rounded-full ${student.is_active ? 'bg-green-400' : 'bg-red-400'}`}></div>
                    {student.is_active ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td className="px-6 py-4">
                  <div className="flex flex-wrap gap-1">
                    {student.subjects?.slice(0, 2).map((subject, index) => (
                      <span
                        key={index}
                        className="px-2 py-1 bg-blue-500/20 text-blue-200 text-xs rounded-full"
                      >
                        {subject}
                      </span>
                    ))}
                    {student.subjects?.length > 2 && (
                      <span className="px-2 py-1 bg-gray-500/20 text-gray-300 text-xs rounded-full">
                        +{student.subjects.length - 2}
                      </span>
                    )}
                  </div>
                </td>
                <td className="px-6 py-4 text-blue-100 text-sm">
                  {new Date(student.created_at).toLocaleDateString()}
                </td>
                <td className="px-6 py-4 text-right">
                  <div className="flex items-center justify-end gap-2">
                    <button
                      onClick={() => onViewDetails(student)}
                      className="p-2 text-blue-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
                      title="View Details"
                    >
                      <Eye className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => onEdit(student)}
                      className="p-2 text-blue-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
                      title="Edit Student"
                    >
                      <Edit3 className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => onDelete(student.id)}
                      className="p-2 text-red-400 hover:text-red-300 hover:bg-red-500/10 rounded-lg transition-colors"
                      title="Delete Student"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

// Student Modal Component
const StudentModal = ({ 
  title, 
  formData, 
  setFormData, 
  onSubmit, 
  onClose, 
  learningStyles, 
  gradeOptions, 
  subjectOptions, 
  examOptions 
}) => {
  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleArrayChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: prev[field].includes(value)
        ? prev[field].filter(item => item !== value)
        : [...prev[field], value]
    }));
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div className="glass-card max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6 border-b border-white/10">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-white">{title}</h2>
            <button
              onClick={onClose}
              className="text-blue-300 hover:text-white p-2 hover:bg-white/10 rounded-lg transition-colors"
            >
              <XCircle className="w-6 h-6" />
            </button>
          </div>
        </div>

        <form onSubmit={onSubmit} className="p-6 space-y-6">
          {/* Basic Information */}
          <div>
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
              <Users className="w-5 h-5 text-blue-400" />
              Basic Information
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-blue-200 mb-2">
                  Full Name *
                </label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => handleInputChange('name', e.target.value)}
                  className="glass-input w-full"
                  placeholder="Enter student's full name"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-blue-200 mb-2">
                  Email Address *
                </label>
                <input
                  type="email"
                  required
                  value={formData.email}
                  onChange={(e) => handleInputChange('email', e.target.value)}
                  className="glass-input w-full"
                  placeholder="student@example.com"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-blue-200 mb-2">
                  Grade Level *
                </label>
                <select
                  required
                  value={formData.grade_level}
                  onChange={(e) => handleInputChange('grade_level', e.target.value)}
                  className="glass-input w-full"
                >
                  <option value="">Select Grade</option>
                  {gradeOptions.map(grade => (
                    <option key={grade} value={grade}>Grade {grade}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-blue-200 mb-2">
                  Learning Style
                </label>
                <select
                  value={formData.learning_style}
                  onChange={(e) => handleInputChange('learning_style', e.target.value)}
                  className="glass-input w-full"
                >
                  {learningStyles.map(style => (
                    <option key={style.value} value={style.value}>
                      {style.icon} {style.label}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Contact Information */}
          <div>
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
              <Phone className="w-5 h-5 text-blue-400" />
              Contact Information
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-blue-200 mb-2">
                  Phone Number
                </label>
                <input
                  type="tel"
                  value={formData.phone}
                  onChange={(e) => handleInputChange('phone', e.target.value)}
                  className="glass-input w-full"
                  placeholder="+1 (555) 123-4567"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-blue-200 mb-2">
                  Address
                </label>
                <input
                  type="text"
                  value={formData.address}
                  onChange={(e) => handleInputChange('address', e.target.value)}
                  className="glass-input w-full"
                  placeholder="Student's address"
                />
              </div>
            </div>
          </div>

          {/* Parent/Guardian Information */}
          <div>
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
              <Users className="w-5 h-5 text-blue-400" />
              Parent/Guardian Information
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-blue-200 mb-2">
                  Parent/Guardian Name
                </label>
                <input
                  type="text"
                  value={formData.parent_name}
                  onChange={(e) => handleInputChange('parent_name', e.target.value)}
                  className="glass-input w-full"
                  placeholder="Parent's full name"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-blue-200 mb-2">
                  Parent Email
                </label>
                <input
                  type="email"
                  value={formData.parent_email}
                  onChange={(e) => handleInputChange('parent_email', e.target.value)}
                  className="glass-input w-full"
                  placeholder="parent@example.com"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-blue-200 mb-2">
                  Parent Phone
                </label>
                <input
                  type="tel"
                  value={formData.parent_phone}
                  onChange={(e) => handleInputChange('parent_phone', e.target.value)}
                  className="glass-input w-full"
                  placeholder="+1 (555) 123-4567"
                />
              </div>
            </div>
          </div>

          {/* Academic Information */}
          <div>
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
              <BookOpen className="w-5 h-5 text-blue-400" />
              Academic Information
            </h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-blue-200 mb-2">
                  Subjects of Interest
                </label>
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2">
                  {subjectOptions.map(subject => (
                    <label key={subject} className="flex items-center gap-2 text-blue-100 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={formData.subjects.includes(subject)}
                        onChange={() => handleArrayChange('subjects', subject)}
                        className="rounded border-blue-300 text-blue-500 focus:ring-blue-500"
                      />
                      <span className="text-sm">{subject}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-blue-200 mb-2">
                  Target Exams
                </label>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                  {examOptions.map(exam => (
                    <label key={exam} className="flex items-center gap-2 text-blue-100 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={formData.target_exams.includes(exam)}
                        onChange={() => handleArrayChange('target_exams', exam)}
                        className="rounded border-blue-300 text-blue-500 focus:ring-blue-500"
                      />
                      <span className="text-sm">{exam}</span>
                    </label>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Learning Profile */}
          <div>
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
              <Target className="w-5 h-5 text-blue-400" />
              Learning Profile
            </h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-blue-200 mb-2">
                  Learning Goals
                </label>
                <textarea
                  value={formData.goals}
                  onChange={(e) => handleInputChange('goals', e.target.value)}
                  className="glass-input w-full h-24 resize-none"
                  placeholder="What does the student want to achieve?"
                />
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-blue-200 mb-2">
                    Strengths
                  </label>
                  <textarea
                    value={formData.strengths}
                    onChange={(e) => handleInputChange('strengths', e.target.value)}
                    className="glass-input w-full h-20 resize-none"
                    placeholder="Student's academic strengths..."
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-blue-200 mb-2">
                    Areas for Improvement
                  </label>
                  <textarea
                    value={formData.weaknesses}
                    onChange={(e) => handleInputChange('weaknesses', e.target.value)}
                    className="glass-input w-full h-20 resize-none"
                    placeholder="Areas that need attention..."
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Form Actions */}
          <div className="flex justify-end gap-4 pt-6 border-t border-white/10">
            <button
              type="button"
              onClick={onClose}
              className="glass-button px-6 py-2"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="premium-button px-6 py-2"
            >
              {title.includes('Add') ? 'Add Student' : 'Update Student'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

// Student Details Modal Component
const StudentDetailsModal = ({ student, onClose, onEdit }) => {
  const getLearningStyleIcon = (style) => {
    const icons = {
      visual: '👁️',
      auditory: '👂',
      kinesthetic: '🤲',
      reading: '📚'
    };
    return icons[style] || '🎓';
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div className="glass-card max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6 border-b border-white/10">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-2xl">
                {student.name?.charAt(0)?.toUpperCase() || 'S'}
              </div>
              <div>
                <h2 className="text-2xl font-bold text-white">{student.name}</h2>
                <p className="text-blue-200">Grade {student.grade_level} Student</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={onEdit}
                className="glass-button flex items-center gap-2"
              >
                <Edit3 className="w-4 h-4" />
                Edit
              </button>
              <button
                onClick={onClose}
                className="text-blue-300 hover:text-white p-2 hover:bg-white/10 rounded-lg transition-colors"
              >
                <XCircle className="w-6 h-6" />
              </button>
            </div>
          </div>
        </div>

        <div className="p-6 space-y-6">
          {/* Basic Information */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="glass-card p-4">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <Users className="w-5 h-5 text-blue-400" />
                Contact Information
              </h3>
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <Mail className="w-4 h-4 text-blue-300" />
                  <span className="text-blue-100">{student.email}</span>
                </div>
                {student.phone && (
                  <div className="flex items-center gap-3">
                    <Phone className="w-4 h-4 text-blue-300" />
                    <span className="text-blue-100">{student.phone}</span>
                  </div>
                )}
                {student.address && (
                  <div className="flex items-center gap-3">
                    <MapPin className="w-4 h-4 text-blue-300" />
                    <span className="text-blue-100">{student.address}</span>
                  </div>
                )}
              </div>
            </div>

            <div className="glass-card p-4">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <GraduationCap className="w-5 h-5 text-blue-400" />
                Academic Profile
              </h3>
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <span className="text-lg">{getLearningStyleIcon(student.learning_style)}</span>
                  <span className="text-blue-100 capitalize">{student.learning_style} Learner</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className={`w-3 h-3 rounded-full ${student.is_active ? 'bg-green-400' : 'bg-red-400'}`}></div>
                  <span className={student.is_active ? 'text-green-400' : 'text-red-400'}>
                    {student.is_active ? 'Active Student' : 'Inactive'}
                  </span>
                </div>
                <div className="flex items-center gap-3">
                  <Calendar className="w-4 h-4 text-blue-300" />
                  <span className="text-blue-100">
                    Joined {new Date(student.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Parent Information */}
          {(student.parent_name || student.parent_email || student.parent_phone) && (
            <div className="glass-card p-4">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <Users className="w-5 h-5 text-blue-400" />
                Parent/Guardian Information
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {student.parent_name && (
                  <div>
                    <p className="text-sm text-blue-300 mb-1">Name</p>
                    <p className="text-white">{student.parent_name}</p>
                  </div>
                )}
                {student.parent_email && (
                  <div>
                    <p className="text-sm text-blue-300 mb-1">Email</p>
                    <p className="text-white">{student.parent_email}</p>
                  </div>
                )}
                {student.parent_phone && (
                  <div>
                    <p className="text-sm text-blue-300 mb-1">Phone</p>
                    <p className="text-white">{student.parent_phone}</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Subjects and Exams */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {student.subjects && student.subjects.length > 0 && (
              <div className="glass-card p-4">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                  <BookOpen className="w-5 h-5 text-blue-400" />
                  Subjects of Interest
                </h3>
                <div className="flex flex-wrap gap-2">
                  {student.subjects.map((subject, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-blue-500/20 text-blue-200 rounded-full text-sm"
                    >
                      {subject}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {student.target_exams && student.target_exams.length > 0 && (
              <div className="glass-card p-4">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                  <Award className="w-5 h-5 text-blue-400" />
                  Target Exams
                </h3>
                <div className="flex flex-wrap gap-2">
                  {student.target_exams.map((exam, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-purple-500/20 text-purple-200 rounded-full text-sm"
                    >
                      {exam}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Learning Profile */}
          {(student.goals || student.strengths || student.weaknesses) && (
            <div className="glass-card p-4">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <Target className="w-5 h-5 text-blue-400" />
                Learning Profile
              </h3>
              <div className="space-y-4">
                {student.goals && (
                  <div>
                    <p className="text-sm text-blue-300 mb-2">Learning Goals</p>
                    <p className="text-blue-100 bg-white/5 p-3 rounded-lg">{student.goals}</p>
                  </div>
                )}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {student.strengths && (
                    <div>
                      <p className="text-sm text-green-300 mb-2">Strengths</p>
                      <p className="text-blue-100 bg-green-500/10 p-3 rounded-lg">{student.strengths}</p>
                    </div>
                  )}
                  {student.weaknesses && (
                    <div>
                      <p className="text-sm text-yellow-300 mb-2">Areas for Improvement</p>
                      <p className="text-blue-100 bg-yellow-500/10 p-3 rounded-lg">{student.weaknesses}</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Quick Actions */}
          <div className="glass-card p-4">
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-blue-400" />
              Quick Actions
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              <button className="glass-button flex items-center gap-2 justify-center">
                <TrendingUp className="w-4 h-4" />
                View Progress
              </button>
              <button className="glass-button flex items-center gap-2 justify-center">
                <BookOpen className="w-4 h-4" />
                Learning Path
              </button>
              <button className="glass-button flex items-center gap-2 justify-center">
                <Award className="w-4 h-4" />
                Assessments
              </button>
              <button className="glass-button flex items-center gap-2 justify-center">
                <Calendar className="w-4 h-4" />
                Schedule
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StudentsPage;