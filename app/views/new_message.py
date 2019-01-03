import logging
import requests
from flask import render_template, request
from app.views.utils import URL

logger = logging.getLogger(__name__)


def new_message():
    if request.method == 'POST':
        return _new_message_post(request)
    else:
        return render_template(
            "new_message.html",
            action_path='',
        )


def _new_message_post(request):
    msg = _parse_html_form_message(request.form)
    users = _get_users()
    data = {
        'message': msg,
        'users': users,
    }
    response = requests.post('{}/messages'.format(URL), json=data)
    if response.status_code == 200:
        return render_template(
            'new_message.html',
            result='New post created!',
        )
    else:
        msg = 'Failure: {}'.format(response.status_code)
        return render_template(
            'response.html',
            msg=msg,
        )


def _get_users():
    response = requests.get('{}/users'.format(URL))
    if response.status_code == 200:
        users = response.json().get('users', [])
        ids = [user.get('_id') for user in users]
        return ids
    else:
        return None


def _parse_html_form_message(form):
    form_dict = form.to_dict(flat=False)
    body = form_dict.get('body', [''])
    type = form_dict.get('type', [''])
    group_message = form_dict.get('group_message', [''])

    message = {
        'body': body[0],
        'type':  type[0],
        'group_message': group_message[0],
    }

    return message
