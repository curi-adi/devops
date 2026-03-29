# VPC

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = var.vpc_name
  }
}

# public ->  "10.0.1.0/24", "10.0.2.0/24"
# private -> "10.0.3.0/24", "10.0.4.0/24"
# rds ->  "10.0.5.0/24", "10.0.6.0/24"

# 2 public subnets

resource "aws_subnet" "public1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = var.primary_az

  tags = {
    Name = "${var.vpc_name}-public1"
  }
}

resource "aws_subnet" "public2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.2.0/24"
  map_public_ip_on_launch = true
  availability_zone       = var.secondary_az

  tags = {
    Name = "${var.vpc_name}-public2"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "main"
  }
}

# 1 Route table for public subnets
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = {
    Name = "public RT"
  }
}

# Add public subnets to route table
resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.public1.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "b" {
  subnet_id      = aws_subnet.public2.id
  route_table_id = aws_route_table.public.id
}

# NAT Gateway (only 1 for cost saving)
resource "aws_eip" "nat" {
}

resource "aws_nat_gateway" "primary" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public1.id

  tags = {
    Name = "gw NAT"
  }

  depends_on = [aws_internet_gateway.gw, aws_route_table.public]
}

# 2 private subnets
resource "aws_subnet" "private1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.3.0/24"
  map_public_ip_on_launch = false
  availability_zone       = var.primary_az

  tags = {
    Name = "${var.vpc_name}-private1"
  }
}

resource "aws_subnet" "private2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.4.0/24"
  map_public_ip_on_launch = false
  availability_zone       = var.secondary_az

  tags = {
    Name = "${var.vpc_name}-private2"
  }
}

# 1 Route table for private subnets
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "private RT"
  }
}

resource "aws_route" "nat" {
  route_table_id         = aws_route_table.private.id
  nat_gateway_id         = aws_nat_gateway.primary.id
  destination_cidr_block = "0.0.0.0/0"
}

resource "aws_route_table_association" "c" {
  subnet_id      = aws_subnet.private1.id
  route_table_id = aws_route_table.private.id
}

resource "aws_route_table_association" "d" {
  subnet_id      = aws_subnet.private2.id
  route_table_id = aws_route_table.private.id
}

# 2 RDS subnets
resource "aws_subnet" "rds1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.5.0/24"
  map_public_ip_on_launch = false
  availability_zone       = var.primary_az

  tags = {
    Name = "${var.vpc_name}-rds1"
  }
}

resource "aws_subnet" "rds2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.6.0/24"
  map_public_ip_on_launch = false
  availability_zone       = var.secondary_az

  tags = {
    Name = "${var.vpc_name}-rds2"
  }
}
