import React from 'react';
import { useAuth } from '../hooks/useAuth';
import { User, Mail, Building, Shield } from 'lucide-react';

const UserProfile = ({ compact = false }) => {
  const { user } = useAuth();

  if (!user) return null;

  if (compact) {
    return (
      <div className="flex items-center space-x-2">
        <div className="w-8 h-8 bg-edu-primary rounded-full flex items-center justify-center">
          <User className="w-4 h-4 text-white" />
        </div>
        <div className="flex flex-col">
          <span className="text-sm font-medium text-visible">
            {user.name || user.full_name}
          </span>
          <span className="text-xs text-visible opacity-75">
            {user.role}
          </span>
        </div>
      </div>
    );
  }

  return (
    <div className="glass-card p-6">
      <div className="flex items-center space-x-4 mb-4">
        <div className="w-16 h-16 bg-edu-primary rounded-full flex items-center justify-center">
          <User className="w-8 h-8 text-white" />
        </div>
        <div>
          <h3 className="text-xl font-bold text-visible">
            {user.name || user.full_name}
          </h3>
          <p className="text-visible opacity-75 capitalize">
            {user.role || 'Teacher'}
          </p>
        </div>
      </div>
      
      <div className="space-y-3">
        <div className="flex items-center space-x-3">
          <Mail className="w-4 h-4 text-edu-primary" />
          <span className="text-visible">{user.email}</span>
        </div>
        
        {user.institution && (
          <div className="flex items-center space-x-3">
            <Building className="w-4 h-4 text-edu-primary" />
            <span className="text-visible">{user.institution}</span>
          </div>
        )}
        
        <div className="flex items-center space-x-3">
          <Shield className="w-4 h-4 text-edu-primary" />
          <span className="text-visible capitalize">{user.role || 'Teacher'} Account</span>
        </div>
      </div>
    </div>
  );
};

export default UserProfile;