class ConfigRepository:
    def __init__(self):
        self._dynamodb = None

    def read(self, device_id: str) -> dict:
        print(f'ConfigRepository:read')
        return {
            'volume': 100,
            'storage_limit': 10
        }

    def update(self, device_id: str, config: dict):
        print(f'ConfigRepository:update')
        return config
