variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-north-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "edweavepack"
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

variable "jwt_secret_key" {
  description = "JWT secret key for authentication"
  type        = string
  sensitive   = true
  default     = ""
}

variable "enable_waf" {
  description = "Enable AWS WAF protection"
  type        = bool
  default     = true
}

variable "enable_secrets_manager" {
  description = "Use AWS Secrets Manager for credentials"
  type        = bool
  default     = true
}

variable "ssl_policy" {
  description = "SSL policy for ALB"
  type        = string
  default     = "ELBSecurityPolicy-TLS13-1-2-2021-06"
}

variable "enable_encryption" {
  description = "Enable encryption at rest"
  type        = bool
  default     = true
}