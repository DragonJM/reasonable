
resource "aws_instance" "web" {
  ami           = "ami-0cf4e1fcfd8494d5b"
  instance_type = "t3.micro"
  key_name = "jordan"

  tags = {
    Name = "HelloWorld"
  }
}