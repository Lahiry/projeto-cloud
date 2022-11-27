variable "aws_region" {
  type    = string
  default = "sa-east-1"
}

variable "security_groups" {
  type = list(object({
    name               = string
    description        = string
    ingress = list(object({
      rule_name        = string
      from_port        = number
      to_port          = number
      protocol         = string
      cidr_blocks      = list(string)
    }))
  }))
}

variable "instances" {
  type = list(object({
    name          = string
    ami           = string
    instance_type = string
    security_groups = list(string)
  }))
}

variable "users" {
  type = list(object({
    name = string
    restriction = object({
      name = string
      description = string
      actions = list(string)
      resources = list(string)
    })
  }))
}