"""Authenticate a user, adminU and an admin to be used during testing
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
from app.api.v1.models import models


class BaseTests(unittest.TestCase):
    """Authenticate a user and an admin and make the tokens available. Create a parcel and request"""


    def setUp(self):
        self.application = app.create_app('instance.config.TestingConfig')
        user_reg = json.dumps({
            "username" : "user",
            "email" : "user@gmail.com",
            "password" : "12345678",
            "confirm" : "12345678"})

        adminU_reg = json.dumps({
            "username" : "adminU1",
            "email" : "adminU1@gmail.com",
            "password" : "123456789",
            "confirm" : "123456789"})
        
        adminU_reg2 = json.dumps({
            "username" : "adminU2",
            "email" : "adminU2@gmail.com",
            "password" : "123456789",
            "confirm" : "123456789"})

        self.user_log = json.dumps({
            "email" : "user@gmail.com",
            "password" : "12345678"})

        self.adminU_log = json.dumps({
            "email" : "adminU1@gmail.com",
            "password" : "123456789"})
        
        self.adminU_log2 = json.dumps({
            "email" : "adminU2@gmail.com",
            "password" : "123456789"})

        self.admin_log = json.dumps({
            "email" : "admin@gmail.com",
            "password" : "adminU234"})

        self.app = self.application.test_client()

        
        register_user = self.app.post(
            '/api/v1/auth/userregister', data=user_reg,
            content_type='application/json')
        register_adminU = self.app.post(
            '/api/v1/auth/adminUregister', data=adminU_reg,
            content_type='application/json')
        
        register_adminU = self.app.post(
            '/api/v1/auth/adminUregister', data=adminU_reg2,
            content_type='application/json')
        
        admin_result = self.app.post(
            '/api/v1/auth/login', data=self.admin_log,
            content_type='application/json')
        
        admin_response = json.loads(admin_result.get_data(as_text=True))
        admin_token = admin_response["token"]
        self.admin_header = {"Content-Type" : "application/json", "x-access-token" : admin_token}

        adminU_result = self.app.post(
            '/api/v1/auth/login', data=self.adminU_log,
            content_type='application/json')

        adminU_response = json.loads(adminU_result.get_data(as_text=True))
        adminU_token = adminU_response["token"]
        self.adminU_header = {"Content-Type" : "application/json", "x-access-token" : adminU_token}

        adminU_result2 = self.app.post(
            '/api/v1/auth/login', data=self.adminU_log2,
            content_type='application/json')

        adminU_response2 = json.loads(adminU_result2.get_data(as_text=True))
        adminU_token2 = adminU_response2["token"]
        self.adminU_header2 = {"Content-Type" : "application/json", "x-access-token" : adminU_token2}
        
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
            headers=self.adminU_header)

        create_parcel2 = self.app.post(
            '/api/v1/parcels', data=parcel2, content_type='application/json',
            headers=self.adminU_header)

        requestparcel = self.app.post(
            '/api/v1/parcels/1/cancels',
            headers=self.user_header)
        
        requestparcel = self.app.post(
            '/api/v1/parcels/2/cancels',
            headers=self.user_header)
    
    def tearDown(self):
        with self.application.app_context():

            models.all_users = { 1 : {"id": "1", "username" : "admin",
            "email" : "admin@gmail.com", "password" : generate_password_hash("adminU234", method='sha256'), "usertype" : "admin",
            },}
            models.user_count = 2

            models.all_parcels = {}
            models.parcel_count = 1

            models.all_cancels = {}
            models.request_count = 1
