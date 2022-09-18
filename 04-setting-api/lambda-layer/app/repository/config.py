import boto3
import json
from helper.logger import LambdaJsonLogger

logger = LambdaJsonLogger.get_logger('DEBUG')


class ConfigRepository:
    def __init__(self):
        self._dynamodb = boto3.resource('dynamodb').Table('settings')

    def read(self, device_id: str) -> dict:
        # print(f'ConfigRepository:read')
        logger.info('ConfigRepository:read')
        logger.info({'test': 'aaaa', 'test2': 'bbbb'})
        response = self._dynamodb.get_item(Key={'imei': device_id})

        if 'Item' in response:
            return response["Item"]
        else:
            raise Exception(f'Parameter not found. {device_id}')

    def update(self, device_id: str, config: dict):
        print(f'ConfigRepository:update')
        return config
