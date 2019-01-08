import logging
import requests
from flask import render_template, request, make_response
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


    #Hack to forward cookies to browser.
    msg = 'Status: {}'.format(response.status_code)
    resp = make_response(render_template('response.html',msg=msg))
    resp.set_cookie('access_token_cookie', value=response.cookies.get('access_token_cookie'))
    resp.set_cookie('refresh_token_cookie', value=response.cookies.get('refresh_token_cookie'))
    return resp

