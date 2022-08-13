from typing import Final


class UserUseCase:
    @staticmethod
    def get_users(limit: int = 10) -> list[dict]:
        return [
            {
                'id': 1,
                'name': 'tanaka'
            },
            {
                'id': 2,
                'name': 'suzuki'
            }
        ]

    @staticmethod
    def get(user_id: int) -> dict:
        return {
            'id': user_id,
            'name': 'tanaka'
        }

    @staticmethod
    def add_user(user: dict) -> dict:
        return user
