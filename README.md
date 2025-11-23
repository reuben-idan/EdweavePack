# EdweavePack

EdweavePack turns any teaching resource into structured curricula, adaptive learning paths, auto-graded assessments, and teacher analytics—powered by Amazon Q Developer and Amazon Kiro.

## 🚀 Features

- **AI-Powered Curriculum Generation**: Transform any teaching material (PDF, text, video transcripts) into structured curricula
- **Adaptive Learning Paths**: Personalized learning sequences based on student performance
- **Auto-Graded Assessments**: Intelligent question generation with automated grading
- **Teacher Analytics**: Comprehensive dashboard with student progress insights
- **Secure Authentication**: OAuth2-based teacher authentication system
- **Scalable Architecture**: Built for K-12 and University scale deployment

## 🏗️ Architecture

### Backend
- **FastAPI** (Python 3.11+) - High-performance API framework
- **PostgreSQL** - Primary database for structured data
- **Redis** - Caching and session management
- **Celery** - Asynchronous task processing
- **Amazon Q Developer** - AI content generation
- **Amazon Kiro** - Curriculum steering and orchestration

### Frontend
- **React 18** - Modern UI framework
- **Tailwind CSS** - Utility-first styling
- **React Router** - Client-side routing
- **Axios** - API communication

### Infrastructure
- **AWS ECS/Fargate** - Container orchestration
- **AWS RDS** - Managed PostgreSQL
- **AWS ElastiCache** - Managed Redis
- **AWS S3** - File storage
- **AWS CloudWatch** - Monitoring and logging
- **Terraform** - Infrastructure as Code

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)
- AWS CLI configured (for deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd EdweavePack
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start the development environment**
   ```bash
   make up
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Demo Mode

To run the demo with sample data:

```bash
make demo
```

This will start all services and populate the database with sample curricula and assessments.

## 📚 API Documentation

The API is fully documented with OpenAPI/Swagger. Once the backend is running, visit:
- Interactive docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Key Endpoints

- `POST /api/auth/register` - Teacher registration
- `POST /api/auth/token` - Authentication
- `POST /api/curriculum/` - Create new curriculum
- `GET /api/curriculum/` - List user's curricula
- `POST /api/curriculum/upload` - Upload teaching materials
- `GET /api/assessment/{id}` - Get assessment details
- `POST /api/assessment/{id}/submit` - Submit assessment answers
- `GET /api/analytics/dashboard` - Teacher dashboard analytics

## 🧪 Testing

### Backend Tests
```bash
make test-backend
```

### Frontend Tests
```bash
make test-frontend
```

### All Tests
```bash
make test
```

## 🚀 Deployment

### Infrastructure Setup

1. **Configure AWS credentials**
   ```bash
   aws configure
   ```

2. **Deploy infrastructure**
   ```bash
   cd infrastructure
   terraform init
   terraform plan
   terraform apply
   ```

### Application Deployment

The application uses GitHub Actions for CI/CD. Push to the `main` branch triggers:
1. Automated testing
2. Docker image building
3. ECR image pushing
4. ECS service updates

## 🔧 Development

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install
npm start
```

### Database Migrations

```bash
cd backend
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

## 📊 Monitoring

- **Application Logs**: CloudWatch Logs
- **Metrics**: CloudWatch Metrics
- **Performance**: AWS X-Ray tracing
- **Errors**: CloudWatch Alarms

## 🔒 Security

- OAuth2 with JWT tokens for authentication
- HTTPS enforcement in production
- Database encryption at rest
- Secrets management with AWS Secrets Manager
- CORS protection
- Input validation and sanitization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the [documentation](docs/)
- Review the [demo script](demo/demo-script.md)

## 🎯 Roadmap

- [ ] Multi-language support
- [ ] Advanced analytics with ML insights
- [ ] Integration with popular LMS platforms
- [ ] Mobile app for students
- [ ] Real-time collaboration features
- [ ] Advanced AI tutoring capabilities

---

**Built with ❤️ for educators worldwide**