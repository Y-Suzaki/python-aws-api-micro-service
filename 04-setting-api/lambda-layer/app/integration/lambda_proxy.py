from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver, Response, content_types, \
    APIGatewayRestResolver
from aws_xray_sdk.core import patch
from aws_lambda_powertools.utilities.typing import LambdaContext
from helper.logger import LambdaJsonLogger

# app = APIGatewayRestResolver()
app = APIGatewayRestResolver(strip_prefixes=['/setting-service'])   # デフォルトではAPI Gateway REST API (v1)が使われる。

# X-Rayの有効化に必要
patch(['boto3'])

logger = LambdaJsonLogger('DEBUG')


@app.exception_handler(Exception)
def handle_invalid_limit_qs(e: Exception):  # receives exception raised
    logger.exception(str(e), 'W0001')
    return Response(
        status_code=400,
        content_type=content_types.APPLICATION_JSON,
        body=f"Invalid request parameters. {str(e)}",
    )
