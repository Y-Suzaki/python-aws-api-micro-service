#!/bin/bash -e

stack_name="micro-service-infra-base-aurora-mysql"

echo "Deploy Aurora MySQL..."
aws cloudformation deploy \
  --template-file infra/aurora-mysql.yml \
  --stack-name ${stack_name} \
  --capabilities CAPABILITY_IAM \
  --region ap-northeast-1 \
  --parameter-overrides \
    Env="${Env?}" \
  --profile default
