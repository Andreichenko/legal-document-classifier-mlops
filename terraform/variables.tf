# Project Configuration
variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "legal-classifier"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

# AWS Configuration
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

# VPC Configuration
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["us-west-2a", "us-west-2b"]
}

# ECS Configuration
variable "task_cpu" {
  description = "CPU units for ECS task (1024 = 1 vCPU)"
  type        = number
  default     = 512
}

variable "task_memory" {
  description = "Memory for ECS task in MiB"
  type        = number
  default     = 1024
}

variable "service_desired_count" {
  description = "Desired number of ECS tasks"
  type        = number
  default     = 1
}

# Tags
variable "common_tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default = {
    Project     = "legal-classifier"
    Environment = "dev"
    ManagedBy   = "Terraform"
  }
} 