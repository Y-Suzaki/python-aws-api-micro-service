import boto3
import threading
from typing import Any
from botocore.exceptions import ClientError


class SecureParameter:
    """ SSM Parameter Storeを操作するクラス。 """
    parameters: dict[str, Any] = {}
    ssm = boto3.client('ssm')
    lock = threading.Lock()

    @classmethod
    def get(cls, name: str) -> str:
        """ SSM Parameter Storeから、指定された名前のSecure Stringを取得する。
        :param str name: 取得対象のパラメータ名。
        :return str: 復号化済のSecure Stringの値
        """
        with cls.lock:
            if value := cls.parameters.get(name, None):
                return value

            try:
                response = cls.ssm.get_parameter(Name=name, WithDecryption=True)
            except ClientError as e:
                raise e

            new_value = response['Parameter']['Value']
            cls.parameters[name] = new_value
            print(f'Succeed to get new value. {new_value}')
            return new_value
