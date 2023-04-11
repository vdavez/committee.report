resource "aws_scheduler_schedule" "scheduler" {
    name                    = "crpts-ecs-run"
    description             = "A run of the ECS for crpts"
    group_name              = "default"
    schedule_expression     = "cron(5 0 ? * * *)"

    target {
        arn = aws_ecs_cluster.cluster.arn
        role_arn = aws_iam_role.eventbridge_role.arn

        retry_policy {
            maximum_retry_attempts       = 5
        }

        ecs_parameters {
            launch_type             = "FARGATE"
            task_count              = 1
            task_definition_arn     = aws_ecs_task_definition.definition.arn

            network_configuration {
                assign_public_ip = true
                security_groups  = [aws_security_group.ecs_tasks.id]
                subnets          = aws_subnet.public.*.id
            }
        }
    }
    flexible_time_window {
        mode = "FLEXIBLE"
        maximum_window_in_minutes = 15
    }

}
