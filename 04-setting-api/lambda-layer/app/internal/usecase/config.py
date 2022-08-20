from repository.config import ConfigRepository
from service import user_permission


class InternalConfigUseCase:
    @staticmethod
    @user_permission.device
    def get(*, device_id: str) -> dict:
        return ConfigRepository().read(device_id)

    @staticmethod
    @user_permission.device
    def update(*, device_id: str, config: dict):
        return ConfigRepository().update(device_id, config)
