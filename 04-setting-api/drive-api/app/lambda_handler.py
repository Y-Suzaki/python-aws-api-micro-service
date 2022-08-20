from aws_lambda_powertools.utilities.typing import LambdaContext
from integration.lambda_proxy import app
from internal.usecase.config import InternalConfigUseCase


@app.get('/devices/<device_id>/config')
def get(device_id: str):
    return InternalConfigUseCase.get(device_id=device_id)


@app.put('/devices/<device_id>/config')
def update(device_id: str):
    config: dict = app.current_event.json_body
    return InternalConfigUseCase.update(device_id=device_id, config=config)


def handler(event: dict, context: LambdaContext) -> dict:
    print(event)
    return app.resolve(event, context)
