#!/bin/bash -e

ServiceName='kinesis-firehose'
stack_name_app="micro-service-${ServiceName?}-app"

echo "Deploy kinesis data firehose..."
aws cloudformation deploy \
  --template-file infra/kinesis-data-firehose.yml \
  --stack-name "${stack_name_app}" \
  --capabilities CAPABILITY_IAM \
  --region ap-northeast-1 \
  --parameter-overrides \
    Env="${Env?}" \
    ServiceName="${ServiceName?}" \
    DatalakeLocationDataBucket="${DatalakeLocationDataBucket?}" \
  --profile default
