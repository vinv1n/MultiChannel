import logging
import requests
from flask import render_template, request

URL = 'http://127.0.0.1:5000'
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
        msg = 'Error while creating user: {}'.format(response.status_code)

    return render_template(
        'response.html',
        msg=msg,
    )


def _sign_up_html_parser(form):
    form_dict = form.to_dict(flat=False)
    logger.warning(form_dict)

    return {
        "username": form_dict['username'],
        "password": form_dict['password'],
        "preferred_channel": form_dict['preferred_channel'],
        "channels": {
            "email": {"address": form_dict['email_address']},
            # "facebook": {"user_id": form_dict['facebook']},
            "telegram": {"user_id": form_dict['telegram']},
            "irc": {"nickname": form_dict['irc_nick'], "network": form_dict['irc_network']},
            # "slack": {"channel": slack_channel, "username": slack_user},
        }
    }
