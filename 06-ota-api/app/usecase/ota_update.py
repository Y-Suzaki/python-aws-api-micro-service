from typing import Final
from repository.ota_update import OTAUpdateRepository


class OTAUseCase:
    def __init__(self):
        self._ota_update = OTAUpdateRepository()

    def get_update_info(self) -> dict:
        signed_url = self._ota_update.generate_url('test.jpg')

        return {
            'name': 'app.test',
            'version': 10000,
            'signed_url': signed_url
        }
