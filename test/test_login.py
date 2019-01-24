import unittest
import requests

import argparse
import logging
import json


class Login_test(unittest.TestCase):


    def test_login_success(self):
        headers = {'Content-type': 'application/json'}
        data = {"username": "admin", "password": "admin"}
        response = requests.post('http://0.0.0.0:5000/api/user-login', headers=headers, data=json.dumps(data))

        self.assertEqual(response.status_code, 200)

    def test_login_bad_username (self):
        headers = {'Content-type': 'application/json'}
        data = {"username": "bad_username", "password": "admin"}
        response = requests.post('http://0.0.0.0:5000/api/user-login', headers=headers, data=json.dumps(data))

        self.assertEqual(response.status_code, 401)
    
    def test_login_bad_password(self):
        headers = {'Content-type': 'application/json'}
        data = {"username": "admin", "password": "wrongpassword"}
        response = requests.post('http://0.0.0.0:5000/api/user-login', headers=headers, data=json.dumps(data))

        self.assertEqual(response.status_code, 401)

    def test_login_empty_fields(self):
        headers = {'Content-type': 'application/json'}
        data = {"username": "", "password": ""}
        response = requests.post('http://0.0.0.0:5000/api/user-login', headers=headers, data=json.dumps(data))

        self.assertEqual(response.status_code, 401)
    
    def test_login_missing_password(self):
        headers = {'Content-type': 'application/json'}
        data = {"username": "admin", }
        response = requests.post('http://0.0.0.0:5000/api/user-login', headers=headers, data=json.dumps(data))

        self.assertEqual(response.status_code, 400)
    
    def test_login_missing_username(self):
        headers = {'Content-type': 'application/json'}
        data = {"password": "admin", }
        response = requests.post('http://0.0.0.0:5000/api/user-login', headers=headers, data=json.dumps(data))

        self.assertEqual(response.status_code, 400)

    def test_login_extra_field(self):
        headers = {'Content-type': 'application/json'}
        data = {"password": "admin", "username" : "admin", "extra" : "extra" }
        response = requests.post('http://0.0.0.0:5000/api/user-login', headers=headers, data=json.dumps(data))

        self.assertEqual(response.status_code, 400)

    def test_login_missing_data(self):
        headers = {'Content-type': 'application/json'}
        response = requests.post('http://0.0.0.0:5000/api/user-login', headers=headers)

        self.assertEqual(response.status_code, 400)

    def test_login_bad_header(self):
        data = {"username": "admin", "password": "admin"}
        response = requests.post('http://0.0.0.0:5000/api/user-login', data=json.dumps(data))

        self.assertEqual(response.status_code, 400)
    
    def test_return_cookies(self):
        headers = {'Content-type': 'application/json'}
        data = {"username": "admin", "password": "admin"}
        response = requests.post('http://0.0.0.0:5000/api/user-login', headers=headers, data=json.dumps(data))

        self.assertTrue(response.cookies.get('access_token_cookie'))
        self.assertTrue(response.cookies.get('refresh_token_cookie'))

class Logout_test(unittest.TestCase):

    def test_logout(self):
        headers = {'Content-type': 'application/json'}
        data = {"username": "admin", "password": "admin"}
        login_response = requests.post('http://0.0.0.0:5000/api/user-login', headers=headers, data=json.dumps(data))

        response = requests.post('http://0.0.0.0:5000/api/logout',
        cookies={'access_token_cookie':login_response.cookies.get('access_token_cookie'),
         'refresh_token_cookie':login_response.cookies.get('refresh_token_cookie')})

        self.assertEqual(response.status_code, 200)

    def test_logout_no_token(self):
        headers = {'Content-type': 'application/json'}
        data = {"username": "admin", "password": "admin"}
        login_response = requests.post('http://0.0.0.0:5000/api/user-login', headers=headers, data=json.dumps(data))

        response = requests.post('http://0.0.0.0:5000/api/logout')

        self.assertEqual(response.status_code, 401)


class LoginRefresh_test(unittest.TestCase):

    def test_refresh_no_cookies(self):

        response = requests.post('http://0.0.0.0:5000/api/re-login')

        self.assertEqual(response.status_code, 401)
    
    
    def test_refresh(self):
        headers = {'Content-type': 'application/json'}
        data = {"username": "admin", "password": "admin"}
        login_response = requests.post('http://0.0.0.0:5000/api/user-login', headers=headers, data=json.dumps(data))

        
        response = requests.post('http://0.0.0.0:5000/api/re-login',
         cookies={'access_token_cookie':login_response.cookies.get('access_token_cookie'),
         'refresh_token_cookie':login_response.cookies.get('refresh_token_cookie')})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.cookies.get('access_token_cookie'))


class LogoutRefresh_test(unittest.TestCase):

    def test_logoutRefresh(self):
        headers = {'Content-type': 'application/json'}
        data = {"username": "admin", "password": "admin"}
        login_response = requests.post('http://0.0.0.0:5000/api/user-login', headers=headers, data=json.dumps(data))

        response = requests.post('http://0.0.0.0:5000/api/re-logout',
        cookies={'access_token_cookie':login_response.cookies.get('access_token_cookie'),
         'refresh_token_cookie':login_response.cookies.get('refresh_token_cookie')})

        self.assertEqual(response.status_code, 200)

    def test_logoutRefresh_no_token(self):
        headers = {'Content-type': 'application/json'}
        data = {"username": "admin", "password": "admin"}
        login_response = requests.post('http://0.0.0.0:5000/api/user-login', headers=headers, data=json.dumps(data))

        response = requests.post('http://0.0.0.0:5000/api/re-logout')

        self.assertEqual(response.status_code, 401)



if __name__ == '__main__':
    unittest.main()
