#!/bin/bash -e

stack_name="micro-service-infra-base-vpc"

echo "Deploy base path mapping..."
aws cloudformation deploy \
  --template-file infra/vpc.yml \
  --stack-name ${stack_name} \
  --capabilities CAPABILITY_IAM \
  --region ap-northeast-1 \
  --parameter-overrides \
    Env="${Env?}" \
    EnableNatGatewayA="false" \
  --profile default
