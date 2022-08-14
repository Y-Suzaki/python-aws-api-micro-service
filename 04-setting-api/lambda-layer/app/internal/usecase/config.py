from repository.config import ConfigRepository


class InternalConfigUseCase:
    @staticmethod
    def get(device_id: str) -> dict:
        return ConfigRepository().read(device_id)

    @staticmethod
    def update(device_id: str, config: dict):
        return ConfigRepository().update(device_id, config)
