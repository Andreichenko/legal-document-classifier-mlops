# ECR Repository
output "ecr_repository_url" {
  description = "URL of the ECR repository"
  value       = aws_ecr_repository.legal_classifier.repository_url
}

output "ecr_repository_name" {
  description = "Name of the ECR repository"
  value       = aws_ecr_repository.legal_classifier.name
}

# ECS Cluster
output "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  value       = aws_ecs_cluster.legal_classifier.name
}

output "ecs_cluster_arn" {
  description = "ARN of the ECS cluster"
  value       = aws_ecs_cluster.legal_classifier.arn
}

# ECS Service
output "ecs_service_name" {
  description = "Name of the ECS service"
  value       = aws_ecs_service.legal_classifier.name
}

# Load Balancer
output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  value       = aws_lb.legal_classifier.dns_name
}

output "alb_url" {
  description = "URL of the Application Load Balancer"
  value       = "http://${aws_lb.legal_classifier.dns_name}"
}

# API Endpoints
output "api_health_url" {
  description = "Health check URL"
  value       = "http://${aws_lb.legal_classifier.dns_name}/health"
}

output "api_docs_url" {
  description = "API documentation URL"
  value       = "http://${aws_lb.legal_classifier.dns_name}/docs"
}

output "api_classify_url" {
  description = "Classification endpoint URL"
  value       = "http://${aws_lb.legal_classifier.dns_name}/classify"
}

# CloudWatch
output "cloudwatch_log_group" {
  description = "CloudWatch log group name"
  value       = aws_cloudwatch_log_group.legal_classifier.name
}

# VPC
output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "public_subnet_ids" {
  description = "Public subnet IDs"
  value       = module.vpc.public_subnet_ids
}

output "private_subnet_ids" {
  description = "Private subnet IDs"
  value       = module.vpc.private_subnet_ids
}

# Security Groups
output "alb_security_group_id" {
  description = "ALB security group ID"
  value       = aws_security_group.alb.id
}

output "ecs_security_group_id" {
  description = "ECS tasks security group ID"
  value       = aws_security_group.ecs_tasks.id
} 