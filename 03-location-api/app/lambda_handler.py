from aws_lambda_powertools.utilities.typing import LambdaContext
from integration.lambda_proxy import app
from usecase.location import LocationUseCase


@app.get('/devices/<device_id>/location/available_days')
def get_available_days(device_id: str):
    return LocationUseCase.get_available_days(device_id)


@app.get('/devices/<device_id>/location/route')
def get_route(device_id: str):
    return LocationUseCase.get_route(device_id)


def handler(event: dict, context: LambdaContext) -> dict:
    print(event)
    return app.resolve(event, context)
