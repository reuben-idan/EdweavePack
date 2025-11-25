# AWS Secrets Manager configuration for secure credential management

# Database credentials secret
resource "aws_secretsmanager_secret" "database" {
  name                    = "edweavepack/database"
  description             = "Database credentials for EdweavePack"
  recovery_window_in_days = 7

  tags = {
    Name        = "${var.project_name}-db-secret"
    Environment = var.environment
  }
}

resource "aws_secretsmanager_secret_version" "database" {
  secret_id = aws_secretsmanager_secret.database.id
  secret_string = jsonencode({
    username = "postgres"
    password = var.db_password
    engine   = "postgres"
    host     = aws_db_instance.main.endpoint
    port     = 5432
    dbname   = "edweavepack"
    url      = "postgresql://postgres:${var.db_password}@${aws_db_instance.main.endpoint}/edweavepack"
  })
}

# JWT secret key
resource "aws_secretsmanager_secret" "jwt" {
  name                    = "edweavepack/jwt"
  description             = "JWT secret key for EdweavePack authentication"
  recovery_window_in_days = 7

  tags = {
    Name        = "${var.project_name}-jwt-secret"
    Environment = var.environment
  }
}

resource "aws_secretsmanager_secret_version" "jwt" {
  secret_id = aws_secretsmanager_secret.jwt.id
  secret_string = jsonencode({
    secret_key = var.jwt_secret_key
    algorithm  = "HS256"
  })
}

# Redis credentials secret
resource "aws_secretsmanager_secret" "redis" {
  name                    = "edweavepack/redis"
  description             = "Redis connection details for EdweavePack"
  recovery_window_in_days = 7

  tags = {
    Name        = "${var.project_name}-redis-secret"
    Environment = var.environment
  }
}

resource "aws_secretsmanager_secret_version" "redis" {
  secret_id = aws_secretsmanager_secret.redis.id
  secret_string = jsonencode({
    host = aws_elasticache_replication_group.main.primary_endpoint_address
    port = 6379
    url  = "redis://${aws_elasticache_replication_group.main.primary_endpoint_address}:6379"
  })
}

# IAM policy for ECS tasks to access secrets
resource "aws_iam_policy" "secrets_access" {
  name        = "${var.project_name}-secrets-access"
  description = "Policy for ECS tasks to access Secrets Manager"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ]
        Resource = [
          aws_secretsmanager_secret.database.arn,
          aws_secretsmanager_secret.jwt.arn,
          aws_secretsmanager_secret.redis.arn
        ]
      }
    ]
  })
}

# Attach secrets policy to ECS task role
resource "aws_iam_role_policy_attachment" "ecs_secrets_policy" {
  role       = aws_iam_role.ecs_task_role.name
  policy_arn = aws_iam_policy.secrets_access.arn
}

# S3 bucket for secure file storage
resource "aws_s3_bucket" "secure_storage" {
  bucket = "${var.project_name}-secure-storage-${random_id.bucket_suffix.hex}"

  tags = {
    Name        = "${var.project_name}-secure-storage"
    Environment = var.environment
  }
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# S3 bucket encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "secure_storage" {
  bucket = aws_s3_bucket.secure_storage.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
    bucket_key_enabled = true
  }
}

# S3 bucket public access block
resource "aws_s3_bucket_public_access_block" "secure_storage" {
  bucket = aws_s3_bucket.secure_storage.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# S3 bucket versioning
resource "aws_s3_bucket_versioning" "secure_storage" {
  bucket = aws_s3_bucket.secure_storage.id
  versioning_configuration {
    status = "Enabled"
  }
}

# IAM policy for S3 access
resource "aws_iam_policy" "s3_access" {
  name        = "${var.project_name}-s3-access"
  description = "Policy for ECS tasks to access S3 bucket"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.secure_storage.arn,
          "${aws_s3_bucket.secure_storage.arn}/*"
        ]
      }
    ]
  })
}

# Attach S3 policy to ECS task role
resource "aws_iam_role_policy_attachment" "ecs_s3_policy" {
  role       = aws_iam_role.ecs_task_role.name
  policy_arn = aws_iam_policy.s3_access.arn
}