#!/bin/bash -ex

stack_name_app="micro-service-user-api-app"

echo "** Start to deploy and build. **"

echo "Upload open-api.yml on s3"
aws s3 cp docs/open-api.yml s3://"${DeployArtifactBucket?}"/

echo "Zip python codes"
mkdir -p lambda
cp infra/web-api.yml lambda/
cp -r app/ lambda/
cd lambda/app

# Because mysql client uses os native library, execute "pip" in docker container.
docker run -v "$PWD:/var/task" public.ecr.aws/sam/build-python3.9  \
  /bin/sh -c "yum install python-devel mysql-devel libmariadb-dev -y &&  pip install -r requirements.txt -t ."
docker ps -aq | xargs docker rm

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
    APIVersion="${APIVersion?}" \
    DeployArtifactBucket="${DeployArtifactBucket?}" \
    AppEnvironmentLogLevel="${AppEnvironmentLogLevel?}" \
    AppEnvironmentRDSPassword="${AppEnvironmentRDSPassword?}" \
    MonitoringXRay="${MonitoringXRay}" \
  --profile default

echo "** All complete! **"
aws s3 rm s3://"${DeployArtifactBucket?}"/serverless-function/ \
  --region ap-northeast-1 \
  --profile default \
  --recursive

cd ..
rm -rf lambda/
