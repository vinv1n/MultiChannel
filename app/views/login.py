import logging
import requests
from flask import render_template, request, redirect, flash
from flask_jwt_extended import decode_token
from app.views.utils import URL

logger = logging.getLogger(__name__)


def login():
    if request.method == 'POST':
        return _login_post(request)
    else:
        return render_template(
            'login.html',
        )


def _login_post(request):
    password = request.form['password']
    name = request.form['name']
    data = {'password': password, 'username': name}
    response = requests.post('{}/user-login'.format(URL), json=data)

    if response.status_code != 200:
        flash(response.json().get('msg'))
        return render_template('login.html')

    access_token = response.cookies.get('access_token_cookie')
    refresh_token = response.cookies.get('refresh_token_cookie')
    decoded_token = decode_token(access_token)
    admin = decoded_token.get('identity', {}).get('admin')

    if admin:
        location = 'home'
    else:
        user_id = decoded_token.get('identity', {}).get('_id')
        location = 'users/{}'.format(user_id)

    resp = redirect(location='/webui/{}'.format(location), code=302)
    resp.set_cookie('access_token_cookie', value=access_token)
    resp.set_cookie('refresh_token_cookie', value=refresh_token)
    return resp
