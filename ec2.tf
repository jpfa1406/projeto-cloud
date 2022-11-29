locals {
  serverconfig = [
    for srv in var.configuration : [
      for i in range(1, srv.instance_count+1) : {
        instance_name = "${srv.instance_name}-${i}"
        instance_type = srv.instance_type
        instance_ami = srv.instance_ami
        instance_count = srv.instance_count
      }
    ]
  ]
}
// We need to Flatten it before using it
locals {
  instances = flatten(local.serverconfig)
}

resource "aws_instance" "app_server" {

  for_each = {for server in local.instances: server.instance_name =>  server}

  ami           = each.value.instance_ami
  instance_type = each.value.instance_type

  tags = {
    Name = "${each.value.instance_name}"
  }

  security_groups = ["${aws_security_group.ssh_access.id}"]
	subnet_id = aws_subnet.public.id
}
