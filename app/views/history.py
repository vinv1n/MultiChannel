import logging
import requests
from flask import render_template, request
from app.views.utils import URL

logger = logging.getLogger(__name__)


def history():
    response = requests.get('{}/messages'.format(URL), cookies=request.cookies)

    if response.status_code != 200:
        return render_template(
            'response.html',
            msg='Could not retrieve messages {}'.format(response.status_code),
        )


    messages = response.json().get('messages', [])

    return render_template(
        'history.html',
        messages=messages,
    )