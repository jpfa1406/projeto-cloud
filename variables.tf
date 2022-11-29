
#EC2 ------------------------------------------------
variable "configuration" {
    default = [{}]
}

#variable "instance_type" {
#  type = string
#  description = ""
#  default = "t2.micro"
#}

#variable "instance_ami" {
#  type = string
#  description = ""
#  default = "ami-0149b2da6ceec4bb0"
#}

#variable "instance_count" {
#    type = string
#    description = "quantidade de instancias criadas"
#    default = "1"
#}

#variable "instance_name" {
#    default = "instance"  
#}
#----------------------------------------------------


#VPC-------------------------------------------------
variable "vpc_cidr" {
	default = "10.20.0.0/16"
}

variable "subnets_cidr" {
	default = "10.20.0.0/16"
}

variable "azs" {
	default = "us-east-1a"
}
#----------------------------------------------------

#USER------------------------------------------------
variable "user_name" {
  type = list
  default = ["user"]
}

variable "user_password" {
  default = "user"
}
#----------------------------------------------------