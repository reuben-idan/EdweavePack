#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 EdweavePack Deployment Script${NC}"

# Check prerequisites
check_prerequisites() {
    echo -e "${YELLOW}Checking prerequisites...${NC}"
    
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker is not installed${NC}"
        exit 1
    fi
    
    if ! command -v aws &> /dev/null; then
        echo -e "${RED}❌ AWS CLI is not installed${NC}"
        exit 1
    fi
    
    if ! command -v terraform &> /dev/null; then
        echo -e "${RED}❌ Terraform is not installed${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ All prerequisites met${NC}"
}

# Deploy infrastructure
deploy_infrastructure() {
    echo -e "${YELLOW}Deploying infrastructure...${NC}"
    
    cd infrastructure
    
    if [ ! -f "terraform.tfvars" ]; then
        echo -e "${RED}❌ terraform.tfvars not found. Please create it with required variables.${NC}"
        exit 1
    fi
    
    terraform init
    terraform plan
    terraform apply -auto-approve
    
    cd ..
    
    echo -e "${GREEN}✅ Infrastructure deployed${NC}"
}

# Build and push images
build_and_push() {
    echo -e "${YELLOW}Building and pushing Docker images...${NC}"
    
    # Get ECR login
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $(aws sts get-caller-identity --query Account --output text).dkr.ecr.us-east-1.amazonaws.com
    
    # Build and push backend
    cd backend
    docker build -t edweavepack-backend .
    docker tag edweavepack-backend:latest $(aws sts get-caller-identity --query Account --output text).dkr.ecr.us-east-1.amazonaws.com/edweavepack-backend:latest
    docker push $(aws sts get-caller-identity --query Account --output text).dkr.ecr.us-east-1.amazonaws.com/edweavepack-backend:latest
    cd ..
    
    # Build and push frontend
    cd frontend
    docker build -t edweavepack-frontend .
    docker tag edweavepack-frontend:latest $(aws sts get-caller-identity --query Account --output text).dkr.ecr.us-east-1.amazonaws.com/edweavepack-frontend:latest
    docker push $(aws sts get-caller-identity --query Account --output text).dkr.ecr.us-east-1.amazonaws.com/edweavepack-frontend:latest
    cd ..
    
    echo -e "${GREEN}✅ Images built and pushed${NC}"
}

# Update ECS service
update_service() {
    echo -e "${YELLOW}Updating ECS service...${NC}"
    
    aws ecs update-service --cluster edweavepack-cluster --service edweavepack-service --force-new-deployment
    
    echo -e "${GREEN}✅ Service updated${NC}"
}

# Main deployment flow
main() {
    case "${1:-all}" in
        "infra")
            check_prerequisites
            deploy_infrastructure
            ;;
        "images")
            check_prerequisites
            build_and_push
            ;;
        "service")
            check_prerequisites
            update_service
            ;;
        "all")
            check_prerequisites
            deploy_infrastructure
            build_and_push
            update_service
            ;;
        *)
            echo "Usage: $0 [infra|images|service|all]"
            exit 1
            ;;
    esac
    
    echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
}

main "$@"