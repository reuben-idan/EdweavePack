import React, { useState } from 'react';
import { BookOpen, Calendar, Users, Download, Share2, Edit, Trash2, Eye } from 'lucide-react';
import { curriculumAPI } from '../services/api';

const CurriculumCard = ({ curriculum, onEdit, onDelete, onView }) => {
  const [isExporting, setIsExporting] = useState(false);
  const [showActions, setShowActions] = useState(false);

  const handleExportPDF = async () => {
    setIsExporting(true);
    try {
      const response = await curriculumAPI.exportPDF(curriculum.id);
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${curriculum.title}_lesson_plan.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Export failed:', error);
    } finally {
      setIsExporting(false);
    }
  };

  const handleShare = async () => {
    try {
      const response = await curriculumAPI.share(curriculum.id);
      const shareUrl = response.data.shareable_link;
      
      if (navigator.share) {
        await navigator.share({
          title: curriculum.title,
          text: `Check out this curriculum: ${curriculum.title}`,
          url: shareUrl,
        });
      } else {
        await navigator.clipboard.writeText(shareUrl);
        alert('Share link copied to clipboard!');
      }
    } catch (error) {
      console.error('Share failed:', error);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getGradeLevelColor = (level) => {
    const colors = {
      'K-2': 'bg-yellow-100 text-yellow-800',
      '3-5': 'bg-green-100 text-green-800',
      '6-8': 'bg-blue-100 text-blue-800',
      '9-12': 'bg-purple-100 text-purple-800',
      'University': 'bg-indigo-100 text-indigo-800'
    };
    return colors[level] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="glass-card overflow-hidden hover-lift">
      {/* Header */}
      <div className="p-6 pb-4">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-visible mb-2 line-clamp-2">
              {curriculum.title}
            </h3>
            <p className="text-visible text-sm mb-3 line-clamp-2">
              {curriculum.description || 'No description available'}
            </p>
          </div>
          
          <div className="relative ml-4">
            <button
              onClick={() => setShowActions(!showActions)}
              className="p-2 text-visible hover:text-edu-primary rounded-full hover:bg-edu-primary/10"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
              </svg>
            </button>
            
            {showActions && (
              <div className="absolute right-0 mt-2 w-48 glass-strong rounded-md shadow-lg z-10">
                <div className="py-1">
                  <button
                    onClick={() => { onView(curriculum); setShowActions(false); }}
                    className="flex items-center px-4 py-2 text-sm text-visible hover:bg-edu-primary/10 w-full text-left"
                  >
                    <Eye className="h-4 w-4 mr-2" />
                    View Details
                  </button>
                  <button
                    onClick={() => { onEdit(curriculum); setShowActions(false); }}
                    className="flex items-center px-4 py-2 text-sm text-visible hover:bg-edu-primary/10 w-full text-left"
                  >
                    <Edit className="h-4 w-4 mr-2" />
                    Edit
                  </button>
                  <button
                    onClick={() => { handleExportPDF(); setShowActions(false); }}
                    disabled={isExporting}
                    className="flex items-center px-4 py-2 text-sm text-visible hover:bg-edu-primary/10 w-full text-left disabled:opacity-50"
                  >
                    <Download className="h-4 w-4 mr-2" />
                    Export PDF
                  </button>
                  <button
                    onClick={() => { handleShare(); setShowActions(false); }}
                    className="flex items-center px-4 py-2 text-sm text-visible hover:bg-edu-primary/10 w-full text-left"
                  >
                    <Share2 className="h-4 w-4 mr-2" />
                    Share
                  </button>
                  <hr className="my-1" />
                  <button
                    onClick={() => { onDelete(curriculum); setShowActions(false); }}
                    className="flex items-center px-4 py-2 text-sm text-edu-error hover:bg-edu-error/10 w-full text-left"
                  >
                    <Trash2 className="h-4 w-4 mr-2" />
                    Delete
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Metadata */}
        <div className="flex flex-wrap items-center gap-3 text-sm text-visible">
          <div className="flex items-center">
            <BookOpen className="h-4 w-4 mr-1" />
            <span>{curriculum.subject}</span>
          </div>
          
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getGradeLevelColor(curriculum.grade_level)}`}>
            {curriculum.grade_level}
          </span>
          
          <div className="flex items-center">
            <Calendar className="h-4 w-4 mr-1" />
            <span>{formatDate(curriculum.created_at)}</span>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="px-6 py-4 bg-edu-primary/5 border-t border-edu-primary/20">
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-lg font-semibold text-visible">
              {curriculum.metadata?.weekly_modules?.length || 0}
            </div>
            <div className="text-xs text-visible">Modules</div>
          </div>
          
          <div>
            <div className="text-lg font-semibold text-visible">
              {curriculum.metadata?.learning_objectives?.length || 0}
            </div>
            <div className="text-xs text-visible">Objectives</div>
          </div>
          
          <div>
            <div className="text-lg font-semibold text-visible">
              {curriculum.assessments?.length || 0}
            </div>
            <div className="text-xs text-visible">Assessments</div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="px-6 py-4 border-t border-edu-primary/20">
        <div className="flex space-x-2">
          <button
            onClick={() => onView(curriculum)}
            className="flex-1 px-3 py-2 text-sm font-medium text-white bg-edu-primary rounded-md hover:bg-edu-primary/90 transition-colors"
          >
            View Curriculum
          </button>
          
          <button
            onClick={handleExportPDF}
            disabled={isExporting}
            className="px-3 py-2 text-sm font-medium text-visible bg-edu-primary/10 rounded-md hover:bg-edu-primary/20 transition-colors disabled:opacity-50"
          >
            <Download className="h-4 w-4" />
          </button>
          
          <button
            onClick={handleShare}
            className="px-3 py-2 text-sm font-medium text-visible bg-edu-primary/10 rounded-md hover:bg-edu-primary/20 transition-colors"
          >
            <Share2 className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default CurriculumCard;