import unittest
import requests

import argparse
import logging
import json

class get_user_test(unittest.TestCase):

    def setUp(self):
        headers = {"Content-type": "application/json"}
        data = {"username": "admin", "password": "admin"}
        login_response = requests.post("http://0.0.0.0:5000/api/user-login", headers=headers, data=json.dumps(data))

        self.auth_cookies={"access_token_cookie":login_response.cookies.get("access_token_cookie"),
        "refresh_token_cookie":login_response.cookies.get("refresh_token_cookie")}

        response = requests.get("http://0.0.0.0:5000/api/users", cookies=self.auth_cookies)
        users = response.json().get('users')
        self.user_id = users[0]['_id']


    def test_get_user(self):

        response = requests.get("http://0.0.0.0:5000/api/users/"+self.user_id, cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 200)

    def test_get_user_fail_id(self):
        response = requests.get("http://0.0.0.0:5000/api/users/"+self.user_id+"1", cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)

    def test_get_user_fail_no_atuh(self):
        response = requests.get("http://0.0.0.0:5000/api/users/"+self.user_id,)

        self.assertEqual(response.status_code, 401)

class delete_user_test(unittest.TestCase):

    def setUp(self):
        headers = {"Content-type": "application/json"}
        data = {"username": "admin", "password": "admin"}
        login_response = requests.post("http://0.0.0.0:5000/api/user-login", headers=headers, data=json.dumps(data))

        self.auth_cookies={"access_token_cookie":login_response.cookies.get("access_token_cookie"),
        "refresh_token_cookie":login_response.cookies.get("refresh_token_cookie")}
      
        data = {
                "username":"userdelete",
                "password":"Testpassword",
                "preferred_channel":"email",
                "channels":{ 
                        "email": {
                            "address":"test@test.test"},
                        "facebook": {
                            "user_id": "test"},
                        "telegram": {
                            "user_id": "test"},
                        "irc": {
                            "nickname":"test",
                            "network":"testnetwork"},
                        "slack": {
                            "username":"test",
                            "channel":"testchannel"}
                }
        }
        response = requests.post("http://0.0.0.0:5000/api/users", headers=headers, data=json.dumps(data))
        
        response = requests.get("http://0.0.0.0:5000/api/users", cookies=self.auth_cookies)
        users = response.json().get('users')
        self.user_id = users[1]['_id']


    def test_delete_user_fail_no_auth(self):
        response = requests.delete("http://0.0.0.0:5000/api/users/"+self.user_id)

        self.assertEqual(response.status_code, 401)

    def test_delete_user_bad_id(self):
        response = requests.delete("http://0.0.0.0:5000/api/users/"+self.user_id+"1", cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)

   
    def test_delete_user(self):
        response = requests.delete("http://0.0.0.0:5000/api/users/"+self.user_id, cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()