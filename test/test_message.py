import unittest
import requests

import argparse
import logging
import json


class single_message_test(unittest.TestCase):

    def setUp(self):
        headers = {'Content-type': 'application/json'}
        data = {"username": "admin", "password": "admin"}
        login_response = requests.post('http://0.0.0.0:5000/api/user-login', headers=headers, data=json.dumps(data))

        self.auth_cookies={'access_token_cookie':login_response.cookies.get('access_token_cookie'),
         'refresh_token_cookie':login_response.cookies.get('refresh_token_cookie')}
       
        response = requests.get('http://0.0.0.0:5000/api/users', cookies=self.auth_cookies)
        users = response.json().get('users', [])
        self.ids = [user.get('_id') for user in users]

        headers = {'Content-type': 'application/json'}
  
        data = {
                    "message" : "TestMessage",
                    "sender" :"Sender",
                    "users" : self.ids,
                    "type" : 'fnf',
                    "group_message" : "False"
                }
        response = requests.post('http://0.0.0.0:5000/api/messages',data = json.dumps(data), headers=headers, cookies=self.auth_cookies)
        
        self.test_id = response.json().get('message_id')



    def test_get_message(self):
        headers = {}

        response = requests.get('http://0.0.0.0:5000/api/messages/'+self.test_id, headers=headers, cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 200)

    def test_get_message_fail_no_auth(self):
        headers = {}

        response = requests.get('http://0.0.0.0:5000/api/messages/'+self.test_id, headers=headers)

        self.assertEqual(response.status_code, 401)
    
    """def test_get_message_fail_wrong_id(self):

        #Bug you can try to load non existent messages with webui as well. ends in error. 
        headers = {}

        response = requests.get('http://0.0.0.0:5000/api/messages/12332423123213213', headers=headers,cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 404)"""
    
    def test_delete_message_fail_no_auth(self):
        headers = {}

        response = requests.delete('http://0.0.0.0:5000/api/messages/'+self.test_id, headers=headers)

        self.assertEqual(response.status_code, 401)

    def test_delete_message(self):
        headers = {}

        response = requests.delete('http://0.0.0.0:5000/api/messages/'+self.test_id, headers=headers, cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 200)

    
    
    # BUG you can delete any id with response 200
    """def test_delete_message_fail_wrong_id(self):
        headers = {}

        response = requests.delete('http://0.0.0.0:5000/api/messages/12332423123sdfsdfsdf213213', headers=headers, cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 200)"""
    

    

if __name__ == '__main__':
    unittest.main()