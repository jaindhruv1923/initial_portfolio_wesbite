variable "aws_region" {
  description = "AWS deployment region"
  type        = string
  default     = "ap-south-1" # Mumbai region for Indian DPDP Act data residency
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "production"
}

variable "app_name" {
  description = "Application name"
  type        = string
  default     = "kavach-platform"
}

variable "fargate_cpu" {
  description = "Fargate instance CPU units (1024 = 1 vCPU)"
  type        = string
  default     = "1024"
}

variable "fargate_memory" {
  description = "Fargate instance memory (in MiB)"
  type        = string
  default     = "2048"
}
