# test_api.py

import unittest
import os
import json
from app import create_app, db


class APITestCase(unittest.TestCase):
    """This represents the API test case"""

    def setUp(self):
        """Some test variables and initialize app"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.car = {
            'make': 'Tesla',
            'model': 'Model 3',
            'year': 2019,
            'currently_with': 'None'
        }
        self.branch = {
            'city': 'London',
            'postcode': 'SW4 0PE'
        }
        self.driver = {
            'name': 'John Doe',
            'dob': '01/01/1980'
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

    def test_branch_creation(self):
        """Test the creation of a branch with a POST request"""
        resp = self.client().post('/branches/', data=self.branch)
        self.assertEqual(resp.status_code, 201)
        self.assertIn('London', str(resp.data))
        self.assertIn('SW4 0PE', str(resp.data))

    def test_driver_creation(self):
        """Test the creation of a driver with a POST request"""
        resp = self.client().post('/drivers/', data=self.driver)
        self.assertEqual(resp.status_code, 201)
        self.assertIn('John Doe', str(resp.data))
        self.assertIn('01/01/1980', str(resp.data))

    def test_retrieve_all_cars(self):
        """Test api can get a list of all cars with a GET request"""
        resp = self.client().post('/cars/', data=self.car)
        self.assertEqual(resp.status_code, 201)
        resp = self.client().get('/cars/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Tesla', str(resp.data))
        self.assertIn('Model 3', str(resp.data))
        self.assertIn('2019', str(resp.data))

    def test_retrieve_all_branches(self):
        """Test api can get a list of all branches with a GET request"""
        resp = self.client().post('/branches/', data=self.branch)
        self.assertEqual(resp.status_code, 201)
        resp = self.client().get('/branches/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('London', str(resp.data))
        self.assertIn('SW4 0PE', str(resp.data))

    def test_retrieve_all_drivers(self):
        """Test api can get a list of all drivers with a GET request"""
        resp = self.client().post('/drivers/', data=self.driver)
        self.assertEqual(resp.status_code, 201)
        resp = self.client().get('/drivers/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('John Doe', str(resp.data))
        self.assertIn('01/01/1980', str(resp.data))

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

    def test_can_retrieve_branch_by_id(self):
        """Test api can retrieve an existing branch by id"""
        resp = self.client().post('/branches/', data=self.branch)
        self.assertEqual(resp.status_code, 201)
        obj = json.loads(resp.data.decode())
        resp = self.client().get('/branches/{}'.format(obj['id']))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('London', str(resp.data))
        self.assertIn('SW4 0PE', str(resp.data))

    def test_can_retrieve_driver_by_id(self):
        """Test api can retrieve an existing driver by id"""
        resp = self.client().post('/drivers/', data=self.driver)
        self.assertEqual(resp.status_code, 201)
        obj = json.loads(resp.data.decode())
        resp = self.client().get('/drivers/{}'.format(obj['id']))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('John Doe', str(resp.data))
        self.assertIn('01/01/1980', str(resp.data))

    def test_can_update_car(self):
        """Test api can update an existing car entry"""
        resp = self.client().post('/cars/', data=self.car)
        self.assertEqual(resp.status_code, 201)
        self.assertIn('Tesla', str(resp.data))
        resp = self.client().put('/cars/1', data={
            'make': 'Foo'
        })
        self.assertEqual(resp.status_code, 200)
        resp = self.client().get('/cars/1')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Foo', str(resp.data))

    def test_can_assign_driver(self):
        """Test api can update an existing car entry with a driver"""
        self.client().post('/cars/', data=self.car)
        self.client().post('/drivers/', data=self.driver)
        resp = self.client().put('/cars/1/drivers/1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.data)['currently_with'],
                         '"{ '
                         'type: driver, '
                         'id: 1, '
                         'name: John Doe, '
                         'dob: 01/01/1980  '
                         '}"'
                         )

    def test_can_assign_branch(self):
        """Test api can update an existing car entry with a branch"""
        self.client().post('/cars/', data=self.car)
        self.client().post('/branches/', data=self.branch)
        resp = self.client().put('/cars/1/branches/1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.data)['currently_with'],
                         '"{ '
                         'type: branch, '
                         'id: 1, '
                         'city: London, '
                         'postcode: SW4 0PE  '
                         '}"'
                         )

    def tearDown(self):
        """Teardown all the tables"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
