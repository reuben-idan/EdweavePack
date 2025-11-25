# Enhanced SSL/TLS configuration with security best practices

# Route53 hosted zone for domain management
resource "aws_route53_zone" "main" {
  name = "edweavepack.com"
  
  tags = {
    Name        = "${var.project_name}-zone"
    Environment = var.environment
  }
}

# ACM certificate with DNS validation
resource "aws_acm_certificate" "main" {
  domain_name               = "edweavepack.com"
  subject_alternative_names = ["*.edweavepack.com"]
  validation_method         = "DNS"
  
  lifecycle {
    create_before_destroy = true
  }
  
  tags = {
    Name        = "${var.project_name}-cert"
    Environment = var.environment
  }
}

# DNS validation records
resource "aws_route53_record" "cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.main.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }
  
  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = aws_route53_zone.main.zone_id
}

# Certificate validation
resource "aws_acm_certificate_validation" "main" {
  certificate_arn         = aws_acm_certificate.main.arn
  validation_record_fqdns = [for record in aws_route53_record.cert_validation : record.fqdn]
  
  timeouts {
    create = "5m"
  }
}

# Fallback self-signed certificate for ALB DNS name
resource "tls_private_key" "fallback" {
  algorithm = "RSA"
  rsa_bits  = 4096  # Enhanced security
}

resource "tls_self_signed_cert" "fallback" {
  private_key_pem = tls_private_key.fallback.private_key_pem

  subject {
    common_name  = "*.eu-north-1.elb.amazonaws.com"
    organization = "EdweavePack"
    country      = "SE"
    locality     = "Stockholm"
  }

  validity_period_hours = 8760 # 1 year
  early_renewal_hours   = 720  # Renew 30 days before expiry

  allowed_uses = [
    "key_encipherment",
    "digital_signature",
    "server_auth",
  ]
  
  dns_names = [
    "*.eu-north-1.elb.amazonaws.com",
    "edweavepack-alb-1353441079.eu-north-1.elb.amazonaws.com"
  ]
}

resource "aws_acm_certificate" "fallback" {
  private_key      = tls_private_key.fallback.private_key_pem
  certificate_body = tls_self_signed_cert.fallback.cert_pem
  
  tags = {
    Name        = "${var.project_name}-fallback-cert"
    Environment = var.environment
  }
}

# A record for main domain
resource "aws_route53_record" "main" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "edweavepack.com"
  type    = "A"
  
  alias {
    name                   = aws_lb.main.dns_name
    zone_id                = aws_lb.main.zone_id
    evaluate_target_health = true
  }
}

# CNAME record for www subdomain
resource "aws_route53_record" "www" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "www.edweavepack.com"
  type    = "A"
  
  alias {
    name                   = aws_lb.main.dns_name
    zone_id                = aws_lb.main.zone_id
    evaluate_target_health = true
  }
}

# Note: SSL policy is configured directly in ALB listener