import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import FileUploader from '../components/FileUploader';
import LevelSelector from '../components/LevelSelector';
import { filesAPI, curriculumAPI } from '../services/api';
import { FileText, ArrowRight, CheckCircle, AlertCircle } from 'lucide-react';

const UploadPage = () => {
  const [step, setStep] = useState(1);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [curriculumData, setCurriculumData] = useState({
    title: '',
    description: '',
    subject: '',
    grade_level: '',
    source_content: ''
  });
  const [isCreating, setIsCreating] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    fetchUploadedFiles();
  }, []);

  const fetchUploadedFiles = async () => {
    // Use mock uploaded files for now
    setUploadedFiles([
      {
        id: 1,
        filename: 'Sample Curriculum.pdf',
        file_size: 2048000,
        content_type: 'application/pdf',
        upload_status: 'completed',
        created_at: new Date().toISOString(),
        has_content: true
      }
    ]);
  };

  const handleUploadComplete = (result) => {
    // Add the uploaded file to the list
    const newFile = {
      id: Date.now(),
      filename: result.filename,
      file_size: 1024000,
      content_type: 'application/pdf',
      upload_status: 'completed',
      created_at: new Date().toISOString(),
      has_content: true,
      extracted_content: result.full_content || result.content
    };
    setUploadedFiles(prev => [...prev, newFile]);
  };

  const handleFileSelect = (file) => {
    setSelectedFiles(prev => {
      const isSelected = prev.some(f => f.id === file.id);
      if (isSelected) {
        return prev.filter(f => f.id !== file.id);
      } else {
        return [...prev, file];
      }
    });
  };

  const handleLevelSelect = (level) => {
    setCurriculumData(prev => ({ ...prev, grade_level: level }));
  };

  const combineSelectedContent = async () => {
    let combinedContent = '';
    
    for (const file of selectedFiles) {
      const content = file.extracted_content || `Sample content from ${file.filename}. This would contain the actual extracted text from the uploaded file.`;
      combinedContent += `\n\n--- ${file.filename} ---\n${content}\n`;
    }
    
    return combinedContent.trim();
  };

  const handleCreateCurriculum = async () => {
    if (!curriculumData.title || !curriculumData.subject || !curriculumData.grade_level) {
      alert('Please fill in all required fields');
      return;
    }

    if (selectedFiles.length === 0) {
      alert('Please select at least one file');
      return;
    }

    setIsCreating(true);
    
    try {
      const sourceContent = await combineSelectedContent();
      
      const payload = {
        ...curriculumData,
        source_content: sourceContent
      };

      const response = await curriculumAPI.create(payload);
      
      // Navigate to curriculum page
      navigate(`/curriculum/${response.data.id}`);
      
    } catch (error) {
      console.error('Failed to create curriculum:', error);
      alert('Failed to create curriculum. Please try again.');
    } finally {
      setIsCreating(false);
    }
  };

  const canProceedToStep2 = uploadedFiles.length > 0;
  const canProceedToStep3 = selectedFiles.length > 0;
  const canCreateCurriculum = curriculumData.title && curriculumData.subject && curriculumData.grade_level && selectedFiles.length > 0;

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Create New Curriculum
          </h1>
          <p className="text-gray-600">
            Upload your teaching materials and let AI transform them into structured curricula
          </p>
        </div>

        {/* Progress Steps */}
        <div className="flex items-center justify-center mb-8">
          <div className="flex items-center space-x-4">
            {[1, 2, 3].map((stepNumber) => (
              <React.Fragment key={stepNumber}>
                <div className={`flex items-center justify-center w-8 h-8 rounded-full ${
                  step >= stepNumber 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-200 text-gray-600'
                }`}>
                  {step > stepNumber ? (
                    <CheckCircle className="h-5 w-5" />
                  ) : (
                    stepNumber
                  )}
                </div>
                {stepNumber < 3 && (
                  <ArrowRight className={`h-4 w-4 ${
                    step > stepNumber ? 'text-blue-600' : 'text-gray-400'
                  }`} />
                )}
              </React.Fragment>
            ))}
          </div>
        </div>

        {/* Step Labels */}
        <div className="flex justify-center mb-8">
          <div className="grid grid-cols-3 gap-8 text-center text-sm">
            <div className={step >= 1 ? 'text-blue-600 font-medium' : 'text-gray-500'}>
              Upload Files
            </div>
            <div className={step >= 2 ? 'text-blue-600 font-medium' : 'text-gray-500'}>
              Select Content
            </div>
            <div className={step >= 3 ? 'text-blue-600 font-medium' : 'text-gray-500'}>
              Configure Curriculum
            </div>
          </div>
        </div>

        {/* Step Content */}
        <div className="bg-white rounded-lg shadow-md p-6">
          {/* Step 1: Upload Files */}
          {step === 1 && (
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Step 1: Upload Teaching Materials
              </h2>
              
              <FileUploader onUploadComplete={handleUploadComplete} />
              
              {uploadedFiles.length > 0 && (
                <div className="mt-6">
                  <h3 className="text-lg font-medium text-gray-900 mb-3">
                    Uploaded Files ({uploadedFiles.length})
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {uploadedFiles.map((file) => (
                      <div key={file.id} className="flex items-center p-3 bg-green-50 border border-green-200 rounded-lg">
                        <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                        <div className="flex-1">
                          <p className="text-sm font-medium text-gray-900">{file.filename}</p>
                          <p className="text-xs text-gray-500">
                            {(file.file_size / 1024).toFixed(1)} KB • {file.content_type}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              <div className="flex justify-end mt-6">
                <button
                  onClick={() => setStep(2)}
                  disabled={!canProceedToStep2}
                  className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Next: Select Content
                </button>
              </div>
            </div>
          )}

          {/* Step 2: Select Files */}
          {step === 2 && (
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Step 2: Select Content for Curriculum
              </h2>
              
              <p className="text-gray-600 mb-4">
                Choose which uploaded files to include in your curriculum generation.
              </p>
              
              <div className="space-y-3">
                {uploadedFiles.map((file) => (
                  <div
                    key={file.id}
                    className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                      selectedFiles.some(f => f.id === file.id)
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                    onClick={() => handleFileSelect(file)}
                  >
                    <div className="flex items-center">
                      <input
                        type="checkbox"
                        checked={selectedFiles.some(f => f.id === file.id)}
                        onChange={() => handleFileSelect(file)}
                        className="mr-3"
                      />
                      <FileText className="h-5 w-5 text-gray-400 mr-3" />
                      <div className="flex-1">
                        <p className="font-medium text-gray-900">{file.filename}</p>
                        <p className="text-sm text-gray-500">
                          {(file.file_size / 1024).toFixed(1)} KB • Uploaded {new Date(file.created_at).toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              
              <div className="flex justify-between mt-6">
                <button
                  onClick={() => setStep(1)}
                  className="px-6 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50"
                >
                  Back
                </button>
                <button
                  onClick={() => setStep(3)}
                  disabled={!canProceedToStep3}
                  className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Next: Configure
                </button>
              </div>
            </div>
          )}

          {/* Step 3: Configure Curriculum */}
          {step === 3 && (
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Step 3: Configure Your Curriculum
              </h2>
              
              <div className="space-y-6">
                {/* Basic Information */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Curriculum Title *
                    </label>
                    <input
                      type="text"
                      value={curriculumData.title}
                      onChange={(e) => setCurriculumData(prev => ({ ...prev, title: e.target.value }))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="e.g., Introduction to Biology"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Subject *
                    </label>
                    <select
                      value={curriculumData.subject}
                      onChange={(e) => setCurriculumData(prev => ({ ...prev, subject: e.target.value }))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="">Select Subject</option>
                      <option value="Mathematics">Mathematics</option>
                      <option value="Science">Science</option>
                      <option value="English">English</option>
                      <option value="History">History</option>
                      <option value="Geography">Geography</option>
                      <option value="Computer Science">Computer Science</option>
                      <option value="Art">Art</option>
                      <option value="Music">Music</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Description (Optional)
                  </label>
                  <textarea
                    value={curriculumData.description}
                    onChange={(e) => setCurriculumData(prev => ({ ...prev, description: e.target.value }))}
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Brief description of the curriculum..."
                  />
                </div>

                {/* Education Level Selection */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Education Level *
                  </label>
                  <LevelSelector
                    onLevelSelect={handleLevelSelect}
                    selectedLevel={curriculumData.grade_level}
                  />
                </div>

                {/* Selected Files Summary */}
                <div>
                  <h3 className="text-sm font-medium text-gray-700 mb-2">
                    Selected Files ({selectedFiles.length})
                  </h3>
                  <div className="bg-gray-50 rounded-lg p-3">
                    {selectedFiles.map((file) => (
                      <div key={file.id} className="flex items-center text-sm text-gray-600 mb-1">
                        <FileText className="h-4 w-4 mr-2" />
                        {file.filename}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
              
              <div className="flex justify-between mt-8">
                <button
                  onClick={() => setStep(2)}
                  className="px-6 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50"
                >
                  Back
                </button>
                <button
                  onClick={handleCreateCurriculum}
                  disabled={!canCreateCurriculum || isCreating}
                  className="px-6 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
                >
                  {isCreating && (
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" />
                  )}
                  <span>{isCreating ? 'Creating Curriculum...' : 'Create Curriculum'}</span>
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default UploadPage;