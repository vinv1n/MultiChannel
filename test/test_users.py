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




class get_users_test(unittest.TestCase):

    def setUp(self):
        print("----------Running get_users_test----------")
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
        print("----------Running create_users_test----------")
        headers = {'Content-type': 'application/json'}
        data = {"username": "admin", "password": "admin"}
        login_response = requests.post(URL+'/user-login', headers=headers, data=json.dumps(data))

        self.auth_cookies={'access_token_cookie':login_response.cookies.get('access_token_cookie'),
         'refresh_token_cookie':login_response.cookies.get('refresh_token_cookie')}
    
    def test_create_user(self):
        headers = {"Content-Type": "application/json",}

        username = randomname(10)
        data = {
                "username": username,
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
        del data['username']

       
        response = requests.post(URL+"/users", headers=headers,data=json.dumps(data))        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_no_password(self):

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
        del data['password']

        response = requests.post(URL+"/users", headers=headers,data=json.dumps(data))        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_no_preferred(self):

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
        del data['preferred_channel']
       
        response = requests.post(URL+"/users", headers=headers,data=json.dumps(data))        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_no_channels(self):

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
        del data['channels']
       
        response = requests.post(URL+"/users", headers=headers,data=json.dumps(data))        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_no_email(self):

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
        del data['channels']['email']
       
        response = requests.post(URL+"/users", headers=headers,data=json.dumps(data))        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_no_email_address(self):

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
        del data['channels']['email']['address']
       
        response = requests.post(URL+"/users", headers=headers,data=json.dumps(data))        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_no_telegram(self):

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
        del data['channels']['telegram']
       
        response = requests.post(URL+"/users", headers=headers,data=json.dumps(data))        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_no_telegram_id(self):

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
        del data['channels']['telegram']['user_id']
       
        response = requests.post(URL+"/users", headers=headers,data=json.dumps(data))        

        self.assertEqual(response.status_code, 400)


    def test_create_user_fail_no_irc(self):

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
        del data['channels']['irc']
       
        response = requests.post(URL+"/users", headers=headers,data=json.dumps(data))        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_no_irc_nickname(self):

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
        del data['channels']['irc']['nickname']
       
        response = requests.post(URL+"/users", headers=headers,data=json.dumps(data))        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_no_network(self):

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
        del data['channels']['irc']['network']
       
        response = requests.post(URL+"/users", headers=headers,data=json.dumps(data))        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_short_name(self):

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
        data['usernmae'] = 's'
       
        response = requests.post(URL+"/users", headers=headers,data=json.dumps(data))        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_long_name(self):

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
        data['usernmae'] = 'Testuser32323adsadasdasdasd123123fsdfsdfdsffsf21332123'
       
        response = requests.post(URL+"/users", headers=headers,data=json.dumps(data))        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_short_password(self):

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
        data['password'] = 's'
       
        response = requests.post(URL+"/users", headers=headers,data=json.dumps(data))        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_long_password(self):

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
        data['password'] = 'Testuser32323adsadasdasdasd123123fsdfsdfdsffsf21332123asdasdsadasdsawqewqewq213213213eaffvxcvxcvxcvxcdsfsfgfdhdfhdfhgdfg3423432432sdfsdfsdfdsf'
       
        response = requests.post(URL+"/users", headers=headers,data=json.dumps(data))        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_extra(self):

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
        data['extra'] = 'extra'
 
        response = requests.post(URL+"/users", headers=headers,data=json.dumps(data))        

        self.assertEqual(response.status_code, 400)

    def test_create_user_fail_wrong_preferred(self):

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
        data['preferred_channel'] = 'this is wrong'
       
        response = requests.post(URL+"/users", headers=headers,data=json.dumps(data))        

        self.assertEqual(response.status_code, 400)


    def test_create_user_same_name(self):

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
        data['username'] = 'admin'
 
        response = requests.post(URL+"/users", headers=headers,data=json.dumps(data))       

        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()