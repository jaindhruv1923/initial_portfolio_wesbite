output = {
  "alb_dns_name" = {
    value       = aws_lb.main.dns_name
    description = "Public DNS hostname of Application Load Balancer"
  }
  "ecs_cluster_name" = {
    value       = aws_ecs_cluster.main.name
    description = "Name of the ECS Fargate cluster"
  }
  "kavach_health_url" = {
    value       = "http://${aws_lb.main.dns_name}/health"
    description = "Public URL for KAVACH platform health probe"
  }
}
