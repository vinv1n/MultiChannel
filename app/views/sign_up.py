import logging
import requests
from flask import render_template, request
from app.views.utils import URL

logger = logging.getLogger(__name__)


def sign_up():
    if request.method == 'POST':
        return _sign_up_post(request)
    else:
        return render_template(
            'sign_up.html',
        )


def _sign_up_post(request):
    msg = _sign_up_html_parser(request.form)
    logger.warning('sign_up msg: {}'.format(msg))

    response = requests.post('{}/users'.format(URL), json=msg)

    if response.status_code == 200:
        msg = 'New user created!'
    else:
        msg = 'Error while creating user: {}'.format(response.json().get('msg'))

    return render_template(
        'response.html',
        msg=msg,
    )


def _sign_up_html_parser(form):
    form_dict = form.to_dict(flat=False)
    user_data = {
        "username": form_dict['username'][0],
        "password": form_dict['password'][0],
        "preferred_channel": form_dict['preferred_channel'][0],
        "channels": {
            "email": {"address": form_dict['email_address'][0]},
            "facebook": {"user_id": form_dict['facebook'][0]},
            "telegram": {"user_id": form_dict['telegram'][0]},
            "irc": {"nickname": form_dict['irc_nick'][0], "network": form_dict['irc_network'][0]},
            "slack": {"channel": form_dict['slack_channel'][0], "username": form_dict['slack_user'][0]},
        }
    }
    return user_data