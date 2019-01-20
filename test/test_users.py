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

class get_users_test(unittest.TestCase):

    def setUp(self):
        headers = {"Content-type": "application/json"}
        data = {"username": "admin", "password": "admin"}
        login_response = requests.post(URL+"/user-login", headers=headers, data=json.dumps(data))

        self.auth_cookies={"access_token_cookie":login_response.cookies.get("access_token_cookie"),
        "refresh_token_cookie":login_response.cookies.get("refresh_token_cookie")}
      
    def test_get_users(self):
        response = requests.get(URL+"/users", cookies=self.auth_cookies)

        self.assertEqual(response.status_code, 200)

    def test_get_users_fail_no_auth(self):
        response = requests.get(URL+"/users")

        self.assertEqual(response.status_code, 401)

class create_users_test(unittest.TestCase):

    def setUp(self):
        headers = {'Content-type': 'application/json'}
        data = {"username": "admin", "password": "admin"}
        login_response = requests.post(URL+'/user-login', headers=headers, data=json.dumps(data))

        self.auth_cookies={'access_token_cookie':login_response.cookies.get('access_token_cookie'),
         'refresh_token_cookie':login_response.cookies.get('refresh_token_cookie')}
    
    def test_create_user(self):
        headers = {"Content-Type": "application/json",}

        username = randomname(10)
        data = {
                "username":username,
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
        response = requests.post(URL+"/users", headers=headers, data=json.dumps(data))        
        self.assertEqual(response.status_code, 200)
        user_id = response.json().get('user_id')

        get_response = requests.get(URL+"/users/"+user_id, headers=headers, data=json.dumps(data), cookies=self.auth_cookies)
        self.assertEqual(get_response.status_code, 200)

        self.assertEqual(get_response.json().get("User").get("username"), username)
        self.assertEqual(get_response.json().get("User").get("preferred_channel"), data.get("preferred_channel"))
        self.assertEqual(get_response.json().get("User").get("channels"), data.get("channels"))






    def test_create_user_fail_no_data(self):

        headers = {"Content-Type": "application/json",}
        response = requests.post(URL+"/users", headers=headers,)        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_no_username(self):

        headers = {"Content-Type": "application/json",}
        data = {
                #"username":"Testuser",
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
       
        response = requests.post(URL+"/users", headers=headers,)        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_no_password(self):

        headers = {"Content-Type": "application/json",}
        data = {
                "username":"Testuser32323",
                #"password":"Testpassword",
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
       
        response = requests.post(URL+"/users", headers=headers,)        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_no_preferred(self):

        headers = {"Content-Type": "application/json",}
        data = {
                "username":"Testuser32323",
                "password":"Testpassword",
                #"preferred_channel":"email",
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
       
        response = requests.post(URL+"/users", headers=headers,)        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_no_channels(self):

        headers = {"Content-Type": "application/json",}
        data = {
                "username":"Testuser32323",
                "password":"Testpassword",
                "preferred_channel":"email",
        }
       
        response = requests.post(URL+"/users", headers=headers,)        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_no_email(self):

        headers = {"Content-Type": "application/json",}
        data = {
                "username":"Testuser32323",
                "password":"Testpassword",
                "preferred_channel":"email",
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
       
        response = requests.post(URL+"/users", headers=headers,)        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_no_facebook(self):

        headers = {"Content-Type": "application/json",}
        data = {
                "username":"Testuser32323",
                "password":"Testpassword",
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
       
        response = requests.post(URL+"/users", headers=headers,)        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_no_telegram(self):

        headers = {"Content-Type": "application/json",}
        data = {
                "username":"Testuser32323",
                "password":"Testpassword",
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
       
        response = requests.post(URL+"/users", headers=headers,)        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_no_irc(self):

        headers = {"Content-Type": "application/json",}
        data = {
                "username":"Testuser32323",
                "password":"Testpassword",
                #"preferred_channel":"email",
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
       
        response = requests.post(URL+"/users", headers=headers,)        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_no_slack(self):

        headers = {"Content-Type": "application/json",}
        data = {
                "username":"Testuser32323",
                "password":"Testpassword",
                #"preferred_channel":"email",
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
       
        response = requests.post(URL+"/users", headers=headers,)        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_short_name(self):

        headers = {"Content-Type": "application/json",}
        data = {
                "username":"T",
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
       
        response = requests.post(URL+"/users", headers=headers,)        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_long_name(self):

        headers = {"Content-Type": "application/json",}
        data = {
                "username":"Testuser32323adsadasdasdasd123123fsdfsdfdsffsf21332123",
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
       
        response = requests.post(URL+"/users", headers=headers,)        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_short_password(self):

        headers = {"Content-Type": "application/json",}
        data = {
                "username":"Testuser32323adsadasdasdasd123123fsdfsdfdsffsf21332123",
                "password":"T",
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
       
        response = requests.post(URL+"/users", headers=headers,)        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_long_password(self):

        headers = {"Content-Type": "application/json",}
        data = {
                "username":"Testuser32323adsadasdasdasd123123fsdfsdfdsffsf21332123",
                "password":"Testpasswordsdffrwefewfewfwvfxvxcvsdfsdfsdfsdfsdfsdvxcvxvsdfsdfcvhbdfgdfgwer34213123sfsgfdbvcbcvbvwerwe3243123123asd",
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
       
        response = requests.post(URL+"/users", headers=headers,)        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_extra(self):

        headers = {"Content-Type": "application/json",}
        data = {
                "extra": "extra",
                "username":"Testuser32323adsadasdasdasd123123fsdfsdfdsffsf21332123",
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
       
        response = requests.post(URL+"/users", headers=headers,)        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_wron_preferred(self):

        headers = {"Content-Type": "application/json",}
        data = {
                "username":"Testuser32323adsadasdasdasd123123fsdfsdfdsffsf21332123",
                "password":"Testpassword",
                "preferred_channel":"Thisiswrong",
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
       
        response = requests.post(URL+"/users", headers=headers,)        

        self.assertEqual(response.status_code, 400)


    def test_create_user_same_name(self):

        headers = {"Content-Type": "application/json",}
        data = {
                "username":"Testuser",
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
       
        response = requests.post(URL+"/users", headers=headers,)        

        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()