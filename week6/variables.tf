variable "aws_region" {
  type        = string
  description = "aws region"
  default     = "ap-south-1"
}

variable "vpc_name" {
  type        = string
  description = "vpc name"
  default     = "adityaweek6"
}

variable "primary_az" {
  type        = string
  description = "primary availability zone"
  default     = "ap-south-1a"
}

variable "secondary_az" {
  type        = string
  description = "secondary availability zone"
  default     = "ap-south-1b"
}

variable "app_name" {
  default = "student-portal"
}

variable "prefix" {
  default = "aditya-bootcamp"
}

variable "image" {
  type    = string
  default = "768093818017.dkr.ecr.ap-south-1.amazonaws.com/aditya-bootcamp-student-portal:1.0"
}

variable "container_port" {
  type    = number
  default = 8000
}

variable "domain_name" {
  type    = string
  default = "adishrivtech.in"
}

variable "alb_zone_id" {
  type        = string
  description = "zone id for ALB on ap-south-1 region"
  default     = "Z11ORPS3UI2S3F"
}
