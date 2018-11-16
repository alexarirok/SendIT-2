"""Test the parcel request endpoints on all methods and covers most edge cases
"""
import unittest
import json

import sys # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.api.v1.models import parcels, users
from .base_test import BaseTests


class RequestParcelTests(BaseTests):
    """Tests functionality of the request endpoint"""

    def test_user_request_parcel(self):
        """Tests user successfully requesting a parcel"""
        request_parcel = self.app.post( # pylint: disable=W0612
            '/api/v1/parcels/1/cancels',
            headers=self.user_header)
        response = request_parcel
        self.assertEqual(response.status_code, 201)
    
    def test_no_token_request_parcel(self):
        """Tests user successfully requesting a parcel"""
        request_parcel = self.app.post( # pylint: disable=W0612
            '/api/v1/parcels/1/cancels')
        response = request_parcel
        self.assertEqual(response.status_code, 401)


    def test_admin_get_allcancels(self):
        """Tests admin successfully getting all cancels"""
        response = self.app.get('/api/v1/cancels', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_user_get_one(self):
        """Tests user successfully getting a request"""
        response = self.app.get('/api/v1/cancels/2', headers=self.user_header)
        self.assertEqual(response.status_code, 200)

    def test_get_non_existing(self):
        """Test getting a request while providing non-existing id"""
        response = self.app.get('/api/v1/cancels/50', headers=self.user_header)
        self.assertEqual(response.status_code, 404)

    def test_good_request_accept_reject(self):
        """Test a successful request update"""
        response = self.app.put(
            '/api/v1/cancels/2',
            content_type='application/json',
            headers=self.admin_header)
        

        self.assertEqual(response.status_code, 200)

    def test_bad_request_accept_reject(self):
        """Test an unsuccessful request update from a admin who does not own the trip"""
        response = self.app.put(
            '/api/v1/cancels/2',
            content_type='application/json',
            headers=self.admin_header2)
        self.assertEqual(response.status_code, 404)

    def test_update_non_existing(self):
        response = self.app.put(
            '/api/v1/cancels/50',
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 404)

    def test_good_deletion(self):
        """Test a successful request deletion"""
        response = self.app.delete('/api/v1/cancels/1', headers=self.user_header)
        self.assertEqual(response.status_code, 200)
    
    def test_bad_deletion_not_your_request(self):
        """Test a unsuccessful request deletion"""
        response = self.app.delete('/api/v1/cancels/1', headers=self.admin_header2)
        self.assertEqual(response.status_code, 404)

    def test_deleting_non_existing(self):
        """Test deleting request that does not exist"""
        response = self.app.delete('/api/v1/cancels/500', headers=self.user_header)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()