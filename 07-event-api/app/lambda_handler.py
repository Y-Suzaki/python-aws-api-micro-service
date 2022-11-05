from aws_lambda_powertools.utilities.typing import LambdaContext
from integration.lambda_proxy import app


@app.get('/events')
def get_event_url():
    print('**************************************')
    print(app.current_event.headers)
    print(app.current_event.request_context)
    print('**************************************')
    return {'message': 'OK'}


def handler(event: dict, context: LambdaContext) -> dict:
    print(event)
    return app.resolve(event, context)
