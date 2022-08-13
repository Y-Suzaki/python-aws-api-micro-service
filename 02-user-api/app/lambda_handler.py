from aws_lambda_powertools.utilities.typing import LambdaContext
from integration.lambda_proxy import app
from usecase.user import UserUseCase


@app.get('/users')
def get_users():
    # query_strings = app.current_event.query_string_parameters
    # headers = app.current_event.headers
    return UserUseCase.get_users()


@app.get('/users/<user_id>')
def get(user_id: str):
    _id = int(user_id)
    return UserUseCase.get(_id)


@app.post('/users')
def add_user():
    user: dict = app.current_event.json_body
    print(f'{user=}')
    added_user = UserUseCase.add_user(user)
    return added_user


def handler(event: dict, context: LambdaContext) -> dict:
    print(event)
    return app.resolve(event, context)
