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
       
       
       
        return _user_info_base(
            request = request,
            method='PATCH',
            user_id=user_id,
            page=_user_info_page,
            json_data=_patch_html_parser(request.form),
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
    
    if method == 'GET':
        response = requests.get('{}/users/{}'.format(URL, user_id), cookies=request.cookies)
        if response.status_code != 200:
            abort(response.status_code)
    if method == 'PATCH':
        response_patch = requests.patch('{}/users/{}'.format(URL, user_id), json=json_data, cookies=request.cookies)
        if response_patch.status_code != 200:
            return render_template(
                'response.html',
                msg=response_patch.status_code
                )
        response = requests.get('{}/users/{}'.format(URL, user_id), cookies=request.cookies)
    

    return page(response)


def _user_info_page(response):
    json_data = response.json()

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


def _user_not_found():
    return render_template(
        'response.html',
        msg='Could not find user.',
    )

def _patch_html_parser(form):
    form_dict = form.to_dict(flat=False)
    user_data = {
    }

    """if form_dict['preferred_channel'][0] != "":
        user_data["preferred_channel"] = form_dict['preferred_channel'][0]
    if form_dict['password'][0] != "" and form_dict['con_pass'][0] == form_dict['password'][0]:
        user_data["password"] = form_dict['password'][0]
    if form_dict['admin'][0] == "True":
        user_data["admin"] = form_dict['admin'][0]"""

    for key in form_dict:
        if form_dict[key][0] != "":
            user_data[key] = form_dict[key][0]
        else:
            pass

    logger.warning(user_data)
    
    
  

    

    return user_data
