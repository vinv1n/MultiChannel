import unittest
import requests
import argparse
import logging
import json

URL = 'http://127.0.0.1:5000/api'

class get_messages_test(unittest.TestCase):

    def setUp(self):
        print("----------Running get_messages_test----------")
        headers = {'Content-type': 'application/json'}
        data = {"username": "admin", "password": "admin"}
        login_response = requests.post(URL+'/user-login', headers=headers, data=json.dumps(data))

        self.auth_cookies={'access_token_cookie':login_response.cookies.get('access_token_cookie'),
         'refresh_token_cookie':login_response.cookies.get('refresh_token_cookie')}

        response = requests.get(URL+'/users', cookies=self.auth_cookies)
        users = response.json().get('users', [])
        self.ids = [user.get('_id') for user in users]
      
    def test_get_messages(self):
        response = requests.get(URL+'/messages', cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 200)

    def test_get_messages_fail_no_auth(self):
        response = requests.get(URL+'/messages')

        self.assertEqual(response.status_code, 401)

class create_message_test(unittest.TestCase):

    def setUp(self):
        print("----------Running create_messages_test----------")
        headers = {'Content-type': 'application/json'}
        data = {"username": "admin", "password": "admin"}
        login_response = requests.post(URL+'/user-login', headers=headers, data=json.dumps(data))

        self.auth_cookies={'access_token_cookie':login_response.cookies.get('access_token_cookie'),
         'refresh_token_cookie':login_response.cookies.get('refresh_token_cookie')}

        response = requests.get(URL+'/users', cookies=self.auth_cookies)
        users = response.json().get('users', [])
        self.ids = [user.get('_id') for user in users]
         
    def test_create_message(self):
        headers = {'Content-type': 'application/json'}
  
        data = {
                    "message" : "TestMessage",
                    "sender" :"Sender",
                    "users" : self.ids,
                    "type" : 'fnf',
                    "group_message" : "False"
                }

        response = requests.post(URL+'/messages',data = json.dumps(data), headers=headers, cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 200)

        inserted_id = response.json().get('message_id')
    
        get_response = requests.get(URL+'/messages/'+inserted_id, headers=headers, cookies=self.auth_cookies)

        message_data = get_response.json().get('message')
        self.assertEqual(get_response.status_code, 200)

        self.assertAlmostEqual(data['message'], message_data['message'])
        self.assertAlmostEqual(data['group_message'], message_data['group_message'])
        self.assertAlmostEqual(data['type'], message_data['type'])

        
        self.assertEqual(response.status_code, 200)


    def test_create_message_fail_bad_headers(self):
        headers = {}
        data = {
                    "message" : "TestMessage",
                    "sender" :"Sender",
                    "users" : self.ids,
                    "type" : 'fnf',
                    "group_message" : "False"
                }
        response = requests.post(URL+'/messages',data = json.dumps(data), headers=headers, cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)

    def test_create_message_fail_extra(self):
        headers = {'Content-type': 'application/json'}
        data = {
                    "extra" : "extra",
                    "message" : "TestMessage",
                    "sender" :"Sender",
                    "users" : self.ids,
                    "type" : 'fnf',
                    "group_message" : "False"
                }
        response = requests.post(URL+'/messages',data = json.dumps(data), headers=headers, cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)

    def test_create_message_fail_no_message(self):
        headers = {'Content-type': 'application/json'}
        data = {
                    "sender" :"Sender",
                    "users" : self.ids,
                    "type" : 'fnf',
                    "group_message" : "False"
                }
        response = requests.post(URL+'/messages',data = json.dumps(data), headers=headers, cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)

    def test_create_message_fail_no_sender(self):
        headers = {'Content-type': 'application/json'}
        data = {
                    "message" : "TestMessage",
                    #"sender" :"Sender",
                    "users" : self.ids,
                    "type" : 'fnf',
                    "group_message" : "False"
                }
        response = requests.post(URL+'/messages',data = json.dumps(data), headers=headers, cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)

    def test_create_message_fail_no_users(self):
        headers = {'Content-type': 'application/json'}
        data = {
                    "message" : "TestMessage",
                    "sender" :"Sender",
                    #"users" : self.ids,
                    "type" : 'fnf',
                    "group_message" : "False"
                }
        response = requests.post(URL+'/messages',data = json.dumps(data), headers=headers, cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)

    def test_create_message_fail_no_type(self):
        headers = {'Content-type': 'application/json'}
        data = {
                    "message" : "TestMessage",
                    "sender" :"Sender",
                    "users" : self.ids,
                    #"type" : 'fnf',
                    "group_message" : "False"
                }
        response = requests.post(URL+'/messages',data = json.dumps(data), headers=headers, cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)

    def test_create_message_fail_no_group_message(self):
        headers = {'Content-type': 'application/json'}
        data = {
                    "message" : "TestMessage",
                    "sender" :"Sender",
                    "users" : self.ids,
                    "type" : 'fnf',
                    #"group_message" : "False"
                }
        response = requests.post(URL+'/messages',data = json.dumps(data), headers=headers, cookies=self.auth_cookies)
       

        self.assertEqual(response.status_code, 400)

    def test_create_message_fail_short_message(self):
        headers = {'Content-type': 'application/json'}
        data = {
                    "message" : "T",
                    "sender" :"Sender",
                    "users" : self.ids,
                    "type" : 'fnf',
                    "group_message" : "False"
                }
        response = requests.post(URL+'/messages',data = json.dumps(data), headers=headers, cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)
    
    def test_create_message_fail_long_message(self):
        headers = {'Content-type': 'application/json'}
        data = {
                    "message" : 1000*"a",
                    "sender" :"Sender",
                    "users" : self.ids,
                    "type" : 'fnf',
                    "group_message" : "False"
                }
        response = requests.post(URL+'/messages',data = json.dumps(data), headers=headers, cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)

    def test_create_message_fail_users_empty(self):
        headers = {'Content-type': 'application/json'}
        data = {
                    "message" : 1000*"a",
                    "sender" :"Sender",
                    "users" : [],
                    "type" : 'fnf',
                    "group_message" : "False"
                }
        response = requests.post(URL+'/messages',data = json.dumps(data), headers=headers, cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)

    def test_create_message_fail_sender_empty(self):
        headers = {'Content-type': 'application/json'}
        data = {
                    "message" : "TestMessage",
                    "sender" :"",
                    "users" : self.ids,
                    "type" : 'fnf',
                    "group_message" : "False"
                }
        response = requests.post(URL+'/messages',data = json.dumps(data), headers=headers, cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)

    def test_create_message_fail_sender_empty(self):
        headers = {'Content-type': 'application/json'}
        data = {
                    "message" : "TestMessage",
                    "sender" :"",
                    "users" : self.ids,
                    "type" : 'fnf',
                    "group_message" : "False"
                }
        response = requests.post(URL+'/messages',data = json.dumps(data), headers=headers, cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)

    def test_create_message_fail_type_empty(self):
        headers = {'Content-type': 'application/json'}
        data = {
                    "message" : "TestMessage",
                    "sender" :"",
                    "users" : self.ids,
                    "type" : "",
                    "group_message" : "False"
                }
        response = requests.post(URL+'/messages',data = json.dumps(data), headers=headers, cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)

    def test_create_message_fail_type_wrong(self):
        headers = {'Content-type': 'application/json'}
        data = {
                    "message" : "TestMessage",
                    "sender" :"",
                    "users" : self.ids,
                    "type" : "this is wrong",
                    "group_message" : "False"
                }
        response = requests.post(URL+'/messages',data = json.dumps(data), headers=headers, cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)
    
    def test_create_message_fail_group_message_wrong(self):
        headers = {'Content-type': 'application/json'}
        data = {
                    "message" : "TestMessage",
                    "sender" :"",
                    "users" : self.ids,
                    "type" : 'fnf',
                    "group_message" : "This is wrong"
                }
        response = requests.post(URL+'/messages',data = json.dumps(data), headers=headers, cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)

    def test_create_message_fail_no_auth(self):
        headers = {'Content-type': 'application/json'}
        data = {
                    "message" : "TestMessage",
                    "sender" :"",
                    "users" : self.ids,
                    "type" : 'fnf',
                    "group_message" : "False"
                }
        response = requests.post(URL+'/messages',data = json.dumps(data), headers=headers)

        self.assertEqual(response.status_code, 401)





if __name__ == '__main__':
    unittest.main()