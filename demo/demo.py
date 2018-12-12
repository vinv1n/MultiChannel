import pprint
import requests

url = 'http://127.0.0.1:5000'


def create_user(username, pref):
    return {
        "username": username,
        "password": "secrut",
        "preferred_channel": pref,
        "channels": {
            "email": {"address": "adderss@server.fi"},
            "facebook": {"user_id": '{}_fb_id'.format(username)},
            "telegram": {"user_id": username},
            "irc": {"nickname": 'irc_{}'.format(username), "network": 'network_{}'.format(username)},
            "slack": {"channel": 'slack_{}'.format(username), "username": 'slack_username_{}'.format(username)},
        }
    }


user1 = create_user('user_1', 'email')
user2 = create_user('user_2', 'slack')

print('POST /users')
print('create user 1')
user1_r = requests.post(f'{url}/users', json=user1)
user1_id = user1_r.json().get('user_id')
print(user1_r.status_code, 'id:', user1_id)


print('create user 2')
user2_r = requests.post(f'{url}/users', json=user2)
user2_id = user2_r.json().get('user_id')
print(user1_r.status_code, 'id:', user2_id)


users = [user1_id, user2_id]
message = {
    'body': 'Hello!\nThe next meeting is on friday at 1700.\n-John Smith',
    'type':  'fnf',
    'group_message': False,
}
data = {
    'message': message,
    'users': users,
}
print('POST /messages')
post_msg = requests.post(f'{url}/messages', json=data)
msg_id = post_msg.json().get('message_id')
print('status:', post_msg.status_code)
print('message_id:', msg_id)

print(f'GET /messages/{msg_id}')
get_msg = requests.get(f'{url}/messages/{msg_id}')
print('status:', get_msg.status_code)
pprint.pprint(get_msg.json())
