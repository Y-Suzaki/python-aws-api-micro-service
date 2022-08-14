#!/bin/bash -e

stack_name="micro-service-user-api-base-path-mapping"

echo "Deploy base path mapping..."
aws cloudformation deploy \
  --template-file infra/base-path-mapping.yml \
  --stack-name ${stack_name} \
  --capabilities CAPABILITY_IAM \
  --region ap-northeast-1 \
  --parameter-overrides \
    Env="${Env?}" \
    APIVersion="${APIVersion?}" \
    DomainAppPrefix="${DomainAppPrefix?}" \
    DomainZoneName="${DomainZoneName?}" \
  --profile default
