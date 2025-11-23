// Utility functions for student data management

export const setStudentName = (name) => {
  localStorage.setItem('studentName', name);
};

export const getStudentName = () => {
  return localStorage.getItem('studentName') || 
         new URLSearchParams(window.location.search).get('name') ||
         'Student';
};

export const clearStudentData = () => {
  localStorage.removeItem('studentName');
  localStorage.removeItem('studentToken');
};