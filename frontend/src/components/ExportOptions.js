import React, { useState } from 'react';
import { Download, Share2, FileText, File, Link, Check } from 'lucide-react';

const ExportOptions = ({ curriculumId, curriculumTitle }) => {
  const [isExporting, setIsExporting] = useState(false);
  const [shareLink, setShareLink] = useState('');
  const [showShareModal, setShowShareModal] = useState(false);

  const handleExportPDF = async () => {
    setIsExporting(true);
    try {
      const response = await fetch(`/api/curriculum/enhanced/${curriculumId}/export/pdf`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${curriculumTitle}_lesson_plan.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      }
    } catch (error) {
      console.error('Export failed:', error);
    } finally {
      setIsExporting(false);
    }
  };

  const handleExportDOCX = async () => {
    setIsExporting(true);
    try {
      const response = await fetch(`/api/curriculum/enhanced/${curriculumId}/export/docx`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${curriculumTitle}_lesson_plan.docx`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      }
    } catch (error) {
      console.error('Export failed:', error);
    } finally {
      setIsExporting(false);
    }
  };

  const handleCreateShareLink = async () => {
    try {
      const response = await fetch(`/api/curriculum/enhanced/${curriculumId}/share`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setShareLink(data.shareable_link);
        setShowShareModal(true);
      }
    } catch (error) {
      console.error('Share link creation failed:', error);
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(shareLink);
    // Show success feedback
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Export & Share</h3>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* PDF Export */}
        <button
          onClick={handleExportPDF}
          disabled={isExporting}
          className="flex items-center justify-center p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-red-500 hover:bg-red-50 transition-colors disabled:opacity-50"
        >
          <div className="text-center">
            <FileText className="h-8 w-8 text-red-500 mx-auto mb-2" />
            <span className="text-sm font-medium text-gray-900">Export PDF</span>
            <p className="text-xs text-gray-500 mt-1">Lesson plan document</p>
          </div>
        </button>

        {/* DOCX Export */}
        <button
          onClick={handleExportDOCX}
          disabled={isExporting}
          className="flex items-center justify-center p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-colors disabled:opacity-50"
        >
          <div className="text-center">
            <File className="h-8 w-8 text-blue-500 mx-auto mb-2" />
            <span className="text-sm font-medium text-gray-900">Export DOCX</span>
            <p className="text-xs text-gray-500 mt-1">Editable document</p>
          </div>
        </button>

        {/* Share Link */}
        <button
          onClick={handleCreateShareLink}
          className="flex items-center justify-center p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-green-500 hover:bg-green-50 transition-colors"
        >
          <div className="text-center">
            <Share2 className="h-8 w-8 text-green-500 mx-auto mb-2" />
            <span className="text-sm font-medium text-gray-900">Share Link</span>
            <p className="text-xs text-gray-500 mt-1">Public view link</p>
          </div>
        </button>
      </div>

      {/* Share Modal */}
      {showShareModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <h4 className="text-lg font-semibold mb-4">Share Curriculum</h4>
            <p className="text-gray-600 mb-4">
              Anyone with this link can view your curriculum (read-only access).
            </p>
            
            <div className="flex items-center space-x-2 mb-4">
              <input
                type="text"
                value={shareLink}
                readOnly
                className="flex-1 px-3 py-2 border border-gray-300 rounded-md bg-gray-50"
              />
              <button
                onClick={copyToClipboard}
                className="px-3 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                <Link className="h-4 w-4" />
              </button>
            </div>
            
            <div className="flex justify-end space-x-2">
              <button
                onClick={() => setShowShareModal(false)}
                className="px-4 py-2 text-gray-600 hover:text-gray-800"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ExportOptions;