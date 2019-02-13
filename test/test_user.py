import unittest
import requests

import argparse
import logging
import json
import random, string

URL = 'http://127.0.0.1:5000/api'

def randomname(length):
   chars = string.ascii_lowercase
   return ''.join(random.choice(chars) for i in range(length))


class get_user_test(unittest.TestCase):

    def setUp(self):
        print("----------Running get_user_test----------")
        headers = {"Content-type": "application/json"}
        data = {"username": "admin", "password": "admin"}
        login_response = requests.post(URL+"/user-login", headers=headers, data=json.dumps(data))

        self.auth_cookies={"access_token_cookie":login_response.cookies.get("access_token_cookie"),
        "refresh_token_cookie":login_response.cookies.get("refresh_token_cookie")}

        response = requests.get(URL+"/users", cookies=self.auth_cookies)
        users = response.json().get('users')
        self.user_id = users[0]['_id']


    def test_get_user(self):

        response = requests.get(URL+"/users/"+self.user_id, cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 200)

    def test_get_user_fail_id(self):
        response = requests.get(URL+"/users/"+self.user_id+"1", cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)

    def test_get_user_fail_no_atuh(self):
        response = requests.get(URL+"/users/"+self.user_id,)

        self.assertEqual(response.status_code, 401)

class delete_user_test(unittest.TestCase):

    def setUp(self):
        print("----------Running delete_users_test----------")
        headers = {"Content-type": "application/json"}
        data = {"username": "admin", "password": "admin"}
        login_response = requests.post(URL+"/user-login", headers=headers, data=json.dumps(data))

        self.auth_cookies={"access_token_cookie":login_response.cookies.get("access_token_cookie"),
        "refresh_token_cookie":login_response.cookies.get("refresh_token_cookie")}
      
        headers = {"Content-Type": "application/json",}
        data = {
                "username": randomname(10),
                "password":"password",
                "preferred_channel":"email",
                "channels":{ 
                        "email": {
                            "address":"test@testi.testi"},
                        "telegram": {
                            "user_id": "testi"},
                        "irc": {
                            "nickname":"testi",
                            "network":"testi"}
                }
        }
        response = requests.post(URL+"/users", headers=headers, data=json.dumps(data))
        
        response = requests.get(URL+"/users", cookies=self.auth_cookies)
        users = response.json().get('users')
        self.user_id = users[1]['_id']


    def test_delete_user_fail_no_auth(self):
        response = requests.delete(URL+"/users/"+self.user_id)

        self.assertEqual(response.status_code, 401)

    def test_delete_user_bad_id(self):
        response = requests.delete(URL+"/users/"+self.user_id+"1", cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)

    def test_delete_user(self):
        response = requests.delete(URL+"/users/"+self.user_id, cookies=self.auth_cookies)
        self.assertEqual(response.status_code, 200)

        get_response = requests.get(URL+"/users/"+self.user_id, cookies=self.auth_cookies)
        self.assertEqual(get_response.status_code, 400)



class patch_user_test(unittest.TestCase):

    def setUp(self):
        print("----------Running patch_users_test----------")
        headers = {"Content-type": "application/json"}
        data = {"username": "admin", "password": "admin"}
        login_response = requests.post(URL+"/user-login", headers=headers, data=json.dumps(data))

        self.auth_cookies={"access_token_cookie":login_response.cookies.get("access_token_cookie"),
        "refresh_token_cookie":login_response.cookies.get("refresh_token_cookie")}
      
        response = requests.get(URL+"/users", cookies=self.auth_cookies)
        users = response.json().get('users')
        self.user_id = users[0]['_id']
        self.user = users[0]


    def test_patch_user_fail_no_auth(self):
        headers = {"Content-type": "application/json"}
        response = requests.patch(URL+"/users/"+self.user_id,headers=headers, data=json.dumps(self.user))

        self.assertEqual(response.status_code, 401)

    def test_patch_user_fail_no_data(self):
        headers = {"Content-type": "application/json"}
        response = requests.patch(URL+"/users/"+self.user_id,headers=headers,cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)

    def test_patch_user_fail_username(self):
        headers = {"Content-type": "application/json"}
        data = {
                "username": randomname(10),
                "password":"password",
                "preferred_channel":"email",
                "channels":{ 
                        "email": {
                            "address":"test@testi.testi"},
                        "telegram": {
                            "user_id": "testi"},
                        "irc": {
                            "nickname":"testi",
                            "network":"testi"}
                }
        }
        response = requests.patch(URL+"/users/"+self.user_id,headers=headers,data=json.dumps(data),cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)

    def test_patch_user_fail_extra(self):
        headers = {"Content-type": "application/json"}
        data = {
                "password":"password",
                "preferred_channel":"email",
                "channels":{ 
                        "email": {
                            "address":"test@testi.testi"},
                        "telegram": {
                            "user_id": "testi"},
                        "irc": {
                            "nickname":"testi",
                            "network":"testi"}
                }
        }
        data['extra'] = 'extra'
        response = requests.patch(URL+"/users/"+self.user_id,headers=headers,data=json.dumps(data),cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)


    def test_patch_user_fail_password_short(self):
        headers = {"Content-type": "application/json"}
        data = {
                "password":"password",
                "preferred_channel":"email",
                "channels":{ 
                        "email": {
                            "address":"test@testi.testi"},
                        "telegram": {
                            "user_id": "testi"},
                        "irc": {
                            "nickname":"testi",
                            "network":"testi"}
                }
        }
        data['password'] = "s"

        response = requests.patch(URL+"/users/"+self.user_id,headers=headers,data=json.dumps(data),cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)

    def test_patch_user_fail_password_long(self):
        headers = {"Content-type": "application/json"}
        data = {
                "password":"password",
                "preferred_channel":"email",
                "channels":{ 
                        "email": {
                            "address":"test@testi.testi"},
                        "telegram": {
                            "user_id": "testi"},
                        "irc": {
                            "nickname":"testi",
                            "network":"testi"}
                }
        }
        data['password'] = "aasdasdasdasdasdasdasdasdasdasdsadsasdasdsasdsadasdsasdasdasdasdasdsadasdasdssadsadasdassds"


        response = requests.patch(URL+"/users/"+self.user_id,headers=headers,data=json.dumps(data),cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)


    def test_patch_user_fail_preferred_wrong(self):
        headers = {"Content-type": "application/json"}
        data = {
                "password":"password",
                "preferred_channel":"email",
                "channels":{ 
                        "email": {
                            "address":"test@testi.testi"},
                        "telegram": {
                            "user_id": "testi"},
                        "irc": {
                            "nickname":"testi",
                            "network":"testi"}
                }
        }
        data['preferred_channel'] = "wrong"

        response = requests.patch(URL+"/users/"+self.user_id,headers=headers,data=json.dumps(data),cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)


    def test_patch_user_fail_no_email(self):
        headers = {"Content-type": "application/json"}
        data = {
                "password":"password",
                "preferred_channel":"email",
                "channels":{ 
                        "email": {
                            "address":"test@testi.testi"},
                        "telegram": {
                            "user_id": "testi"},
                        "irc": {
                            "nickname":"testi",
                            "network":"testi"}
                }
        }
        del data['channels']['email']

        response = requests.patch(URL+"/users/"+self.user_id,headers=headers,data=json.dumps(data),cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)


    def test_patch_user_fail_no_telegram(self):
        headers = {"Content-type": "application/json"}
        data = {
                "password":"password",
                "preferred_channel":"email",
                "channels":{ 
                        "email": {
                            "address":"test@testi.testi"},
                        "telegram": {
                            "user_id": "testi"},
                        "irc": {
                            "nickname":"testi",
                            "network":"testi"}
                }
        }
        del data['channels']['telegram']

        response = requests.patch(URL+"/users/"+self.user_id,headers=headers,data=json.dumps(data),cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)

    def test_patch_user_fail_no_irc(self):
        headers = {"Content-type": "application/json"}
        data = {
                "password":"password",
                "preferred_channel":"email",
                "channels":{ 
                        "email": {
                            "address":"test@testi.testi"},
                        "telegram": {
                            "user_id": "testi"},
                        "irc": {
                            "nickname":"testi",
                            "network":"testi"}
                }
        }
        del data['channels']['irc']

        response = requests.patch(URL+"/users/"+self.user_id,headers=headers,data=json.dumps(data),cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 400)

    def test_patch_user(self):
        headers = {"Content-type": "application/json"}
        data = {
                "password":"admin",
                "preferred_channel":"email",
                "channels":{ 
                        "email": {
                            "address":"Thishaschanged"},
                        "telegram": {
                            "user_id": "test"},
                        "irc": {
                            "nickname":"test",
                            "network":"testnetwork"},
                }
        }

        response = requests.patch(URL+"/users/"+self.user_id,headers=headers,data=json.dumps(data),cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 200)

        get_response = requests.get(URL+"/users/"+self.user_id,cookies=self.auth_cookies)
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json().get("User").get("preferred_channel"), data.get("preferred_channel"))
        self.assertEqual(get_response.json().get("User").get("channels"), data.get("channels"))





if __name__ == "__main__":
    unittest.main()