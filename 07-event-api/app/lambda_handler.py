from aws_lambda_powertools.utilities.typing import LambdaContext
from integration.lambda_proxy import app
from repository.adas_event import AdasEventRepository


@app.get('/events')
def get_event_url():
    print('**************************************')
    print(app.current_event.headers)
    print(app.current_event.request_context)
    identity_id = app.current_event.request_context.identity.cognito_identity_id
    print(identity_id)
    print('**************************************')
    return {'message': 'OK'}


@app.get('/devices/<device_id>/adas_events')
def get_adas_events(device_id: str):
    print('**************************************')
    print(f'{device_id=}')
    adas_events = AdasEventRepository().get_events(device_id)


def handler(event: dict, context: LambdaContext) -> dict:
    print(event)
    return app.resolve(event, context)


if __name__ == '__main__':
    import os
    _event = {
        'resource': '/devices/{device_id}/adas_events',
        'path': '/event-service/devices/123456789012345/adas_events',
        'httpMethod': 'GET',
        'headers': {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'api-drive-dev.ys-dev-web.tk',
            'User-Agent': 'python-requests/2.28.1',
            'x-amz-content-sha256': '',
            'x-amz-date': '20220814T155111Z',
            'x-amz-security-token': '',
            'X-Forwarded-For': '133.200.47.128',
            'X-Forwarded-Port': '443',
            'X-Forwarded-Proto': 'https'},
        'multiValueHeaders': {},
        'queryStringParameters': None,
        'multiValueQueryStringParameters': None,
        'pathParameters': {'device_id': '12345'},
        'stageVariables': None,
        'requestContext': {},
        'body': None,
        'isBase64Encoded': False
    }

    os.environ['AWS_XRAY_SDK_ENABLED'] = 'false'
    os.environ['_X_AMZN_TRACE_ID'] = 'Trace-001'
    os.environ['AWS_S3_BUCKET_QUERY_RESULTS'] = 'ys-dev-web-datalake-analytics'

    from lambda_handler import handler
    handler(_event, None)
