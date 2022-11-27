terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = var.aws_region
}

resource "aws_vpc" "vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "VPC"
  }
}

resource "aws_subnet" "subnet" {
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "sa-east-1a"
 
 tags = {
    Name = "Public Subnet"
 }
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "VPC Internet Gateway"
  }
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = {
    Name = "Public Route"
  }
}

resource "aws_route_table_association" "public_subnet_asso" {
  subnet_id      = aws_subnet.subnet.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_security_group" "security_group" {
  for_each    = { for security_group in var.security_groups : security_group.name => security_group }
  description = each.value.description
  vpc_id      = aws_vpc.vpc.id

  tags = {
    Name = each.value.name
  }

  dynamic "ingress" {
    for_each = each.value.ingress

    content {
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
    }
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "ec2_instance" {
  for_each               = { for instance in var.instances : instance.name => instance }
  ami                    = each.value.ami
  instance_type          = each.value.instance_type
  vpc_security_group_ids = [for security_group_name in each.value.security_groups : aws_security_group.security_group[security_group_name].id]
  subnet_id              = aws_subnet.subnet.id 

  tags = {
    Name = each.value.name
  }
}

resource "aws_iam_user" "iam_user" {
  for_each = { for iam_user in var.users : iam_user.name => iam_user }
  name     = each.value.name
}	

resource "aws_iam_access_key" "iam_access_key" {
  for_each = { for user in var.users : user.name => user }
  user     = aws_iam_user.iam_user[each.value.name].name
}

data "aws_iam_policy_document" "ec2_policy" {
  for_each    = { for user in var.users : user.name => user }
  policy_id   = each.value.name
  statement {
    effect    = "Allow"
    actions   = each.value.restriction.actions
    resources = each.value.restriction.resources
  }
}

resource "aws_iam_policy" "ec2_policy" {
  for_each    = { for user in var.users : user.name => user }
  name        = each.value.restriction.name
  description = each.value.restriction.description
  policy      = data.aws_iam_policy_document.ec2_policy[each.value.name].json
}

resource "aws_iam_user_policy_attachment" "user_policy_attachment" {
  for_each   = { for user in var.users : user.name => user }
  user       = aws_iam_user.iam_user[each.value.name].name
  policy_arn = aws_iam_policy.ec2_policy[each.value.name].arn
}

resource "aws_iam_user_login_profile" "profile" {
    for_each                = { for user in var.users : user.name => user }
    user                    = aws_iam_user.iam_user[each.value.name].name
    password_reset_required = true
}