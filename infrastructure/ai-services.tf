# AWS AI Services Infrastructure for EdweavePack

# IAM Role for AI Services
resource "aws_iam_role" "ai_services_role" {
  name = "edweavepack-ai-services-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = ["ecs-tasks.amazonaws.com", "lambda.amazonaws.com"]
        }
      }
    ]
  })
}

# IAM Policy for Bedrock Access
resource "aws_iam_policy" "bedrock_policy" {
  name = "edweavepack-bedrock-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream"
        ]
        Resource = [
          "arn:aws:bedrock:${var.aws_region}::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0",
          "arn:aws:bedrock:${var.aws_region}::foundation-model/amazon.titan-text-express-v1"
        ]
      }
    ]
  })
}

# IAM Policy for Textract Access
resource "aws_iam_policy" "textract_policy" {
  name = "edweavepack-textract-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "textract:DetectDocumentText",
          "textract:AnalyzeDocument"
        ]
        Resource = "*"
      }
    ]
  })
}

# IAM Policy for Comprehend Access
resource "aws_iam_policy" "comprehend_policy" {
  name = "edweavepack-comprehend-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "comprehend:DetectEntities",
          "comprehend:DetectKeyPhrases",
          "comprehend:DetectSentiment"
        ]
        Resource = "*"
      }
    ]
  })
}

# IAM Policy for Polly Access
resource "aws_iam_policy" "polly_policy" {
  name = "edweavepack-polly-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "polly:SynthesizeSpeech"
        ]
        Resource = "*"
      }
    ]
  })
}

# IAM Policy for Translate Access
resource "aws_iam_policy" "translate_policy" {
  name = "edweavepack-translate-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "translate:TranslateText"
        ]
        Resource = "*"
      }
    ]
  })
}

# Attach policies to role
resource "aws_iam_role_policy_attachment" "bedrock_attachment" {
  role       = aws_iam_role.ai_services_role.name
  policy_arn = aws_iam_policy.bedrock_policy.arn
}

resource "aws_iam_role_policy_attachment" "textract_attachment" {
  role       = aws_iam_role.ai_services_role.name
  policy_arn = aws_iam_policy.textract_policy.arn
}

resource "aws_iam_role_policy_attachment" "comprehend_attachment" {
  role       = aws_iam_role.ai_services_role.name
  policy_arn = aws_iam_policy.comprehend_policy.arn
}

resource "aws_iam_role_policy_attachment" "polly_attachment" {
  role       = aws_iam_role.ai_services_role.name
  policy_arn = aws_iam_policy.polly_policy.arn
}

resource "aws_iam_role_policy_attachment" "translate_attachment" {
  role       = aws_iam_role.ai_services_role.name
  policy_arn = aws_iam_policy.translate_policy.arn
}

# S3 Bucket for AI Content Storage
resource "aws_s3_bucket" "ai_content" {
  bucket = "edweavepack-ai-content-${random_string.bucket_suffix.result}"
}

resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
}

# Outputs
output "ai_services_role_arn" {
  value = aws_iam_role.ai_services_role.arn
}

output "ai_content_bucket" {
  value = aws_s3_bucket.ai_content.bucket
}

# Variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}