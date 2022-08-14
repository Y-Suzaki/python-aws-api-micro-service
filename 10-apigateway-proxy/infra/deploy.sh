#!/bin/bash -ex

#stack_name_cognito="micro-service-apigateway-proxy-cognito"

echo "** Start to deploy and build. **"

#echo "Deploy cognito template for micro service..."
#aws cloudformation deploy \
#  --template-file 01-apigateway-proxy/infra/cognito.yml \
#  --stack-name ${stack_name_cognito} \
#  --no-fail-on-empty-changeset \
#  --capabilities CAPABILITY_IAM \
#  --region ap-northeast-1 \
#  --parameter-overrides Env="${Env?}" \
#  --profile default


stack_name_domain="micro-service-apigateway-proxy-domain-${ServiceName?}"

echo "Deploy cognito template for micro service..."
aws cloudformation deploy \
  --template-file infra/custom-domain.yml \
  --stack-name "${stack_name_domain}" \
  --no-fail-on-empty-changeset \
  --capabilities CAPABILITY_IAM \
  --region ap-northeast-1 \
  --parameter-overrides \
    Env="${Env?}" \
    DomainAppPrefix="${DomainAppPrefix?}" \
    DomainZoneId="${DomainZoneId?}" \
    DomainZoneName="${DomainZoneName?}" \
  --profile default
