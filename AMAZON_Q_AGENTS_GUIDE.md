# Amazon Q Agent Templates - EdweavePack

This guide covers the 3 Amazon Q agent templates that automate AI pipelines and integrate with backend APIs & S3.

## 🤖 Agent Overview

### 1. Ingest Agent
**Purpose**: Process uploaded content from S3 and extract structured data
- **Input**: S3 object key (PDF, text, video link)
- **Output**: `resource_id` in DB and S3 path for processed content

### 2. Curriculum Architect Agent  
**Purpose**: Generate curricula from processed resources using chain-of-thought prompts
- **Input**: `resource_id` from Ingest Agent
- **Output**: curriculum id, module ids, estimated learning time

### 3. Assessment Generator Agent
**Purpose**: Create assessments with multiple question types and validation
- **Input**: curriculum id, module id, difficulty level
- **Output**: assessment id(s) and scoring rubric

## 📁 Created Files

### Agent Implementation
- `backend/agents/ingest_agent.py` - S3 content processing with OCR
- `backend/agents/curriculum_architect_agent.py` - Curriculum generation
- `backend/agents/assessment_generator_agent.py` - Assessment creation
- `backend/agents/agent_orchestrator_q.py` - Pipeline orchestration
- `backend/agents/agent_config.py` - Cost controls and dry-run mode

### Security & Configuration
- `iam-policies/agent-policies.json` - Role-limited IAM policies
- `test-agents-simple.py` - Comprehensive test suite

## 🔄 Agent Workflows

### Ingest Agent Workflow
```
S3 Object → Download → Extract Text (Textract/OCR) → Chunk Content → Upload to Backend
```

**Key Features**:
- Amazon Textract integration for PDF OCR
- Intelligent content chunking with metadata
- AI-powered chunk analysis
- Backend API integration via `/api/curriculum/upload`

### Curriculum Architect Workflow
```
Resource ID → Fetch Content → Chain-of-Thought Generation → Create Modules → Backend API
```

**Key Features**:
- Chain-of-thought prompting for curriculum design
- Bloom's taxonomy alignment
- Module structure with learning objectives
- Time estimation and difficulty assessment

### Assessment Generator Workflow
```
Curriculum/Module → Generate Questions → Validate Answers → Create Rubric → Backend API
```

**Key Features**:
- Multiple question types (MC, short answer, coding)
- Model-based answer validation
- Automated scoring rubric generation
- Bloom's taxonomy alignment

## 🔐 Security & Cost Controls

### IAM Policies
Each agent has role-limited permissions:

**Ingest Agent**:
- S3 read access to `edweavepack-content/*`
- Textract document analysis
- CloudWatch logging

**Curriculum Architect**:
- Bedrock model access (Claude, Titan)
- CloudWatch logging

**Assessment Generator**:
- Bedrock model access (Claude, Titan)
- CloudWatch logging

### Cost Limits
```python
COST_LIMITS = {
    "ingest_agent": {
        "max_textract_pages": 50,
        "max_s3_downloads_mb": 100,
        "max_runtime_minutes": 10
    },
    "curriculum_architect": {
        "max_ai_tokens": 10000,
        "max_modules": 10,
        "max_runtime_minutes": 15
    },
    "assessment_generator": {
        "max_ai_tokens": 8000,
        "max_questions": 20,
        "max_runtime_minutes": 12
    }
}
```

### Dry-Run Mode
Set `AGENT_DRY_RUN=true` to simulate agent execution without actual processing.

## 🧪 Test Results

### Test Case: Small PDF (1 page)
**Input**: `sample-materials/python-basics.pdf`

**Expected Results**:
```json
{
  "ingest": {
    "success": true,
    "resource_id": "resource_sample-materials/python-basics_pdf",
    "chunks_created": 3,
    "total_characters": 2500
  },
  "curriculum": {
    "success": true,
    "curriculum_id": "curriculum_resource_sample-materials/python-basics_pdf",
    "modules_created": 3,
    "estimated_learning_time": 16
  },
  "assessments": [
    {
      "success": true,
      "assessment_id": "assessment_curriculum_..._module_0",
      "questions_generated": 10,
      "scoring_rubric": {
        "total_points": 50,
        "passing_score": 35
      }
    }
  ]
}
```

### Database Validation
```sql
SELECT COUNT(*) FROM users;      -- Expected: > 0
SELECT COUNT(*) FROM curricula;  -- Expected: > 0  
SELECT COUNT(*) FROM assessments; -- Expected: > 0
```

## 🚀 Usage Examples

### 1. Complete Pipeline
```python
from agents.agent_orchestrator_q import AmazonQAgentOrchestrator

orchestrator = AmazonQAgentOrchestrator()

result = await orchestrator.process_complete_pipeline(
    s3_key="materials/lesson.pdf",
    teacher_id=1,
    generation_schema={
        "difficulty": "intermediate",
        "duration_weeks": 4,
        "learning_objectives": ["Understand concepts", "Apply knowledge"]
    }
)
```

### 2. Individual Agent Usage
```python
# Ingest Agent
from agents.ingest_agent import IngestAgent

ingest_agent = IngestAgent()
result = await ingest_agent.process_s3_object("lesson.pdf", teacher_id=1)

# Curriculum Agent
from agents.curriculum_architect_agent import CurriculumArchitectAgent

curriculum_agent = CurriculumArchitectAgent()
result = await curriculum_agent.generate_curriculum_from_resource(
    resource_id="resource_123",
    generation_schema={"difficulty": "intermediate"}
)

# Assessment Agent
from agents.assessment_generator_agent import AssessmentGeneratorAgent

assessment_agent = AssessmentGeneratorAgent()
result = await assessment_agent.generate_assessment(
    curriculum_id="curriculum_456",
    module_id="module_1", 
    difficulty="intermediate"
)
```

### 3. API Integration
```bash
# Run complete pipeline
curl -X POST "http://localhost:8000/api/agents/pipeline" \
  -H "Content-Type: application/json" \
  -d '{
    "s3_key": "materials/lesson.pdf",
    "teacher_id": 1,
    "generation_schema": {
      "difficulty": "intermediate",
      "duration_weeks": 4
    }
  }'

# Batch processing
curl -X POST "http://localhost:8000/api/agents/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "s3_keys": ["lesson1.pdf", "lesson2.pdf"],
    "teacher_id": 1,
    "generation_schema": {"difficulty": "intermediate"}
  }'
```

## 🔧 Configuration

### Environment Variables
```env
# Agent Configuration
AGENT_DRY_RUN=false
AWS_REGION=us-east-1
S3_BUCKET_NAME=edweavepack-content

# Backend API
BACKEND_API_URL=http://localhost:8000

# Cost Controls
MAX_TEXTRACT_PAGES=50
MAX_AI_TOKENS=10000
```

### Backend API Endpoints
- `POST /api/curriculum/upload` - Ingest agent uploads
- `POST /api/curriculum/` - Curriculum creation
- `POST /api/assessment/{curriculum_id}` - Assessment creation
- `GET /api/curriculum/resource/{resource_id}` - Resource data

## 📊 Monitoring & Logs

### CloudWatch Log Groups
- `/aws/lambda/edweavepack-ingest-agent`
- `/aws/lambda/edweavepack-curriculum-agent`
- `/aws/lambda/edweavepack-assessment-agent`

### Key Metrics
- Processing time per agent
- Token usage for AI calls
- Success/failure rates
- Cost per pipeline run

## 🚨 Error Handling

### Common Issues
1. **S3 Access Denied**: Check IAM permissions for bucket access
2. **Textract Limits**: Reduce page count or implement pagination
3. **AI Token Limits**: Optimize prompts or increase limits
4. **Backend API Errors**: Verify endpoint availability and authentication

### Retry Logic
All agents implement exponential backoff for:
- S3 download failures
- Textract processing errors
- AI service timeouts
- Backend API failures

## 🎯 Performance Optimization

### Best Practices
1. **Batch Processing**: Use batch endpoints for multiple files
2. **Caching**: Cache AI responses for similar content
3. **Parallel Processing**: Run assessments for multiple modules concurrently
4. **Content Chunking**: Optimize chunk sizes for better AI processing

### Scaling Considerations
- Use SQS for asynchronous processing
- Implement Lambda concurrency limits
- Monitor and adjust cost limits based on usage
- Consider using Step Functions for complex workflows

## ✅ Validation Checklist

- [x] Ingest Agent processes S3 objects successfully
- [x] Curriculum Agent generates structured curricula
- [x] Assessment Agent creates validated questions
- [x] IAM policies restrict access appropriately
- [x] Cost limits prevent runaway usage
- [x] Dry-run mode works for testing
- [x] Database entries are created correctly
- [x] API integration functions properly

The Amazon Q agent templates are now ready for production deployment and can automatically process educational content from upload to assessment generation.