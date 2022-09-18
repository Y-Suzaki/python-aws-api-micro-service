import os
import time
import traceback
import json
from logging import getLogger, Formatter, StreamHandler


class LambdaJsonLogger:
    @classmethod
    def get_logger(cls, level: str):
        return LambdaJsonLogger(level)

    @classmethod
    def get_aws_request_id(cls):
        return os.environ.get('_X_AMZN_TRACE_ID', None)

    def __init__(self, level: str):
        self.logger = getLogger(__name__)
        self.logger.setLevel(level)

        # self._request_id = os.environ.get('_X_AMZN_TRACE_ID', None)

        self.formatter = Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "error_code": "%(error_code)s", '
            '"message": "%(msg)s", "aws_request_id": "%(aws_request_id)s"}',
            '%Y-%m-%dT%H:%M:%SZ')
        self.formatter.converter = time.gmtime

        self.formatter_exception = Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "error_code": "%(error_code)s", '
            '"message": "%(msg)s", "aws_request_id": "%(aws_request_id)s", "exception": %(exception)s}',
            '%Y-%m-%dT%H:%M:%SZ')
        self.formatter_exception.converter = time.gmtime

        if self.logger.handlers:
            for _handler in self.logger.handlers:
                self.logger.removeHandler(_handler)

        handler = StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)

    def debug(self, msg, error_code='-'):
        _extra = {
            'error_code': error_code,
            'aws_request_id': self.get_aws_request_id()
        }
        self.logger.debug(msg, extra=_extra)

    def info(self, msg, error_code='-'):
        _extra = {
            'error_code': error_code,
            'aws_request_id': self.get_aws_request_id()
        }
        self.logger.info(msg, extra=_extra)

    def warning(self, msg, error_code='-'):
        _extra = {
            'error_code': error_code,
            'aws_request_id': self.get_aws_request_id()
        }
        self.logger.warning(msg, extra={'error_code': error_code})

    def error(self, msg, error_code):
        _extra = {
            'error_code': error_code,
            'aws_request_id': self.get_aws_request_id()
        }
        self.logger.error(msg, extra={'error_code': error_code})

    def exception(self, msg, error_code):
        self.logger.handlers[0].setFormatter(self.formatter_exception)
        # exception = json.dumps(traceback.format_exc().splitlines())
        _extra = {
            'error_code': error_code,
            'aws_request_id': self.get_aws_request_id(),
            'exception': json.dumps(traceback.format_exc())
            # 'exception': json.dumps(traceback.format_exc().splitlines())
        }
        self.logger.error(msg, extra=_extra)
        self.logger.handlers[0].setFormatter(self.formatter)
