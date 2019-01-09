import logging
import requests
import json

from flask import render_template, request, abort
from app.views.utils import URL


logger = logging.getLogger(__name__)


def user_info(user_id):
    logger.warning('user_info method: {}'.format(request.method))
    logger.warning('{}'.format(request.args.get('delete_user')))

    if request.method == 'POST':
        # HTML forms can only use methods POST and GET
        # Therefore, POST is used here in place of PATCH
        patching_data = _parse_patching_data(request)

        return _user_info_base(
            request = request,
            method='PATCH',
            user_id=user_id,
            page=_user_patched,
            json_data=patching_data,
        )

    # HTML forms/buttons/links cannot send DELETE requests,
    # so deletion has to be handled using a different pattern.
    # The HTTP request here is GET, but the arg has delete_user set to TRUE
    elif request.args.get('delete_user') == 'TRUE':

        return _user_info_base(
            request = request,
            method='DELETE',
            user_id=user_id,
            page=_user_deleted,
        )

    else:

        return _user_info_base(
            request = request,
            method='GET',
            user_id=user_id,
            page=_user_info_page,
        )


def _user_info_base(request, method, user_id, page, json_data=None):
    
    response = requests.get('{}/users/{}'.format(URL, user_id), cookies=request.cookies)

    if response.status_code != 200:
        abort(response.status_code)

    return page(response)


def _user_info_page(response):
    json_data = response.json()
    logger.warning(json_data)

    _user_data = json_data.get('User', {})

    # User does not exist
    if _user_data is None:
        return _user_not_found()

    # hack
    _channels = _user_data.get('channels', {})

    username = _user_data.get('username', '')
    admin = _user_data.get('admin', '')
    email = _channels.get('email', {}).get('address', '')
    irc_nick = _channels.get('irc', {}).get('nickname', '')
    irc_network = _channels.get('irc', {}).get('network', '')
    slack_username = _channels.get('slack', {}).get('username', '')
    slack_channel = _channels.get('slack', {}).get('channel', '')
    telegram_username = _channels.get('telegram', {}).get('user_id', '')

    return render_template(
        'user_info.html',
        username=username,
        admin=admin,
        email=email,
        irc_nick=irc_nick,
        irc_network=irc_network,
        slack_username=slack_username,
        telegram_username=telegram_username,
    )


def _user_deleted(response):
    return render_template(
        'response.html',
        msg='user deleted!',
    )


def _parse_patching_data(response):
    json_data = response.json()


def _user_patched(response):
    pass

def _user_not_found():
    return render_template(
        'response.html',
        msg='Could not find user.',
    )
