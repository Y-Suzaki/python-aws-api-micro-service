import boto3


class ConfigRepository:
    def __init__(self):
        self._dynamodb = boto3.resource('dynamodb').Table('settings')

    def read(self, device_id: str) -> dict:
        print(f'ConfigRepository:read')
        response = self._dynamodb.get_item(Key={'imei': device_id})

        if 'Item' in response:
            return response["Item"]
        else:
            return {}

    def update(self, device_id: str, config: dict):
        print(f'ConfigRepository:update')
        return config
