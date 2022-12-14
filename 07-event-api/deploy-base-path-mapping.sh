#!/bin/bash -e

ServiceName="event-service"
stack_name="micro-service-${ServiceName?}-api-base-path-mapping"

echo "Deploy base path mapping..."
aws cloudformation deploy \
  --template-file infra/base-path-mapping.yml \
  --stack-name ${stack_name} \
  --capabilities CAPABILITY_IAM \
  --region ap-northeast-1 \
  --parameter-overrides \
    Env="${Env?}" \
    ServiceName="${ServiceName?}" \
    APIVersion="${APIVersion?}" \
    DomainAppPrefix="${DomainAppPrefix?}" \
    DomainZoneName="${DomainZoneName?}" \
  --profile default
