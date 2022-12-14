import boto3
import os
import json
from boto3.session import Session
import requests
from requests_aws4auth import AWS4Auth

# ACCOUNT_ID = os.environ['ACCOUNT_ID']
USER_POOL_ID = os.environ['USER_POOL_ID']
USER_ID = "y-suzaki"
ACCOUNT_ID = os.environ['ACCOUNT_ID']
PASSWORD = os.environ['PASSWORD']
CLIENT_ID = os.environ['CLIENT_ID']
IDENTITY_POOL_ID = os.environ['IDENTITY_POOL_ID']
TARGET_S3_BUCKET = "ys-dev-web-deploy-module"
DRIVE_API_URL = os.environ['DRIVE_API_URL']
SP_API_URL = os.environ['SP_API_URL']
KINESIS_FIREHOSE = os.environ['KINESIS_FIREHOSE']

region = 'ap-northeast-1'


def auth(user_id, password):
    """Cognito認証（Cognito UserPool）"""
    aws_client = boto3.client('cognito-idp', region_name=region)
    auth_result = aws_client.admin_initiate_auth(
        UserPoolId=USER_POOL_ID,
        ClientId=CLIENT_ID,
        AuthFlow="ADMIN_NO_SRP_AUTH",
        AuthParameters={
            "USERNAME": user_id,
            "PASSWORD": password,
        }
    )
    return auth_result


def authorize(id_token):
    """認可"""
    aws_client = boto3.client('cognito-identity', region_name=region)
    logins = {f'cognito-idp.{region}.amazonaws.com/{USER_POOL_ID}': id_token}

    cognito_identity_id = aws_client.get_id(
        AccountId=ACCOUNT_ID,
        IdentityPoolId=IDENTITY_POOL_ID,
        Logins=logins
    )

    credentials = aws_client.get_credentials_for_identity(
        IdentityId=cognito_identity_id['IdentityId'],
        Logins=logins
    )
    return credentials['Credentials']


def list_on_s3(credential):
    """Bucket内のオブジェクト一覧"""
    session = Session(
        aws_access_key_id=credential['AccessKeyId'],
        aws_secret_access_key=credential['SecretKey'],
        aws_session_token=credential['SessionToken'])

    s3_resource = session.resource('s3')
    bucket = s3_resource.Bucket(TARGET_S3_BUCKET)
    for key in bucket.objects.all():
        print(key.key)


def access_api_gateway(credential, api_path):
    """ IAM認証されたAPIGatewayにアクセスする。 """
    access_url = f'{DRIVE_API_URL}/{api_path}'
    print(f'{access_url}')
    aws_auth = AWS4Auth(
        credential['AccessKeyId'],
        credential['SecretKey'],
        region,
        'execute-api',
        session_token=credential['SessionToken'],
    )
    response = requests.get(access_url, auth=aws_auth)
    print(response.text)
    print()


def access_api_gateway_no_auth(api_path):
    access_url = f'{SP_API_URL}/{api_path}'
    print(f'{access_url}')
    response = requests.get(access_url)
    print(response.text)
    print()


def put_kinesis_firehose(credential, firehose_name: str):
    session = Session(
        aws_access_key_id=credential['AccessKeyId'],
        aws_secret_access_key=credential['SecretKey'],
        aws_session_token=credential['SessionToken'],
        region_name='ap-northeast-1')

    data_list = [
        {
            "user_id": 1,
            "user_name": "tanaka"
        },
        {
            "user_id": 2,
            "user_name": "y-suzaki"
        }
    ]

    kinesis = session.client('firehose')
    response = kinesis.put_record(
        DeliveryStreamName=firehose_name,
        Record={'Data': (json.dumps(data_list[0]) + "\n").encode()})
    response = kinesis.put_record(
        DeliveryStreamName=firehose_name,
        Record={'Data': (json.dumps(data_list[1]) + "\n").encode()})


def upload_s3(credential, bucket_name, key, file):
    session = Session(
        aws_access_key_id=credential['AccessKeyId'],
        aws_secret_access_key=credential['SecretKey'],
        aws_session_token=credential['SessionToken'],
        region_name='ap-northeast-1')

    s3 = session.resource('s3')
    s3bucket = s3.Bucket(bucket_name)
    s3bucket.upload_file(key, file)


_auth_result = auth(USER_ID, PASSWORD)
_credential = authorize(id_token=_auth_result["AuthenticationResult"]["IdToken"])
# list_on_s3(_credential)

# access_api_gateway(_credential, 'user-service/users?limit=100')
# access_api_gateway(_credential, 'location-service/devices/12345/location/available_days')
# access_api_gateway(_credential, 'setting-service/devices/012345678901234/config')
# access_api_gateway(_credential, 'setting-service/devices/999999999/config')

# access_api_gateway(_credential, 'event-service/events')
try:
    upload_s3(_credential, 'ys-dev-web-datalake-analytics', 'upload.json',
              'ap-northeast-1:6d54d2ad-d36a-4745-9f64-87273d2e53e3/upload.json')
except Exception as e:
    print(e)

upload_s3(_credential, 'ys-dev-web-datalake-analytics', 'upload.json',
          'ap-northeast-1:6d54d2ad-d36a-4745-9f64-87273d2e53e2/upload.json')

# access_api_gateway_no_auth('setting-service/devices/12345/config')

# put_kinesis_firehose(_credential, KINESIS_FIREHOSE)

print('Completed!')
