import logging
import requests
from flask import render_template, request, make_response, redirect
from app.views.utils import URL

logger = logging.getLogger(__name__)


def refresh_login():
    response = requests.post('{}/re-login'.format(URL), cookies=request.cookies, verify=False)

    #Hack to forward cookies to browser.
    msg = 'Status: {}'.format(response.status_code)
    resp = make_response(render_template('home.html'))
    resp.set_cookie('access_token_cookie', value=response.cookies.get('access_token_cookie'))
    return resp