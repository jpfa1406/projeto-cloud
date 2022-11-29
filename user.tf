resource "aws_iam_user" "lb" {
  count = length(var.user_name)
  name = "${element(var.user_name, count.index)}"
}

#resource "aws_iam_access_key" "newemp" {
#  count = length(var.username)
#  user = element(var.username,count.index)
#}

#output "password" {
#  value = aws_iam_user_login_profile.lb.encrypted_password
#}