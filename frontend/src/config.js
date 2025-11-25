// Secure API configuration - enforce HTTPS in production
const IS_PRODUCTION = process.env.NODE_ENV === 'production';

// Dynamic API URL detection
const getApiBaseUrl = () => {
  if (typeof window === 'undefined') return 'http://localhost:8000';
  
  const hostname = window.location.hostname;
  const protocol = window.location.protocol;
  
  // Production AWS environment
  if (hostname.includes('amazonaws.com') || hostname.includes('elb.')) {
    return `${protocol}//${hostname}`;
  }
  
  // Local development
  return 'http://localhost:8000';
};

export const API_BASE_URL = getApiBaseUrl();
export const IS_PRODUCTION_ENV = IS_PRODUCTION;
export const ENABLE_LOGGING = !IS_PRODUCTION;

// Security headers for production
export const SECURITY_CONFIG = {
  enforceHTTPS: IS_PRODUCTION,
  strictTransportSecurity: IS_PRODUCTION,
  contentSecurityPolicy: IS_PRODUCTION
};