# Configure AWS Provider
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  # Backend configuration (optional for sandbox)
  # backend "s3" {
  #   bucket = "legal-classifier-terraform-state"
  #   key    = "terraform.tfstate"
  #   region = "us-west-2"
  # }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}

# VPC and Networking
module "vpc" {
  source = "./modules/vpc"
  
  project_name = var.project_name
  environment  = var.environment
  vpc_cidr     = var.vpc_cidr
  azs          = var.availability_zones
}

# ECR Repository
resource "aws_ecr_repository" "legal_classifier" {
  name                 = "${var.project_name}-${var.environment}"
  image_tag_mutability = "MUTABLE"
  
  image_scanning_configuration {
    scan_on_push = true
  }
  
  tags = {
    Name = "${var.project_name}-ecr"
  }
}

# ECR Lifecycle Policy
resource "aws_ecr_lifecycle_policy" "legal_classifier" {
  repository = aws_ecr_repository.legal_classifier.name
  
  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 5 images"
        selection = {
          tagStatus     = "tagged"
          tagPrefixList = ["v"]
          countType     = "imageCountMoreThan"
          countNumber   = 5
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}

# ECS Cluster
resource "aws_ecs_cluster" "legal_classifier" {
  name = "${var.project_name}-${var.environment}"
  
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
  
  tags = {
    Name = "${var.project_name}-cluster"
  }
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "legal_classifier" {
  name              = "/ecs/${var.project_name}-${var.environment}"
  retention_in_days = 7
  
  tags = {
    Name = "${var.project_name}-logs"
  }
}

# IAM Roles
resource "aws_iam_role" "ecs_execution_role" {
  name = "${var.project_name}-ecs-execution-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_execution_role_policy" {
  role       = aws_iam_role.ecs_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role" "ecs_task_role" {
  name = "${var.project_name}-ecs-task-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

# ECS Task Definition
resource "aws_ecs_task_definition" "legal_classifier" {
  family                   = "${var.project_name}-${var.environment}"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.task_cpu
  memory                   = var.task_memory
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn
  
  container_definitions = jsonencode([
    {
      name  = "${var.project_name}-container"
      image = "${aws_ecr_repository.legal_classifier.repository_url}:latest"
      
      portMappings = [
        {
          containerPort = 8000
          protocol      = "tcp"
        }
      ]
      
      environment = [
        {
          name  = "LOG_LEVEL"
          value = "INFO"
        },
        {
          name  = "AWS_REGION"
          value = var.aws_region
        }
      ]
      
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.legal_classifier.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
      
      healthCheck = {
        command     = ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"]
        interval    = 30
        timeout     = 5
        retries     = 3
        startPeriod = 60
      }
      
      essential = true
    }
  ])
  
  tags = {
    Name = "${var.project_name}-task-definition"
  }
}

# ECS Service
resource "aws_ecs_service" "legal_classifier" {
  name            = "${var.project_name}-${var.environment}"
  cluster         = aws_ecs_cluster.legal_classifier.id
  task_definition = aws_ecs_task_definition.legal_classifier.arn
  desired_count   = var.service_desired_count
  launch_type     = "FARGATE"
  
  network_configuration {
    subnets          = module.vpc.private_subnet_ids
    security_groups  = [aws_security_group.ecs_tasks.id]
    assign_public_ip = false
  }
  
  load_balancer {
    target_group_arn = aws_lb_target_group.legal_classifier.arn
    container_name   = "${var.project_name}-container"
    container_port   = 8000
  }
  
  depends_on = [aws_lb_listener.legal_classifier]
  
  tags = {
    Name = "${var.project_name}-service"
  }
}

# Application Load Balancer
resource "aws_lb" "legal_classifier" {
  name               = "${var.project_name}-${var.environment}"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = module.vpc.public_subnet_ids
  
  enable_deletion_protection = false
  
  tags = {
    Name = "${var.project_name}-alb"
  }
}

# ALB Target Group
resource "aws_lb_target_group" "legal_classifier" {
  name        = "${var.project_name}-${var.environment}"
  port        = 8000
  protocol    = "HTTP"
  vpc_id      = module.vpc.vpc_id
  target_type = "ip"
  
  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/health"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 3
  }
  
  tags = {
    Name = "${var.project_name}-target-group"
  }
}

# ALB Listener
resource "aws_lb_listener" "legal_classifier" {
  load_balancer_arn = aws_lb.legal_classifier.arn
  port              = "80"
  protocol          = "HTTP"
  
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.legal_classifier.arn
  }
}

# Security Groups
resource "aws_security_group" "alb" {
  name        = "${var.project_name}-alb-sg"
  description = "Security group for ALB"
  vpc_id      = module.vpc.vpc_id
  
  ingress {
    description = "HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "${var.project_name}-alb-sg"
  }
}

resource "aws_security_group" "ecs_tasks" {
  name        = "${var.project_name}-ecs-tasks-sg"
  description = "Security group for ECS tasks"
  vpc_id      = module.vpc.vpc_id
  
  ingress {
    description     = "HTTP from ALB"
    from_port       = 8000
    to_port         = 8000
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "${var.project_name}-ecs-tasks-sg"
  }
} 