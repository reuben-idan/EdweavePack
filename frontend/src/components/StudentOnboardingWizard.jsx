import React, { useState } from 'react';
import { ChevronRightIcon, ChevronLeftIcon } from '@heroicons/react/24/outline';
import { api } from '../services/api';

const StudentOnboardingWizard = ({ onComplete }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState({
    goals: { goals: '', score_targets: {}, skill_goals: [], exam_targets: [] },
    subjects: { subjects: [] },
    availability: { days_per_week: 5, hours_per_day: 2, preferred_times: [] },
    uploads: []
  });

  const steps = [
    { title: 'Study Goals', component: GoalsStep },
    { title: 'Focus Subjects', component: SubjectsStep },
    { title: 'Study Schedule', component: AvailabilityStep },
    { title: 'Study Materials', component: UploadsStep }
  ];

  const handleNext = async () => {
    if (currentStep < steps.length - 1) {
      await saveCurrentStep();
      setCurrentStep(currentStep + 1);
    } else {
      await completeOnboarding();
    }
  };

  const saveCurrentStep = async () => {
    const stepData = Object.keys(formData)[currentStep];
    const endpoint = ['goals', 'subjects', 'availability', 'uploads'][currentStep];
    await api.post(`/student/${endpoint}`, formData[stepData]);
  };

  const completeOnboarding = async () => {
    await api.post('/student/complete');
    onComplete();
  };

  const CurrentStepComponent = steps[currentStep].component;

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white/10 backdrop-blur-lg rounded-xl">
      <div className="mb-8">
        <div className="flex justify-between items-center mb-4">
          {steps.map((step, index) => (
            <div key={index} className={`flex items-center ${index < steps.length - 1 ? 'flex-1' : ''}`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium
                ${index <= currentStep ? 'bg-blue-500 text-white' : 'bg-gray-300 text-gray-600'}`}>
                {index + 1}
              </div>
              <span className="ml-2 text-sm font-medium">{step.title}</span>
              {index < steps.length - 1 && <div className="flex-1 h-px bg-gray-300 mx-4" />}
            </div>
          ))}
        </div>
      </div>

      <CurrentStepComponent formData={formData} setFormData={setFormData} />

      <div className="flex justify-between mt-8">
        <button
          onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
          disabled={currentStep === 0}
          className="flex items-center px-4 py-2 text-gray-600 disabled:opacity-50"
        >
          <ChevronLeftIcon className="w-4 h-4 mr-1" />
          Previous
        </button>
        <button
          onClick={handleNext}
          className="flex items-center px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
          {currentStep === steps.length - 1 ? 'Complete' : 'Next'}
          <ChevronRightIcon className="w-4 h-4 ml-1" />
        </button>
      </div>
    </div>
  );
};

const GoalsStep = ({ formData, setFormData }) => {
  const examples = [
    { type: 'score', label: 'Score 85% on Math SAT', value: 'math_sat_85' },
    { type: 'skill', label: 'Master Calculus', value: 'calculus_mastery' },
    { type: 'exam', label: 'Pass AP Biology', value: 'ap_biology' }
  ];

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">What do you want to achieve?</h2>
      
      <div>
        <label className="block text-sm font-medium mb-2">Describe your goals</label>
        <textarea
          value={formData.goals.goals}
          onChange={(e) => setFormData(prev => ({
            ...prev,
            goals: { ...prev.goals, goals: e.target.value }
          }))}
          className="w-full p-3 border rounded-lg"
          rows="3"
          placeholder="I want to improve my understanding of..."
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">Example Goals</label>
        <div className="grid grid-cols-1 gap-2">
          {examples.map((example, index) => (
            <button
              key={index}
              onClick={() => setFormData(prev => ({
                ...prev,
                goals: { ...prev.goals, goals: prev.goals.goals + (prev.goals.goals ? ', ' : '') + example.label }
              }))}
              className="p-3 text-left border rounded-lg hover:bg-gray-50"
            >
              {example.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

const SubjectsStep = ({ formData, setFormData }) => {
  const subjects = ['Mathematics', 'Science', 'English', 'History', 'Computer Science', 'Languages', 'Arts'];

  const toggleSubject = (subject) => {
    setFormData(prev => ({
      ...prev,
      subjects: {
        subjects: prev.subjects.subjects.includes(subject)
          ? prev.subjects.subjects.filter(s => s !== subject)
          : [...prev.subjects.subjects, subject]
      }
    }));
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Choose Focus Subjects</h2>
      <div className="grid grid-cols-2 gap-3">
        {subjects.map(subject => (
          <button
            key={subject}
            onClick={() => toggleSubject(subject)}
            className={`p-4 rounded-lg border-2 transition-colors ${
              formData.subjects.subjects.includes(subject)
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            {subject}
          </button>
        ))}
      </div>
    </div>
  );
};

const AvailabilityStep = ({ formData, setFormData }) => {
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Study Schedule</h2>
      
      <div>
        <label className="block text-sm font-medium mb-2">Days per week</label>
        <input
          type="range"
          min="1"
          max="7"
          value={formData.availability.days_per_week}
          onChange={(e) => setFormData(prev => ({
            ...prev,
            availability: { ...prev.availability, days_per_week: parseInt(e.target.value) }
          }))}
          className="w-full"
        />
        <div className="text-center mt-2">{formData.availability.days_per_week} days</div>
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">Hours per day</label>
        <input
          type="range"
          min="0.5"
          max="8"
          step="0.5"
          value={formData.availability.hours_per_day}
          onChange={(e) => setFormData(prev => ({
            ...prev,
            availability: { ...prev.availability, hours_per_day: parseFloat(e.target.value) }
          }))}
          className="w-full"
        />
        <div className="text-center mt-2">{formData.availability.hours_per_day} hours</div>
      </div>
    </div>
  );
};

const UploadsStep = ({ formData, setFormData }) => {
  const [uploadType, setUploadType] = useState('file');

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (file) {
      const formDataObj = new FormData();
      formDataObj.append('file', file);
      await api.post('/student/uploads', formDataObj);
    }
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Upload Study Materials (Optional)</h2>
      
      <div className="flex space-x-4 mb-4">
        {['file', 'url', 'text'].map(type => (
          <button
            key={type}
            onClick={() => setUploadType(type)}
            className={`px-4 py-2 rounded-lg ${
              uploadType === type ? 'bg-blue-500 text-white' : 'bg-gray-200'
            }`}
          >
            {type === 'file' ? 'PDF Upload' : type === 'url' ? 'URL Import' : 'Text Content'}
          </button>
        ))}
      </div>

      {uploadType === 'file' && (
        <input
          type="file"
          accept=".pdf,.doc,.docx"
          onChange={handleFileUpload}
          className="w-full p-3 border rounded-lg"
        />
      )}

      {uploadType === 'url' && (
        <input
          type="url"
          placeholder="https://example.com/study-material"
          className="w-full p-3 border rounded-lg"
        />
      )}

      {uploadType === 'text' && (
        <textarea
          placeholder="Paste your study content here..."
          rows="6"
          className="w-full p-3 border rounded-lg"
        />
      )}
    </div>
  );
};

export default StudentOnboardingWizard;