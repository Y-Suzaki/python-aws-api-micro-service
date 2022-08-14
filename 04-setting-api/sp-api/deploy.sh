#!/bin/bash -e

ServiceName="setting-service"
stack_name_app="micro-service-${ServiceName?}-sp-api-app"

echo "** Start to deploy and build. **"

echo "Upload open-api.yml on s3"
aws s3 cp docs/open-api.yml s3://"${DeployArtifactBucket?}"/"${ServiceName?}"/

echo "Zip python codes"
mkdir -p lambda
cp infra/web-api.yml lambda/
cp -r app/ lambda/
cp -r ../lambda-layer/app/ lambda/
cd lambda/app
pip install -r requirements.txt -t .
zip -r ../lambda.zip ./*
cd ..

echo "Build serverless function..."
aws cloudformation package \
  --template-file web-api.yml \
  --output-template-file web-api-deploy.yml \
  --s3-bucket "${DeployArtifactBucket?}" \
  --s3-prefix serverless-function \
  --region ap-northeast-1 \
  --profile default

echo "Deploy serverless function..."
aws cloudformation deploy \
  --template-file web-api-deploy.yml \
  --stack-name ${stack_name_app} \
  --capabilities CAPABILITY_IAM \
  --region ap-northeast-1 \
  --parameter-overrides \
    Env="${Env?}" \
    ServiceName="${ServiceName}" \
    APIVersion="${APIVersion?}" \
    DeployArtifactBucket="${DeployArtifactBucket?}" \
    AppEnvironmentLogLevel="${AppEnvironmentLogLevel?}" \
  --profile default

echo "** All complete! **"
aws s3 rm s3://"${DeployArtifactBucket?}"/serverless-function/ \
  --region ap-northeast-1 \
  --profile default \
  --recursive

cd ..
rm -rf lambda/
