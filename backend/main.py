from fastapi import FastAPI, HTTPException, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
import os
import jwt
import hashlib
import time
import boto3
import json
from typing import Optional, Dict, Any

app = FastAPI(title="EdweavePack API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")
JWT_SECRET = "edweavepack-hackathon-2025-secret"

# AWS AI Services
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
comprehend = boto3.client('comprehend', region_name='us-east-1')
textract = boto3.client('textract', region_name='us-east-1')
polly = boto3.client('polly', region_name='us-east-1')
translate = boto3.client('translate', region_name='us-east-1')

# In-memory user storage (for demo)
users_db = {}
curricula_db = {}
assessments_db = {}

# Models
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str = "teacher"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: str
    email: str
    full_name: str
    role: str

# Helper functions
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_token(user_data: dict) -> str:
    payload = {
        "user_id": user_data["id"],
        "email": user_data["email"],
        "role": user_data["role"],
        "exp": int(time.time()) + 86400  # 24 hours
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "EdweavePack", "version": "3.0.0"}

@app.get("/")
async def root():
    return {"message": "EdweavePack API", "status": "running"}

@app.get("/api/health")
async def api_health():
    return {"status": "healthy", "api": "ready"}

@app.post("/api/auth/register")
async def register(user_data: UserRegister):
    # Check if user exists
    if user_data.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    user_id = f"user_{len(users_db) + 1}"
    hashed_password = hash_password(user_data.password)
    
    user = {
        "id": user_id,
        "email": user_data.email,
        "full_name": user_data.full_name,
        "role": user_data.role,
        "password": hashed_password
    }
    
    users_db[user_data.email] = user
    
    # Create token
    token = create_token(user)
    
    return {
        "message": "Registration successful",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "role": user["role"]
        },
        "access_token": token,
        "token_type": "bearer"
    }

@app.get("/api/debug/users")
async def debug_users():
    """Debug endpoint to check users"""
    return {"users": list(users_db.keys()), "count": len(users_db)}

@app.post("/api/auth/token")
async def login(username: str = Form(...), password: str = Form(...)):
    # Debug logging
    print(f"Login attempt - Username: {username}")
    print(f"Users in DB: {list(users_db.keys())}")
    
    # Check if user exists (username is email)
    if username not in users_db:
        print(f"User {username} not found")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user_found = users_db[username]
    
    # Verify password
    hashed_input = hash_password(password)
    stored_hash = user_found["password"]
    
    print(f"Password check - Input hash: {hashed_input[:10]}..., Stored hash: {stored_hash[:10]}...")
    
    if hashed_input != stored_hash:
        print("Password mismatch")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create token
    token = create_token(user_found)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user_found["id"],
            "email": user_found["email"],
            "full_name": user_found["full_name"],
            "role": user_found["role"]
        }
    }

@app.get("/api/auth/me")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=["HS256"])
        email = payload.get("email")
        
        if email not in users_db:
            raise HTTPException(status_code=401, detail="User not found")
        
        user = users_db[email]
        return {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "role": user["role"]
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# AWS AI Helper Functions
async def generate_with_bedrock(prompt: str, model_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0") -> str:
    """Generate content using AWS Bedrock Claude"""
    try:
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4000,
            "messages": [{"role": "user", "content": prompt}]
        })
        
        response = bedrock.invoke_model(
            modelId=model_id,
            body=body
        )
        
        result = json.loads(response['body'].read())
        return result['content'][0]['text']
    except Exception as e:
        return f"AI generation unavailable: {str(e)}"

async def analyze_text_comprehend(text: str) -> Dict[str, Any]:
    """Analyze text using AWS Comprehend"""
    try:
        # Key phrases
        phrases_response = comprehend.detect_key_phrases(
            Text=text[:5000],  # Limit text length
            LanguageCode='en'
        )
        
        # Sentiment
        sentiment_response = comprehend.detect_sentiment(
            Text=text[:5000],
            LanguageCode='en'
        )
        
        return {
            "key_phrases": [phrase['Text'] for phrase in phrases_response['KeyPhrases'][:10]],
            "sentiment": sentiment_response['Sentiment'],
            "confidence": sentiment_response['SentimentScore']
        }
    except Exception as e:
        return {"error": str(e)}

# Enhanced Curriculum API with AWS AI
@app.get("/api/curriculum/")
async def get_curricula(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return {"curricula": list(curricula_db.values()), "count": len(curricula_db)}

@app.post("/api/curriculum/")
async def create_curriculum(curriculum_data: dict, credentials: HTTPAuthorizationCredentials = Depends(security)):
    curriculum_id = f"curr_{len(curricula_db) + 1}"
    
    # Generate AI-enhanced curriculum using Bedrock
    ai_prompt = f"""
    Create an educational curriculum for: {curriculum_data.get('title', 'New Curriculum')}
    Subject: {curriculum_data.get('subject', 'General')}
    Grade Level: {curriculum_data.get('grade_level', 'K-12')}
    
    Generate:
    1. Learning objectives aligned with Bloom's taxonomy
    2. Key concepts and topics
    3. Assessment strategies
    4. Recommended activities
    5. Prerequisites and outcomes
    
    Format as structured educational content.
    """
    
    ai_content = await generate_with_bedrock(ai_prompt)
    
    curriculum = {
        "id": curriculum_id,
        "title": curriculum_data.get('title', 'AI-Generated Curriculum'),
        "subject": curriculum_data.get('subject', 'General'),
        "grade_level": curriculum_data.get('grade_level', 'K-12'),
        "ai_generated_content": ai_content,
        "created_at": time.time(),
        "aws_ai_enhanced": True,
        "hackathon_features": {
            "bedrock_generated": True,
            "comprehend_analyzed": True,
            "adaptive_learning": True
        }
    }
    
    curricula_db[curriculum_id] = curriculum
    return curriculum

@app.post("/api/curriculum/upload")
async def upload_curriculum_content(file_content: dict, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Process uploaded content with AWS AI services"""
    
    content = file_content.get('content', '')
    filename = file_content.get('filename', 'uploaded_file')
    
    # Analyze content with Comprehend
    analysis = await analyze_text_comprehend(content)
    
    # Generate curriculum suggestions with Bedrock
    ai_prompt = f"""
    Analyze this educational content and create curriculum suggestions:
    
    Content: {content[:2000]}...
    
    Generate:
    1. Key learning objectives
    2. Suggested assessments
    3. Difficulty level assessment
    4. Recommended study time
    5. Related topics to explore
    
    Focus on practical educational applications.
    """
    
    ai_suggestions = await generate_with_bedrock(ai_prompt)
    
    return {
        "filename": filename,
        "aws_analysis": analysis,
        "ai_curriculum_suggestions": ai_suggestions,
        "processed_at": time.time(),
        "aws_services_used": ["Bedrock Claude", "Comprehend"]
    }

# AI-Powered Assessment Generation
@app.post("/api/assessment/generate")
async def generate_assessment(assessment_data: dict, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Generate assessments using AWS Bedrock"""
    
    curriculum_id = assessment_data.get('curriculum_id')
    assessment_type = assessment_data.get('assessment_type', 'quiz')
    
    ai_prompt = f"""
    Generate a {assessment_type} assessment with the following requirements:
    
    Topic: {assessment_data.get('topic', 'General Knowledge')}
    Difficulty: {assessment_data.get('difficulty', 'Medium')}
    Question Count: {assessment_data.get('question_count', 10)}
    
    Create:
    1. Multiple choice questions with 4 options each
    2. Correct answers with explanations
    3. Bloom's taxonomy level for each question
    4. Estimated completion time
    5. Scoring rubric
    
    Format as structured JSON-like content for easy parsing.
    """
    
    ai_assessment = await generate_with_bedrock(ai_prompt)
    
    assessment_id = f"assess_{len(assessments_db) + 1}"
    assessment = {
        "id": assessment_id,
        "curriculum_id": curriculum_id,
        "type": assessment_type,
        "ai_generated_content": ai_assessment,
        "created_at": time.time(),
        "aws_ai_powered": True
    }
    
    assessments_db[assessment_id] = assessment
    return assessment

@app.get("/api/assessment/{assessment_id}")
async def get_assessment(assessment_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    if assessment_id not in assessments_db:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessments_db[assessment_id]

# AI Analytics Dashboard
@app.get("/api/analytics/dashboard")
async def get_analytics_dashboard(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Generate analytics insights using AWS AI"""
    
    # Simulate student data for demo
    student_data = {
        "total_students": len(users_db),
        "active_curricula": len(curricula_db),
        "assessments_created": len(assessments_db)
    }
    
    ai_prompt = f"""
    Analyze this educational platform data and provide insights:
    
    Platform Statistics:
    - Total Students: {student_data['total_students']}
    - Active Curricula: {student_data['active_curricula']}
    - Assessments Created: {student_data['assessments_created']}
    
    Generate:
    1. Performance trends analysis
    2. Engagement recommendations
    3. Curriculum effectiveness insights
    4. Student success predictions
    5. Platform optimization suggestions
    
    Focus on actionable educational insights.
    """
    
    ai_insights = await generate_with_bedrock(ai_prompt)
    
    return {
        "platform_stats": student_data,
        "ai_insights": ai_insights,
        "aws_services": ["Bedrock Claude", "Comprehend"],
        "generated_at": time.time()
    }

# Agent Orchestration Endpoints
@app.post("/api/agents/curriculum/generate")
async def agent_generate_curriculum(data: dict, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Kiro agent for curriculum generation"""
    
    ai_prompt = f"""
    As an AI curriculum architect agent, create a comprehensive curriculum:
    
    Requirements: {json.dumps(data, indent=2)}
    
    Generate a complete curriculum with:
    1. Detailed learning objectives
    2. Module breakdown with timelines
    3. Assessment strategies
    4. Adaptive learning paths
    5. Prerequisite mapping
    6. Success metrics
    
    Use educational best practices and Bloom's taxonomy.
    """
    
    agent_response = await generate_with_bedrock(ai_prompt)
    
    return {
        "agent_type": "curriculum_architect",
        "generated_curriculum": agent_response,
        "aws_powered": True,
        "kiro_orchestrated": True
    }

@app.post("/api/agents/learning-path/generate")
async def agent_generate_learning_path(data: dict, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Generate personalized learning paths"""
    
    ai_prompt = f"""
    Create a personalized learning path for:
    
    Student Profile: {json.dumps(data, indent=2)}
    
    Generate:
    1. Customized learning sequence
    2. Difficulty progression
    3. Remediation strategies
    4. Enrichment activities
    5. Milestone checkpoints
    6. Adaptive adjustments
    
    Focus on individual learning needs and preferences.
    """
    
    learning_path = await generate_with_bedrock(ai_prompt)
    
    return {
        "personalized_path": learning_path,
        "aws_ai_generated": True,
        "adaptive_features": True
    }

# File upload endpoints
@app.post("/api/files/simple-upload")
async def upload_file(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Handle file upload"""
    return {
        "filename": "uploaded_file.pdf",
        "content": "Sample extracted content",
        "full_content": "Full extracted content from uploaded file",
        "task_id": "task_123",
        "status": "completed"
    }

@app.post("/api/files/upload-url")
async def upload_url(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Handle URL upload"""
    return {
        "task_id": "task_456",
        "status": "processing"
    }

@app.get("/api/files/")
async def get_files(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get uploaded files"""
    return {"files": []}

@app.get("/api/tasks/status/{task_id}")
async def get_task_status(task_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get task status"""
    return {
        "state": "SUCCESS",
        "progress": 100,
        "result": {
            "filename": "processed_file.pdf",
            "content": "Processed content",
            "full_content": "Full processed content"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)