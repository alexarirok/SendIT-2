"""Test the parcel endpoints on all methods and covers most edge cases
"""
import unittest
import json

import sys # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.api.v1.models import models
from .base_test import BaseTests


class ParcelTests(BaseTests):
    """Tests functionality of the parcel endpoint"""


    def test_admin_get_one(self):
        """Tests admin successfully getting a book"""
        response = self.app.get('/api/v1/parcels/1', headers=self.user_header)
        self.assertEqual(response.status_code, 200)

    def test_user_get_one(self):
        """Tests user successfully getting a parcel"""
        response = self.app.get('/api/v1/parcels/2', headers=self.user_header)
        self.assertEqual(response.status_code, 200)
    
    def test_user_get_all(self):
        """Tests user successfully getting all parcel"""
        response = self.app.get('/api/v1/parcels',)
        self.assertEqual(response.status_code, 200)

    def test_get_non_existing(self):
        """Test getting a parcel while providing non-existing id"""
        response = self.app.get('/api/v1/parcels/300', headers=self.user_header)
        self.assertEqual(response.status_code, 404)

    def test_good_parcel_update(self):
        """Test a successful parcel update"""
        initial_data = json.dumps({"pickup_location" : "Syokimau", "destination_location" : "Nairobi",
         "date_ordered" : "16/04/2015 1400HRS", "price" : "400", "max" : "1"})
        added_parcel = self.app.post( # pylint: disable=W0612
            '/api/v1/parcels', data=initial_data,
            content_type='application/json',
            headers=self.adminU_header)
        data = json.dumps({"pickup_location" : "Kayole", "destination_location" : "Nairobi",
         "date_ordered" : "16/04/2015 1400HRS", "price" : "400", "max" : "2"})
        response = self.app.put(
            '/api/v1/parcels/2', data=data,
            content_type='application/json',
            headers=self.adminU_header)
        self.assertEqual(response.status_code, 200)

    def test_bad_parcel_create(self):
        """Test a unsuccessful parcel create"""
        initial_data = json.dumps({"pickup_location" : "Syokimau", "destination_location" : "Nairobi",
         "date_ordered" : "16/04/2015 1400HRS", "price" : "400", "max" : "1"})
        added_parcel = self.app.post( # pylint: disable=W0612
            '/api/v1/parcels', data=initial_data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(added_parcel.status_code, 401)
    
    def test_invalid_token_parcel_create(self):
        """Test a unsuccessful parcel create"""
        invalid_token = {
            "Content-Type" : "application/json",
            "x-access-token" : "hbGciOiJIUzI1NiJ9.eyJpZCI6NCwiYWRtaW4iOnRydWUsImV4cCI6MTUyNjczNzQ5Nvm2laNiJek7X266RLLk-bWL-ZF2RuD32FBvg_G8KyM"}
        initial_data = json.dumps({"pickup_location" : "Githuraiu", "destination_location" : "Nairobi",
         "date_ordered" : "16/04/2015 1400HRS", "price" : "400", "max" : "1"})
        added_parcel = self.app.post( # pylint: disable=W0612
            '/api/v1/parcels', data=initial_data,
            content_type='application/json',
            headers=invalid_token)
        self.assertEqual(added_parcel.status_code, 401)

    def test_update_non_existing(self):
        """Test updating non_existing parcel"""
        data = json.dumps({"pickup_location" : "Syokimau", "destination_location" : "Nairobi",
         "date_ordered" : "16/04/2015 1400HRS", "price" : "400", "max" : "1"})
        response = self.app.put(
            '/api/v1/parcels/200', data=data,
            content_type='application/json',
            headers=self.adminU_header)
        self.assertEqual(response.status_code, 404)

    def test_good_deletion(self):
        """Test a successful parcel deletion"""
        response = self.app.delete('/api/v1/parcels/1', headers=self.adminU_header)
        self.assertEqual(response.status_code, 200)

    def test_no_header(self):
        """Test a unsuccessful parcel deletion"""
        response = self.app.delete('/api/v1/parcels/1',)
        self.assertEqual(response.status_code, 401)

    def test_deleting_non_existing(self):
        """Test deleting parcel that does not exist"""
        response = self.app.delete('/api/v1/parcels/200', headers=self.adminU_header)
        self.assertEqual(response.status_code, 404)
    
    def test_start_parcel_delivery(self):
        """Test starting a parcel successfully"""
        response = self.app.post('/api/v1/parcels/1', headers=self.adminU_header)
        self.assertEqual(response.status_code, 200)
    
    def test_unsuccessful_start_parcel_delivery(self):
        """Test starting a parcel unsuccessfully"""
        response = self.app.post('/api/v1/parcels/5', headers=self.adminU_header2)
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
