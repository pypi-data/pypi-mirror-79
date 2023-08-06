import os

import click
import requests

from cotoba_cli.error import ApiResponseError
from cotoba_cli.configuration import Session


def _handle_requests_exception(response, *args, **kwargs):
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise ApiResponseError(status_code=e.response.status_code, body=e.response.text)
    except requests.exceptions.RequestException as e:
        raise RuntimeError(e)


def api_session(handle_error=True,
                authorization=True,
                content_type_json=False,
                api_key=None):
    session = requests.Session()
    if handle_error:
        session.hooks = {
            'response': _handle_requests_exception
        }
    if authorization:
        session.headers.update({'Authorization': Session().id_token})
    if content_type_json:
        session.headers.update({'Content-Type': 'application/json; charset=utf-8'})

    if api_key:
        session.headers.update({'x-api-key': api_key})

    return session


def validate_file_exists(ctx, param, value):
    if type(value) is str and not os.path.exists(value):
        raise click.BadParameter('file does not exist.')
    return value


def validate_end_date(ctx, param, value):
    start_date = ctx.params.get('start_date')
    end_date = value
    if start_date and end_date and start_date > end_date:
        raise click.BadParameter('end-date must be after start-date')
    return value
