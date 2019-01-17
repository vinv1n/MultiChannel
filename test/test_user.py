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

class patch_user_test(unittest.TestCase):

    def setUp(self):
        headers = {"Content-type": "application/json"}
        data = {"username": "admin", "password": "admin"}
        login_response = requests.post("http://0.0.0.0:5000/api/user-login", headers=headers, data=json.dumps(data))

        self.auth_cookies={"access_token_cookie":login_response.cookies.get("access_token_cookie"),
        "refresh_token_cookie":login_response.cookies.get("refresh_token_cookie")}
      
        response = requests.get("http://0.0.0.0:5000/api/users", cookies=self.auth_cookies)
        users = response.json().get('users')
        self.user_id = users[0]['_id']
        self.user = users[0]


    def test_patch_user_fail_no_auth(self):
        headers = {"Content-type": "application/json"}
        response = requests.patch("http://0.0.0.0:5000/api/users/"+self.user_id,headers=headers, data=json.dumps(self.user))

        self.assertEqual(response.status_code, 401)

    def test_patch_user_fail_no_data(self):
        headers = {"Content-type": "application/json"}
        response = requests.patch("http://0.0.0.0:5000/api/users/"+self.user_id,headers=headers,cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)

    def test_patch_user_fail_username(self):
        headers = {"Content-type": "application/json"}
        data = {
                "username":"userdelete",
                "password":"admin",
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

        response = requests.patch("http://0.0.0.0:5000/api/users/"+self.user_id,headers=headers,data=json.dumps(data),cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)

    def test_patch_user_fail_extra(self):
        headers = {"Content-type": "application/json"}
        data = {
                "extra" : "extra",
                "password":"admin",
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

        response = requests.patch("http://0.0.0.0:5000/api/users/"+self.user_id,headers=headers,data=json.dumps(data),cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)


    def test_patch_user_fail_password_short(self):
        headers = {"Content-type": "application/json"}
        data = {
                "password":"a",
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

        response = requests.patch("http://0.0.0.0:5000/api/users/"+self.user_id,headers=headers,data=json.dumps(data),cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)

    def test_patch_user_fail_password_long(self):
        headers = {"Content-type": "application/json"}
        data = {
                "password":"aasdasdasdasdasdasdasdasdasdasdsadsasdasdsasdsadasdsasdasdasdasdasdsadasdasdssadsadasdassds",
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

        response = requests.patch("http://0.0.0.0:5000/api/users/"+self.user_id,headers=headers,data=json.dumps(data),cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)


    def test_patch_user_fail_preferred_wrong(self):
        headers = {"Content-type": "application/json"}
        data = {
                "password":"admin",
                "preferred_channel":"thisiswrong",
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

        response = requests.patch("http://0.0.0.0:5000/api/users/"+self.user_id,headers=headers,data=json.dumps(data),cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)


    def test_patch_user_fail_no_email(self):
        headers = {"Content-type": "application/json"}
        data = {
                "password":"a",
                #"preferred_channel":"email",
                "channels":{ 
                        "email": {},
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

        response = requests.patch("http://0.0.0.0:5000/api/users/"+self.user_id,headers=headers,data=json.dumps(data),cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)

    def test_patch_user_fail_no_facebook(self):
        headers = {"Content-type": "application/json"}
        data = {
                "password":"admin",
                "preferred_channel":"email",
                "channels":{ 
                        "email": {
                            "address":"test@test.test"},
                        "facebook": {},
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

        response = requests.patch("http://0.0.0.0:5000/api/users/"+self.user_id,headers=headers,data=json.dumps(data),cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)

    def test_patch_user_fail_no_telegram(self):
        headers = {"Content-type": "application/json"}
        data = {
                "password":"admin",
                "preferred_channel":"email",
                "channels":{ 
                        "email": {
                            "address":"test@test.test"},
                        "facebook": {
                            "user_id": "test"},
                        "telegram": {},
                        "irc": {
                            "nickname":"test",
                            "network":"testnetwork"},
                        "slack": {
                            "username":"test",
                            "channel":"testchannel"}
                }
        }

        response = requests.patch("http://0.0.0.0:5000/api/users/"+self.user_id,headers=headers,data=json.dumps(data),cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)

    def test_patch_user_fail_no_irc(self):
        headers = {"Content-type": "application/json"}
        data = {
                "password":"admin",
                "preferred_channel":"email",
                "channels":{ 
                        "email": {
                            "address":"test@test.test"},
                        "facebook": {
                            "user_id": "test"},
                        "telegram": {
                            "user_id": "test"},
                        "irc": {},
                        "slack": {
                            "username":"test",
                            "channel":"testchannel"}
                }
        }

        response = requests.patch("http://0.0.0.0:5000/api/users/"+self.user_id,headers=headers,data=json.dumps(data),cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)

    def test_patch_user_fail_no_slack(self):
        headers = {"Content-type": "application/json"}
        data = {
                "password":"admin",
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
                        "slack": {}
                }
        }

        response = requests.patch("http://0.0.0.0:5000/api/users/"+self.user_id,headers=headers,data=json.dumps(data),cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)

    def test_patch_user(self):
        headers = {"Content-type": "application/json"}
        data = {
                "password":"admin",
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

        response = requests.patch("http://0.0.0.0:5000/api/users/"+self.user_id,headers=headers,data=json.dumps(data),cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 200)



if __name__ == "__main__":
    unittest.main()