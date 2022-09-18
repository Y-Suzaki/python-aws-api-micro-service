import datetime

from integration.lambda_proxy import app
from repository.user import UserRepository


def device(func):
    def _wrapper(*args, **keywords):
        # 前処理
        print(f'{func.__name__}の実行')
        print(f'開始: {datetime.datetime.now()}')

        user_id = app.current_event.request_context.identity.cognito_identity_id
        user_profile = UserRepository().get_profile(user_id=user_id)
        device_id = keywords.get('device_id', None)

        # 権限チェック
        if device_id not in user_profile['available_devices']:
            raise Exception(f'Permission Error. {device_id=}, {user_profile=}')

        print(f'{user_id=}, {device_id=}')

        # デコレート対象の関数の実行
        result = func(*args, **keywords)

        # 後処理
        print(f'終了: {datetime.datetime.now()}')
        print(f'実行結果: {result}')

        return result
    return _wrapper
