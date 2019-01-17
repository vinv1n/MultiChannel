import logging
import requests
from flask import render_template, request, flash, redirect
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
    form_dict = request.form.to_dict(flat=False)

    password = form_dict.get('password')[0]
    password_confirm = form_dict.get('password')[0]
    username = form_dict.get('username')[0]

    if not username:
        flash('Please give username.')
        return render_template('sign_up.html')
    elif not password:
        flash('Please give password.')
        return render_template('sign_up.html')
    elif password != password_confirm:
        flash('Password does not match with confirmed one, please try again.')
        return render_template('sign_up.html')

    msg = _sign_up_html_parser(form_dict)

    response = requests.post('{}/users'.format(URL), json=msg)

    if response.status_code == 200:
        flash('New user created, you can now log in.')
        return redirect('/webui/login')
    else:
        msg = 'User creation error: {}'.format(response.json().get('msg'))
        flash(msg)
        return render_template('sign_up.html')


def _sign_up_html_parser(form_dict):
    user_data = {
        "username": form_dict.get('username', [''])[0],
        "password": form_dict.get('password', [''])[0],
        "preferred_channel": form_dict.get('preferred_channel', [''])[0],
        "channels": {
            "email": {"address": form_dict.get('email_address', [''])[0]},
            "facebook": {"user_id": form_dict.get('facebook', [''])[0]},
            "telegram": {"user_id": form_dict.get('telegram', [''])[0]},
            "irc": {"nickname": form_dict.get('irc_nick', [''])[0], "network": form_dict.get('irc_network', [''])[0]},
            "slack": {"channel": form_dict.get('slack_channel', [''])[0], "username": form_dict.get('slack_user', [''])[0]},
        }
    }
    return user_data
