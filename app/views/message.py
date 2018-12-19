import logging
import requests
import json

from flask import render_template, request
from jinja2 import Template


URL = 'http://127.0.0.1:5000'
logger = logging.getLogger(__name__)


def message(message_id):
    if request.method == 'DELETE':
        return _message_delete(request, message_id)
    else:
        return _message(request, message_id)


def _message_delete(request, message_id):
    response = requests.delete('{}/messages/{}'.format(URL, message_id))
    if response.status_code == 200:
        msg = 'Message deleted!'
    else:
        msg = 'Failure: {}'.format(response.status_code)

    return render_template(
        'msg_creation_response.html',
        msg=msg,
    )


def _message(request, message_id):
    response = requests.get('{}/messages/{}'.format(URL, message_id))

    if response.status_code == 404:
        return render_template(
            'msg_creation_response.html',
            msg=response.json().get('message', '404, Could not retrieve the message.'),
        )
    if response.status_code != 200:
        return render_template(
            'msg_creation_response.html',
            msg='Failure: {}'.format(response.status_code),
        )

    return _format_message_template(response.json()['message'])


def _format_message_template(message):
    logger.warning(message)
    # Hack, because the receivers in string and not proper json as it should me
    receivers = json.loads(message.get('receivers').replace("'", '"').replace('False', 'false'))
    show_answers = True if message.get('type', 'fnf') != 'fnf' else False
    return render_template(
        'message_history.html',
        message=message,
        receivers=receivers,
        show_answers=show_answers,
    )
