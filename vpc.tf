# VPC
resource "aws_vpc" "joao_vpc" {
  cidr_block = var.vpc_cidr
  tags = {
    Name = "VPC"
  }
}

resource "aws_subnet" "public" {
  vpc_id = aws_vpc.joao_vpc.id
  cidr_block = var.subnets_cidr
  availability_zone = var.azs
  map_public_ip_on_launch = true
  tags = {
    Name = "Subnet"
  }
}

resource "aws_security_group" "ssh_access" {
  name        = "allow_ssh"
  description = "Allow ssh inbound traffic"
  vpc_id      = aws_vpc.joao_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
  }
}