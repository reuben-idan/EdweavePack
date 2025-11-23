# EdweavePack Architecture

## System Overview

```plantuml
@startuml EdweavePack Architecture
!theme aws-orange

package "Frontend Layer" {
  [React App] as Frontend
  [Tailwind CSS] as Styles
  [React Router] as Router
}

package "API Gateway" {
  [FastAPI] as API
  [JWT Auth] as Auth
  [CORS Middleware] as CORS
}

package "Agent Orchestration" {
  [Agent Orchestrator] as Orchestrator
  [Curriculum Architect] as CurriculumAgent
  [Assessment Generator] as AssessmentAgent
  [Personalized Learning] as LearningAgent
  [Auto-Grader] as GraderAgent
}

package "AI Services" {
  [Amazon Q Developer] as QDeveloper
  [Kiro Configuration] as Kiro
  [Bloom's Taxonomy] as Bloom
}

package "Data Layer" {
  database "PostgreSQL" as DB
  database "Redis Cache" as Cache
  cloud "AWS S3" as Storage
}

package "Task Processing" {
  [Celery Workers] as Workers
  [Flower Monitor] as Monitor
}

package "Infrastructure" {
  cloud "AWS ECS/Fargate" as ECS
  cloud "AWS RDS" as RDS
  cloud "AWS ElastiCache" as ElastiCache
  cloud "Application Load Balancer" as ALB
}

' Frontend connections
Frontend --> API : HTTP/REST
Styles --> Frontend
Router --> Frontend

' API connections
API --> Auth
API --> CORS
API --> Orchestrator

' Agent connections
Orchestrator --> CurriculumAgent
Orchestrator --> AssessmentAgent
Orchestrator --> LearningAgent
Orchestrator --> GraderAgent

' AI Service connections
CurriculumAgent --> QDeveloper
AssessmentAgent --> QDeveloper
LearningAgent --> QDeveloper
GraderAgent --> QDeveloper
Orchestrator --> Kiro
Kiro --> Bloom

' Data connections
API --> DB
API --> Cache
API --> Storage
Workers --> DB
Workers --> Cache

' Task processing
API --> Workers
Workers --> Monitor

' Infrastructure
ECS --> API
ECS --> Workers
RDS --> DB
ElastiCache --> Cache
ALB --> ECS

@enduml
```

## Agent Workflow

```plantuml
@startuml Agent Orchestration Flow
!theme aws-orange

actor Teacher
participant "Upload Interface" as Upload
participant "Agent Orchestrator" as Orchestrator
participant "Curriculum Architect" as Curriculum
participant "Assessment Generator" as Assessment
participant "Personalized Learning" as Learning
participant "Auto-Grader" as Grader
participant "Amazon Q Developer" as Q
participant "Kiro Config" as Kiro

Teacher -> Upload: Upload teaching content
Upload -> Orchestrator: Process content request

Orchestrator -> Kiro: Load pedagogical templates
Kiro -> Orchestrator: Return Bloom's taxonomy config

Orchestrator -> Curriculum: Generate curriculum structure
Curriculum -> Q: Request lesson plans
Q -> Curriculum: Return structured modules
Curriculum -> Orchestrator: Curriculum with objectives

Orchestrator -> Assessment: Generate assessments
Assessment -> Q: Request questions & rubrics
Q -> Assessment: Return comprehensive assessments
Assessment -> Orchestrator: Assessments with grading criteria

Orchestrator -> Learning: Create learning paths
Learning -> Q: Request personalized paths
Q -> Learning: Return adaptive sequences
Learning -> Orchestrator: Personalized learning paths

Orchestrator -> Teacher: Complete curriculum package

note right of Orchestrator
  All agents work together to create:
  - Pedagogically sound curricula
  - Comprehensive assessments
  - Personalized learning paths
  - Auto-grading capabilities
end note

@enduml
```

## Technology Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **PostgreSQL**: Primary database for structured data
- **Redis**: Caching and session management
- **Celery**: Asynchronous task processing
- **SQLAlchemy**: Database ORM
- **Alembic**: Database migrations

### Frontend
- **React 18**: Modern UI framework
- **Tailwind CSS**: Utility-first styling
- **React Router**: Client-side routing
- **Recharts**: Data visualization
- **Axios**: HTTP client

### AI & Agents
- **Amazon Q Developer**: Content generation
- **Kiro**: Pedagogical configuration
- **Agent Orchestrator**: Multi-agent coordination
- **Bloom's Taxonomy**: Educational framework

### Infrastructure
- **AWS ECS/Fargate**: Container orchestration
- **AWS RDS**: Managed PostgreSQL
- **AWS ElastiCache**: Managed Redis
- **AWS S3**: File storage
- **AWS ALB**: Load balancing
- **Docker**: Containerization

### Monitoring
- **CloudWatch**: Logging and metrics
- **OpenSearch**: Log analysis
- **Flower**: Celery monitoring
- **AWS X-Ray**: Distributed tracing

## Data Flow

1. **Content Upload**: Teachers upload PDFs, text, or video URLs
2. **Content Extraction**: AI extracts and analyzes educational content
3. **Agent Orchestration**: Four specialized agents process content
4. **Curriculum Generation**: Structured learning modules created
5. **Assessment Creation**: Comprehensive evaluations generated
6. **Personalization**: Adaptive paths for individual students
7. **Delivery**: Content delivered through responsive web interface
8. **Analytics**: Real-time tracking and insights

## Security Architecture

- **Authentication**: OAuth2 + JWT tokens
- **Authorization**: Role-based access control
- **Transport**: HTTPS/TLS encryption
- **Data**: Encryption at rest (RDS, S3)
- **Network**: VPC with private subnets
- **Secrets**: AWS Secrets Manager
- **Monitoring**: CloudTrail audit logs

## Scalability Design

- **Horizontal Scaling**: ECS auto-scaling groups
- **Database**: Read replicas for performance
- **Caching**: Multi-layer Redis caching
- **CDN**: CloudFront for static assets
- **Load Balancing**: Application Load Balancer
- **Async Processing**: Celery task queues