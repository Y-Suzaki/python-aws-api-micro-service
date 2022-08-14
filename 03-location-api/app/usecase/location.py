from typing import Final


class LocationUseCase:
    @staticmethod
    def get_available_days(device_id: str, limit: int = 10) -> dict:
        return {
            "start": "2022-08-08T12:12:12Z",
            "end": "2022-08-0T10:12:12Z",
            "available_days": [
                1,
                0,
                1
            ]
        }

    @staticmethod
    def get_route(device_id: str) -> dict:
        return {
            "start": "2022-08-08T12:12:12Z",
            "end": "2022-08-0T10:12:12Z",
            "locations": [
                {
                    "lat": 35.99,
                    "lng": 139.11
                }
            ]
        }

    @staticmethod
    def add_user(user: dict) -> dict:
        return user
