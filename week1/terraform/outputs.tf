output "public_ip" {
  description = "vm public ip address"
  value       = tencentcloud_instance.web[0].public_ip
}

output "private_ip" {
  description = "vm public ip address"
  value       = tencentcloud_instance.web[0].private_ip
}

output "password" {
  description = "vm password"
  value       = var.password
}
