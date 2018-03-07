import unittest
import os
import json
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(
  inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from app import create_app


class UserAuthTestCase(unittest.TestCase):
    
    """This class initializes the app with test data"""
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.app = self.app.test_client()
        self.app.post("/auth/register",
                    data=json.dumps(dict(email="jeff@gmail.com",username="jefftest",
                                password="jeffpass")), content_type="application/json")

        self.app.post("/auth/login",
                        data=json.dumps(dict(email="jeff@gmail.com",password="jeffpass")),
                                         content_type="application/json")

    def test_user_registration(self):
        """ Test API can register a user"""
        response = self.app.post("/auth/register",
                        data=json.dumps(dict(email="jeff2@gmail.com",username="jefftest2",
                            password="jeffpass2")), content_type="application/json")

        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("created", response_msg["message"])


    def test_user_already_registered(self):
        """ Test API can check a registered user"""
        response = self.app.post("/auth/register",
                        data=json.dumps(dict(email="jeff@gmail.com",username="jefftest",
                            password="jeffpass")), content_type="application/json")

        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("instead", response_msg["message"])


    def test_user_login(self):
        """ Test API can login a user"""
        response = self.app.post("/auth/login",
                        data=json.dumps(dict(email="jeff@gmail.com",password="jeffpass")),
                                         content_type="application/json")

        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("valid", response_msg["message"])  


    def test_user_login_with_wrong_password_or_username(self):
        """ Test API can check if user used wrong password"""
        response = self.app.post("/auth/login",
                        data=json.dumps(dict(email="jeff@gmail.com",password="jeffpassxxx")),
                                         content_type="application/json")

        self.assertEqual(response.status_code, 403)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Wrong", response_msg["message"])      

    def test_check_user_is_registrerd(self):
        """ Test API can check if user is registered"""
        response = self.app.post("/auth/login",
                        data=json.dumps(dict(email="jeffnot@gmail.com",password="jeffpassnot")),
                                         content_type="application/json")

        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Not registered", response_msg["message"]) 

    def test_if_user_has_logged_out(self):
        """ Test API can check if user is logged out"""
        response = self.app.get("/auth/logout")
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("logged out", response_msg["message"])


if __name__ == "__main__":
   unittest.main()