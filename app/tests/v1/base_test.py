"""Authenticate a user, admin and an admin to be used during testing
Set up required items to be used during testing
"""
# pylint: disable=W0612
import unittest
import json
from werkzeug.security import generate_password_hash

import sys # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app
from app.api.v1.models import users, parcels


class BaseTests(unittest.TestCase):
    """Authenticate a user and an admin and make the tokens available. Create a parcel and request"""


    def setUp(self):
        self.application = app.create_app('instance.config.TestingConfig')
        user_reg = json.dumps({
            "username" : "user",
            "email" : "user@gmail.com",
            "password" : "12345678",
            "confirm" : "12345678"})

        admin_reg = json.dumps({
            "username" : "admin1",
            "email" : "admin1@gmail.com",
            "password" : "123456789",
            "confirm" : "123456789"})
        
        admin_reg2 = json.dumps({
            "username" : "admin2",
            "email" : "admin2@gmail.com",
            "password" : "123456789",
            "confirm" : "123456789"})

        self.user_log = json.dumps({
            "email" : "user@gmail.com",
            "password" : "12345678"})

        self.admin_log1 = json.dumps({
            "email" : "admin1@gmail.com",
            "password" : "123456789"})
        
        self.admin_log2 = json.dumps({
            "email" : "admin2@gmail.com",
            "password" : "123456789"})

        self.admin_log = json.dumps({
            "email" : "admin@gmail.com",
            "password" : "admin234"})

        self.app = self.application.test_client()

        
        register_user = self.app.post(
            '/api/v1/auth/user-register', data=user_reg,
            content_type='application/json')
        register_admin = self.app.post(
            '/api/v1/auth/admin-register', data=admin_reg,
            content_type='application/json')
        
        register_admin = self.app.post(
            '/api/v1/auth/admin-register', data=admin_reg2,
            content_type='application/json')
        
        admin_result = self.app.post(
            '/api/v1/auth/login', data=self.admin_log1,
            content_type='application/json')
        
        admin_response = json.loads(admin_result.get_data(as_text=True))
        admin_token = admin_response["token"]
        self.admin_header = {"Content-Type" : "application/json", "x-access-token" : admin_token}

        admin_result = self.app.post(
            '/api/v1/auth/login', data=self.admin_log,
            content_type='application/json')

        admin_response = json.loads(admin_result.get_data(as_text=True))
        admin_token = admin_response["token"]
        self.admin_header = {"Content-Type" : "application/json", "x-access-token" : admin_token}

        admin_result2 = self.app.post(
            '/api/v1/auth/login', data=self.admin_log2,
            content_type='application/json')

        admin_response2 = json.loads(admin_result2.get_data(as_text=True))
        admin_token2 = admin_response2["token"]
        self.admin_header2 = {"Content-Type" : "application/json", "x-access-token" : admin_token2}
        
        user_result = self.app.post(
            '/api/v1/auth/login', data=self.user_log,
            content_type='application/json')

        user_response = json.loads(user_result.get_data(as_text=True))
        user_token = user_response["token"]
        self.user_header = {"Content-Type" : "application/json", "x-access-token" : user_token}

        parcel = json.dumps({"pickup_location" : "Syokimau", "destination_location" : "Nairobi",
         "date_ordered" : "16/04/2015 1400HRS", "price" : "400", "max" : "2"})

        parcel2 = json.dumps({"pickup_location" : "Syokimau2", "destination_location" : "Nairobi2",
         "date_ordered" : "16/04/2015 1400HRS", "price" : "400", "max" : "2"})

        create_parcel = self.app.post(
            '/api/v1/parcels', data=parcel, content_type='application/json',
            headers=self.admin_header)

        create_parcel2 = self.app.post(
            '/api/v1/parcels', data=parcel2, content_type='application/json',
            headers=self.admin_header)

        requestparcel = self.app.post(
            '/api/v1/parcels/1/cancels',
            headers=self.user_header)
        
        requestparcel = self.app.post(
            '/api/v1/parcels/2/cancels',
            headers=self.user_header)
    
    def tearDown(self):
        with self.application.app_context():

            users.all_users = { 1 : {"id": "1", "username" : "admin",
            "email" : "admin@gmail.com", "password" : generate_password_hash("admin234", method='sha256'), "usertype" : "admin",
            },}
            users.user_count = 2

            parcels.all_parcels = {}
            parcels.parcel_count = 1

            parcels.all_cancels = {}
            parcels.request_count = 1