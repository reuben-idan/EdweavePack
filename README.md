<div align="center">

<img src="frontend/public/images/Edweave Pack Logo.png" alt="EdweavePack Logo" width="120" height="120">

# EdweavePack

**AI-Powered Educational Content Platform**

[![Live Demo](https://img.shields.io/badge/Live_Demo-Available-brightgreen)](http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com)
[![AWS](https://img.shields.io/badge/AWS-Deployed-orange)](https://aws.amazon.com/)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)
[![Hackathon](https://img.shields.io/badge/AWS_Global_Vibe-2025-gold)](https://dorahacks.io/hackathon/aws-global-vibe)
[![Status](https://img.shields.io/badge/Status-Production-success)](http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com)
[![API](https://img.shields.io/badge/API-Operational-green)](http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com/docs)

**Transform teaching materials into intelligent curricula with Amazon Q Developer**

[Try Live Demo](http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com) • [API Documentation](http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com/docs)

</div>

## Features

**Amazon Q Integration** - AI-powered curriculum generation  
**Smart Content Processing** - Transform PDFs and videos into structured curricula  
**Automated Assessments** - Generate quizzes aligned with Bloom's taxonomy  
**Real-time Analytics** - Student progress tracking and insights  
**Agent Orchestration** - Kiro-powered adaptive learning paths  

## Quick Start

```bash
git clone https://github.com/reuben-idan/EdweavePack.git
cd EdweavePack
cp .env.example .env
make up
```

## Architecture

| Component | Technology |
|-----------|------------|
| AI Services | Amazon Bedrock, Comprehend, Textract |
| Backend | FastAPI, PostgreSQL, Redis |
| Frontend | React 18, Tailwind CSS |
| Infrastructure | AWS ECS, RDS, S3, ALB |
| DevOps | Docker, Terraform, ECR |

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/register` | User registration |
| `POST` | `/api/auth/token` | Authentication |
| `POST` | `/api/curriculum/` | Create AI curriculum |
| `POST` | `/api/files/simple-upload` | Upload materials |
| `GET` | `/api/analytics/dashboard` | Analytics data |

## AWS Global Vibe Hackathon 2025

**Track**: AI in Education  
**Technology**: Amazon Q Developer  
**Innovation**: AI-driven educational content transformation  

## Legal

**Copyright** © 2025 EdweavePack. All rights reserved.

**License**: MIT License - see [LICENSE](LICENSE) file for details.

**Disclaimer**: This software is provided "as is" without warranty of any kind. Use at your own risk.

**Privacy**: Personal data processing complies with applicable privacy laws. No data stored without explicit consent.

**Educational Compliance**: FERPA and COPPA compliant for educational institutions.

**Liability**: EdweavePack shall not be liable for any damages arising from the use of this software.

---

<div align="center">

**Professional Educational Technology Solution**

[Live Application](http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com) • [Technical Support](mailto:support@edweavepack.com)

</div>