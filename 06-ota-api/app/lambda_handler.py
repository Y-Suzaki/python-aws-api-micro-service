from aws_lambda_powertools.utilities.typing import LambdaContext
from integration.lambda_proxy import app
from usecase.ota_update import OTAUseCase


@app.get('/ota/update')
def get_ota_update():
    return OTAUseCase().get_update_info()


def handler(event: dict, context: LambdaContext) -> dict:
    print(event)
    return app.resolve(event, context)
