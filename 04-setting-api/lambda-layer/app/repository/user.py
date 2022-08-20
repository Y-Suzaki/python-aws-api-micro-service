class UserRepository:
    def __init__(self):
        pass

    def get_profile(self, user_id: str) -> dict:
        return {
            'name': 'tanaka',
            'available_devices': [
                '012345678901234', '123456789012345'
            ]
        }
