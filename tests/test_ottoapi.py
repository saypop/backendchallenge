# test_otto-backend.py

import unittest
import os
import json
from app import create_app, db


class CarTestCase(unittest.TestCase):
    """This represents the car test case"""

    def setUp(self):
        """Some test variables and initialize app"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.car = {
            'make': 'Tesla',
            'model': 'Model 3',
            'year': 2019
        }

        with self.app.app_context():
            db.create_all()

    def test_car_creation(self):
        """Test the creation of a car with a POST request"""
        resp = self.client().post('/cars/', data=self.car)
        self.assertEqual(resp.status_code, 201)
        self.assertIn('Tesla', str(resp.data))
        self.assertIn('Model 3', str(resp.data))
        self.assertIn('2019', str(resp.data))

    def test_retrieve_all_cars(self):
        """Test api can get a list of all cars with a GET request"""
        resp = self.client().post('/cars/', data=self.car)
        self.assertEqual(resp.status_code, 201)
        resp = self.client().get('/cars/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Tesla', str(resp.data))
        self.assertIn('Model 3', str(resp.data))
        self.assertIn('2019', str(resp.data))

    def test_can_retrieve_car_by_id(self):
        """Test api can retrieve an existing car by id"""
        resp = self.client().post('/cars/', data=self.car)
        self.assertEqual(resp.status_code, 201)
        obj = json.loads(resp.data.decode())
        resp = self.client().get('/cars/{}'.format(obj['id']))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Tesla', str(resp.data))
        self.assertIn('Model 3', str(resp.data))
        self.assertIn('2019', str(resp.data))

    def tearDown(self):
        """teardown all the tables"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
