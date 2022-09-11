import os
import boto3
from datetime import datetime, timedelta

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from botocore.signers import CloudFrontSigner
from botocore.exceptions import ClientError
from helper.secure_parameter import SecureParameter


class OTAUpdateRepository:
    def __init__(self):
        self._public_key_id = os.environ['PUBLIC_KEY_ID']
        self._cloudfront_domain = os.environ['CLOUDFRONT_DOMAIN']
        self._expire_seconds = os.environ['EXPIRE_SECONDS']

        private_key_name: str = os.environ['PRIVATE_KEY_NAME']
        self._private_key = SecureParameter.get(private_key_name)

    def _rsa_signer(self, message):
        private_key = serialization.load_pem_private_key(
            self._private_key.encode(),
            password=None,
            backend=default_backend()
        )
        return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())

    def generate_url(self, file_path):
        url = f'https://{self._cloudfront_domain}/{file_path}'
        expire_date = datetime.utcnow() + timedelta(seconds=float(self._expire_seconds))
        cloudfront_signer = CloudFrontSigner(self._public_key_id, self._rsa_signer)

        try:
            return cloudfront_signer.generate_presigned_url(url, date_less_than=expire_date)
        except ClientError as e:
            raise e
