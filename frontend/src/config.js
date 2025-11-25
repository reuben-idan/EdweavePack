// Secure API configuration - enforce HTTPS in production
const IS_PRODUCTION = process.env.NODE_ENV === 'production';

// Hardcoded production URL - no localhost fallback
export const API_BASE_URL = 'https://edweavepack-alb-1353441079.eu-north-1.elb.amazonaws.com';
export const IS_PRODUCTION_ENV = IS_PRODUCTION;
export const ENABLE_LOGGING = !IS_PRODUCTION;

// Security headers for production
export const SECURITY_CONFIG = {
  enforceHTTPS: IS_PRODUCTION,
  strictTransportSecurity: IS_PRODUCTION,
  contentSecurityPolicy: IS_PRODUCTION
};