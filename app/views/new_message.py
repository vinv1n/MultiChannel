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
    cookies = request.cookies
    msg_data = _parse_html_form_message(request.form)
    users = _get_users(cookies)
    data = {
        'message': msg_data.get('body'),
        'sender' : msg_data.get('sender'),
        'users': users,
        'type' : msg_data.get('type'),
        'group_message': msg_data.get('group_message')
    }
    
    response = requests.post('{}/messages'.format(URL), json=data, cookies=cookies, verify=False)
    
    if response.status_code == 200:
        return render_template(
            'new_message.html',
            result='New post created!',
        )
    else:
       
       return render_template(
            'new_message.html',
            result=response.status_code,
        )


def _get_users(cookies):
    response = requests.get('{}/users'.format(URL), cookies=cookies, verify=False)
    if response.status_code == 200:
        users = response.json().get('users', [])
        ids = [user.get('_id') for user in users]
        if ids != []:
            return ids
    else:
        return None


def _parse_html_form_message(form):
    form_dict = form.to_dict(flat=False)
    body = form_dict.get('body', [''])
    sender = form_dict.get('sender', [''])
    type = form_dict.get('type', [''])
    group_message = form_dict.get('group_message', [''])

    message_data = {
        'body': body[0],
        'sender': sender[0],
        'type':  type[0],
        'group_message': group_message[0],
    }

    return message_data