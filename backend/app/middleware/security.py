"""
Security middleware for FastAPI application
"""
import os
from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)

class SecurityMiddleware(BaseHTTPMiddleware):
    """Enhanced security middleware with HTTPS enforcement and security headers"""
    
    def __init__(self, app, enforce_https: bool = False):
        super().__init__(app)
        self.enforce_https = enforce_https
        
    async def dispatch(self, request: Request, call_next):
        # HTTPS enforcement in production
        if self.enforce_https and request.headers.get("x-forwarded-proto") != "https":
            if request.method == "GET":
                # Redirect GET requests to HTTPS
                https_url = str(request.url).replace("http://", "https://", 1)
                return RedirectResponse(url=https_url, status_code=301)
            else:
                # Block non-GET requests over HTTP
                raise HTTPException(
                    status_code=400,
                    detail="HTTPS required for this operation"
                )
        
        # Process request
        response = await call_next(request)
        
        # Add security headers
        security_headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Content-Security-Policy": (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self' https:; "
                "connect-src 'self' https:; "
                "frame-ancestors 'none';"
            )
        }
        
        # Add HSTS header for HTTPS
        if self.enforce_https:
            security_headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )
        
        # Apply headers
        for header, value in security_headers.items():
            response.headers[header] = value
            
        # Remove server information
        response.headers.pop("server", None)
        
        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple rate limiting middleware"""
    
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.request_counts = {}
        
    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host
        if "x-forwarded-for" in request.headers:
            client_ip = request.headers["x-forwarded-for"].split(",")[0].strip()
        
        # Simple rate limiting (in production, use Redis)
        import time
        current_time = int(time.time() / 60)  # Current minute
        
        if client_ip not in self.request_counts:
            self.request_counts[client_ip] = {}
            
        if current_time not in self.request_counts[client_ip]:
            self.request_counts[client_ip][current_time] = 0
            
        self.request_counts[client_ip][current_time] += 1
        
        # Clean old entries
        for minute in list(self.request_counts[client_ip].keys()):
            if minute < current_time - 1:
                del self.request_counts[client_ip][minute]
        
        # Check rate limit
        if self.request_counts[client_ip][current_time] > self.requests_per_minute:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again later."
            )
        
        return await call_next(request)

def get_security_middleware():
    """Factory function to create security middleware with environment-based config"""
    enforce_https = os.getenv("ENFORCE_HTTPS", "false").lower() == "true"
    return SecurityMiddleware, {"enforce_https": enforce_https}

def get_rate_limit_middleware():
    """Factory function to create rate limit middleware"""
    requests_per_minute = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    return RateLimitMiddleware, {"requests_per_minute": requests_per_minute}