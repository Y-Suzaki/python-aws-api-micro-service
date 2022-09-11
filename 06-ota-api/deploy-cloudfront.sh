#!/bin/bash -e

stack_name="micro-service-ota-api-cloudfront"

PublicKey=$(cat infra/key/public_key.pem)

echo "Deploy cloudfront..."
aws cloudformation deploy \
  --template-file infra/cloudfront.yml \
  --stack-name "${stack_name}" \
  --capabilities CAPABILITY_IAM \
  --region ap-northeast-1 \
  --parameter-overrides \
    Env="${Env?}" \
    PublicKey="${PublicKey?}" \
  --profile default
