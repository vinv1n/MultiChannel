import logging
import requests
from flask import render_template, request
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
    logger.warning(request.form)
    password = request.form['password']
    name = request.form['name']
    data = {'password': password, 'username': name}
    response = requests.post('{}/user-login'.format(URL), json=data)

    msg = 'Status: {}'.format(response.status_code)
    return render_template(
        'response.html',
        msg=msg,
    )
