# CloudFront
## Generate Private Key and Public Key
```shell
openssl genrsa -out private_key.pem 2048
openssl rsa -pubout -in private_key.pem -out public_key.pem
```
