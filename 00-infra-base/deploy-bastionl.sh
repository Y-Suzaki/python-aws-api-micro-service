#!/bin/bash -e

stack_name="micro-service-infra-base-bastion"

echo "Deploy Bastion..."
aws cloudformation deploy \
  --template-file infra/bastion.yml \
  --stack-name ${stack_name} \
  --capabilities CAPABILITY_IAM \
  --region ap-northeast-1 \
  --parameter-overrides \
    Env="${Env?}" \
  --profile default
