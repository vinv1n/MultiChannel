import logging
import requests
from flask import render_template, request


URL = 'http://127.0.0.1:5000'
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
    data = {'password': password, 'name': name}
    response = requests.post('{}/login'.format(URL), json=data)
