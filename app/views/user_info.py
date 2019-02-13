import logging
import requests

from flask import render_template, request, abort, flash, redirect
from app.views.utils import URL


logger = logging.getLogger(__name__)


def user_info(user_id):
    if request.method == 'POST':
        # HTML forms can only use methods POST and GET
        # Therefore, POST is used here in place of PATCH
        patching_data = _parse_patching_data(request.form.to_dict(flat=False))

        return _user_info_base(
            request=request,
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
            request=request,
            method='DELETE',
            user_id=user_id,
            page=_user_deleted,
        )

    else:

        return _user_info_base(
            request=request,
            method='GET',
            user_id=user_id,
            page=_user_info_page,
        )


def _user_info_base(request, method, user_id, page, json_data=None):
    response = requests.request(
        method=method,
        url='{}/users/{}'.format(URL, user_id),
        json=json_data,
        cookies=request.cookies,
        verify=False
    )

    if response.status_code not in [200, 304]:
        abort(response.status_code)

    return page(response, user_id)


def _user_info_page(response, user_id):
    json_data = response.json()

    _user_data = json_data.get('User', {})

    # User does not exist
    if _user_data is None:
        return _user_not_found()

    _channels = _user_data.get('channels', {})
    preferred_channel = _user_data.get('preferred_channel')

    user_information_kwargs = {
        'username': _user_data.get('username', ''),
        'admin': _user_data.get('admin', ''),
        'email': _channels.get('email', {}).get('address', ''),
        'irc_nick': _channels.get('irc', {}).get('nickname', ''),
        'irc_network': _channels.get('irc', {}).get('network', ''),
        'telegram_username': _channels.get('telegram', {}).get('user_id', ''),
        'pref_{}'.format(preferred_channel): 'checked',
    }

    logger.warning(user_information_kwargs)

    return render_template(
        'user_info.html',
        **user_information_kwargs,
    )


def _user_deleted(response, user_id):
    flash('user deleted!')
    return redirect('/webui/login')


def _parse_patching_data(patching_data):
    user_information = dict()
    channels = dict()

    channel_mapping = {
        'email':  {'email_address': 'address'},
        'telegram': {'telegram': 'user_id'},
        'irc': {'irc_nick': 'nickname', 'irc_network': 'network'},
    }

    for channel, mapping in channel_mapping.items():
        channels[channel] = {
            _to: patching_data.get(_from)[0]
            for _from, _to in mapping.items()
        }

    user_information['channels'] = channels

    # Logic for confirming password change
    password = patching_data.get('password')[0]
    password_confirm = patching_data.get('password')[0]
    if password and password == password_confirm:
        user_information['password'] = password

    preferred_channel = patching_data.get('preferred_channel', [''])[0]
    user_information['preferred_channel'] = preferred_channel
    return user_information


def _user_patched(response, user_id):
    if response.status_code == 304:
        flash('Changes submitted, no changes were done.')
    else:
        flash('Changes submitted.')
    return redirect('/webui/users/{}'.format(user_id))


def _user_not_found():
    return render_template(
        'response.html',
        msg='Could not find user.',
    )
