// Secure API configuration - enforce HTTPS in production
const IS_PRODUCTION = process.env.NODE_ENV === 'production';

// Updated production URL for enhanced AI deployment
export const API_BASE_URL = IS_PRODUCTION 
  ? 'https://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com'
  : 'http://localhost:8001';
export const IS_PRODUCTION_ENV = IS_PRODUCTION;
export const ENABLE_LOGGING = !IS_PRODUCTION;

// Hackathon-specific configuration
export const HACKATHON_CONFIG = {
  event: 'AWS Global Vibe: AI Coding Hackathon 2025',
  track: 'AI in Education',
  features: {
    amazonQDeveloper: true,
    agentOrchestration: true,
    adaptiveLearning: true,
    aiAssessments: true
  }
};

// Security headers for production
export const SECURITY_CONFIG = {
  enforceHTTPS: IS_PRODUCTION,
  strictTransportSecurity: IS_PRODUCTION,
  contentSecurityPolicy: IS_PRODUCTION
};