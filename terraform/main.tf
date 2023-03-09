terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
    region                      = "us-east-1"
    shared_credentials_files    = ["~/.aws/credentials"]
}

resource "aws_ecs_cluster" "cluster" {
  name = "crpts-cluster"
}

resource "aws_ecs_task_definition" "definition" {
  family                   = "crpts-ecs-task"
  task_role_arn            = aws_iam_role.ecs_task_role.arn
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  network_mode             = "awsvpc"
  cpu                      = "256"
  memory                   = "1024"
  requires_compatibilities = ["FARGATE"]

  container_definitions = <<DEFINITION
[
  {
    "image": "public.ecr.aws/i4f5a0p9/crpts:latest",
    "name": "converter",
    "command": ["python,main.py,getfromday"],
    "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-region" : "us-east-1",
                    "awslogs-group": "/ecs/crpt2epub2",
                    "awslogs-stream-prefix" : "crpt2epub"
                }
            },
    "environment": [
                {
                    "name": "DATA_DOT_GOV_API_KEY",
                    "value": "${var.DATA_DOT_GOV_API_KEY}"
                },
                {
                    "name": "AWS_ACCESS_KEY_ID",
                    "value": "${var.AWS_ACCESS_KEY_ID}"
                },
                {
                    "name": "AWS_SECRET_ACCESS_KEY",
                    "value": "${var.AWS_SECRET_ACCESS_KEY}"
                }
            ]
    }

]
DEFINITION
}