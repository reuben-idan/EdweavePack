import React, { useState, useCallback } from 'react';
import { Upload, File, Link, CheckCircle, AlertCircle, Loader } from 'lucide-react';
import { filesAPI, tasksAPI } from '../services/api';

const FileUploader = ({ onUploadComplete }) => {
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState({});
  const [urlInput, setUrlInput] = useState('');

  const handleDrag = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files);
    }
  }, []);

  const handleFiles = async (files) => {
    const fileArray = Array.from(files);
    
    for (const file of fileArray) {
      await uploadFile(file);
    }
  };

  const uploadFile = async (file) => {
    const fileId = Date.now() + Math.random();
    setUploadProgress(prev => ({
      ...prev,
      [fileId]: { name: file.name, status: 'uploading', progress: 0 }
    }));

    try {
      // Simulate upload progress
      setUploadProgress(prev => ({
        ...prev,
        [fileId]: { ...prev[fileId], progress: 50 }
      }));
      
      // Simulate processing time
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setUploadProgress(prev => ({
        ...prev,
        [fileId]: { ...prev[fileId], progress: 100, status: 'completed' }
      }));
      
      // Mock successful result
      const mockResult = {
        filename: file.name,
        content: `Content extracted from ${file.name}`,
        full_content: `Detailed curriculum content from ${file.name}`
      };
      
      if (onUploadComplete) {
        onUploadComplete(mockResult);
      }
      
      // Remove from progress after 3 seconds
      setTimeout(() => {
        setUploadProgress(prev => {
          const newProgress = { ...prev };
          delete newProgress[fileId];
          return newProgress;
        });
      }, 3000);
      
    } catch (error) {
      setUploadProgress(prev => ({
        ...prev,
        [fileId]: { ...prev[fileId], status: 'error', error: error.message }
      }));
    }
  };

  const monitorTask = async (taskId, fileId) => {
    const checkStatus = async () => {
      try {
        const response = await tasksAPI.getStatus(taskId);
        const { state, progress, result, error } = response.data;

        setUploadProgress(prev => ({
          ...prev,
          [fileId]: { 
            ...prev[fileId], 
            progress: progress || 0,
            status: state === 'SUCCESS' ? 'completed' : state === 'FAILURE' ? 'error' : 'processing'
          }
        }));

        if (state === 'SUCCESS') {
          if (onUploadComplete) {
            onUploadComplete(result);
          }
          // Remove from progress after 3 seconds
          setTimeout(() => {
            setUploadProgress(prev => {
              const newProgress = { ...prev };
              delete newProgress[fileId];
              return newProgress;
            });
          }, 3000);
        } else if (state === 'FAILURE') {
          setUploadProgress(prev => ({
            ...prev,
            [fileId]: { ...prev[fileId], error: error }
          }));
        } else {
          // Continue monitoring
          setTimeout(checkStatus, 2000);
        }
      } catch (error) {
        setUploadProgress(prev => ({
          ...prev,
          [fileId]: { ...prev[fileId], status: 'error', error: error.message }
        }));
      }
    };

    checkStatus();
  };

  const handleUrlUpload = async () => {
    if (!urlInput.trim()) return;

    setUploading(true);
    const fileId = Date.now();
    
    setUploadProgress(prev => ({
      ...prev,
      [fileId]: { name: urlInput, status: 'uploading', progress: 0 }
    }));

    try {
      const response = await filesAPI.uploadUrl(urlInput);
      const { task_id } = response.data;
      
      monitorTask(task_id, fileId);
      setUrlInput('');
      
    } catch (error) {
      setUploadProgress(prev => ({
        ...prev,
        [fileId]: { ...prev[fileId], status: 'error', error: error.message }
      }));
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* File Drop Zone */}
      <div
        className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          dragActive 
            ? 'border-blue-500 bg-blue-50' 
            : 'border-gray-300 hover:border-gray-400'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          type="file"
          multiple
          accept=".pdf,.doc,.docx,.txt,.csv"
          onChange={(e) => handleFiles(e.target.files)}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        />
        
        <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">
          Upload Teaching Materials
        </h3>
        <p className="text-gray-600 mb-4">
          Drag and drop files here, or click to browse
        </p>
        <p className="text-sm text-gray-500">
          Supports PDF, DOC, DOCX, TXT, CSV files
        </p>
      </div>

      {/* URL Input */}
      <div className="flex space-x-2">
        <div className="flex-1">
          <input
            type="url"
            value={urlInput}
            onChange={(e) => setUrlInput(e.target.value)}
            placeholder="Or paste a URL to extract content from..."
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <button
          onClick={handleUrlUpload}
          disabled={!urlInput.trim() || uploading}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 flex items-center space-x-2"
        >
          <Link className="h-4 w-4" />
          <span>Extract</span>
        </button>
      </div>

      {/* Upload Progress */}
      {Object.keys(uploadProgress).length > 0 && (
        <div className="space-y-2">
          <h4 className="font-medium text-gray-900">Upload Progress</h4>
          {Object.entries(uploadProgress).map(([id, file]) => (
            <div key={id} className="bg-gray-50 rounded-lg p-3">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center space-x-2">
                  <File className="h-4 w-4 text-gray-500" />
                  <span className="text-sm font-medium text-gray-900 truncate">
                    {file.name}
                  </span>
                </div>
                <div className="flex items-center space-x-2">
                  {file.status === 'completed' && (
                    <CheckCircle className="h-4 w-4 text-green-500" />
                  )}
                  {file.status === 'error' && (
                    <AlertCircle className="h-4 w-4 text-red-500" />
                  )}
                  {file.status === 'processing' && (
                    <Loader className="h-4 w-4 text-blue-500 animate-spin" />
                  )}
                </div>
              </div>
              
              {file.status !== 'error' && (
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${file.progress}%` }}
                  />
                </div>
              )}
              
              {file.error && (
                <p className="text-sm text-red-600 mt-1">{file.error}</p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default FileUploader;