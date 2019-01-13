import logging
import requests
from flask import render_template, request, make_response, redirect
from app.views.utils import URL

logger = logging.getLogger(__name__)

def logout_both():

    response = requests.post('{}/logout'.format(URL), cookies=request.cookies)
    response_2 = requests.post('{}/re-logout'.format(URL), cookies=request.cookies)

    msg = 'Status: {}'.format(response.status_code)
    resp = make_response(render_template('logout.html',msg=msg))
    return resp
