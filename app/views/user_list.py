import logging
import requests
from flask import render_template, request
from app.views.utils import URL

logger = logging.getLogger(__name__)


def user_list():
    response = requests.get('{}/users'.format(URL), cookies=request.cookies)

    if response.status_code != 200:
        return render_template(
            'response.html',
            msg='Could not retrieve users {}'.format(response.status_code),
        )


    users = response.json().get('users', [])

    return render_template(
        'user_list.html',
        users=users,
    )