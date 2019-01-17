import logging
import requests

from flask import render_template, request
from app.views.utils import URL

logger = logging.getLogger(__name__)


def message_status(message_id):
    if request.method == 'POST':
        return _message_status_delete(request, message_id)
    else:
        return _message_status(request, message_id)


def _message_status_delete(request, message_id):
    response = requests.delete('{}/messages/{}'.format(URL, message_id), cookies=request.cookies)
    if response.status_code == 200:
        msg = 'Message deleted!'
    else:
        msg = 'Failure when deleting message: {}'.format(response.status_code)

    return render_template(
        'response_admin.html',
        msg=msg,
    )


def _message_status(request, message_id):
    response = requests.get('{}/messages/{}'.format(URL, message_id), cookies=request.cookies)

    if response.status_code == 404:
        return render_template(
            'response.html',
            msg=response.json().get('message', '404, Could not retrieve the message.'),
        )
    if response.status_code != 200:
        return render_template(
            'response.html',
            msg='Failure: {}'.format(response.status_code),
        )

    user_response = requests.get(
        '{}/users'.format(URL),
        cookies=request.cookies
    )
    users = user_response.json()
    usernames = {user.get('_id'): user.get('username') for user in users.get('users',  [])}

    return _format_message_status_template(response.json()['message'], usernames)


def _format_message_status_template(message, usernames):
    receivers = message.get('receivers')
    show_answers = True if message.get('type', 'fnf') != 'fnf' else False

    return render_template(
        'message_status.html',
        message=message,
        receivers=receivers,
        show_answers=show_answers,
        usernames=usernames,
    )
