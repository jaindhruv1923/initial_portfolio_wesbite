# Security Group for ALB
resource "aws_security_group" "alb_sg" {
  name        = "${var.app_name}-alb-sg"
  description = "Allow inbound HTTP/HTTPS traffic to ALB"
  vpc_id      = aws_vpc.kavach_vpc.id

  ingress {
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
}

# Application Load Balancer
resource "aws_lb" "main" {
  name               = "${var.app_name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = [aws_subnet.public_1.id, aws_subnet.public_2.id]
  tags               = { Name = "${var.app_name}-alb" }
}

# Target Group 1: KAVACH Platform (Port 8000)
resource "aws_lb_target_group" "kavach_tg" {
  name        = "${var.app_name}-tg-8000"
  port        = 8000
  protocol    = "HTTP"
  vpc_id      = aws_vpc.kavach_vpc.id
  target_type = "ip"

  health_check {
    path                = "/health"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 3
    matcher             = "200"
  }
}

# Target Group 2: Bharat Core Banking (Port 8050)
resource "aws_lb_target_group" "banking_tg" {
  name        = "${var.app_name}-tg-8050"
  port        = 8050
  protocol    = "HTTP"
  vpc_id      = aws_vpc.kavach_vpc.id
  target_type = "ip"

  health_check {
    path                = "/api/bank/accounts"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 3
    matcher             = "200"
  }
}

# Target Group 3: Results Cockpit (Port 8090)
resource "aws_lb_target_group" "results_tg" {
  name        = "${var.app_name}-tg-8090"
  port        = 8090
  protocol    = "HTTP"
  vpc_id      = aws_vpc.kavach_vpc.id
  target_type = "ip"

  health_check {
    path                = "/api/results/summary"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 3
    matcher             = "200"
  }
}

# HTTP Listener on Port 80
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.kavach_tg.arn
  }
}

# Path-based routing for Banking (/api/bank/*)
resource "aws_lb_listener_rule" "banking_rule" {
  listener_arn = aws_lb_listener.http.arn
  priority     = 10

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.banking_tg.arn
  }

  condition {
    path_pattern {
      values = ["/api/bank*"]
    }
  }
}

# Path-based routing for Results (/results/*)
resource "aws_lb_listener_rule" "results_rule" {
  listener_arn = aws_lb_listener.http.arn
  priority     = 20

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.results_tg.arn
  }

  condition {
    path_pattern {
      values = ["/results*"]
    }
  }
}
