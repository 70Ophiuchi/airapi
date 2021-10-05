import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import true
from werkzeug.datastructures import Headers

from mainApp import *
from models import *

FA_JWT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkhrbjFFRndQUG5kSjVOQzZkaE5iTCJ9.eyJpc3MiOiJodHRwczovL2Rldi1udTB3bHEtci5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE0MGQyMzExYjU0ZTUwMDcyMDJmOGE5IiwiYXVkIjoiQWlyQVBJIiwiaWF0IjoxNjMzNDY1MDg5LCJleHAiOjE2MzM0NzIyODksImF6cCI6Ik9LQ0JWMzh2SjJnaUpYNFQ2ZXVBbmRxcW1UWmp3ZU51Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6YWlycGxhbmUiLCJhZGQ6YWlycG9ydCIsImRlbGV0ZTphaXJwbGFuZSIsImRlbGV0ZTphaXJwb3J0IiwidXBkYXRlOmFpcnBsYW5lIiwidXBkYXRlOmFpcnBvcnQiXX0.dtUQPKt-C0navbn2rUezS92xf2WhsNfUjcbZrFiVr84QajGOuu56mM1uqPgFo404q62U0KwYQwUYqqHlkt2vyNbkJe8uWNGHJp6QO3Dd_rPHm9VdPKhlY-24vo1LagsRi8-f8xCBLqB7Ly9Ko5I45eDv1yV67LdxUfJGBHGz9MevJ7Sb6wBxsUk_hDjbJcbczuLZa7gUDR1cznxEXP52CgN6OOBUQij56Pq4n8IsQIBqitZgq6EyPYGVHe4cSBQWx1pG0bdvep_erPPKqnG5DVfE3nVToZkLwpWeam3wGOhUzu9zK03ZXvlwkmV4qxsPyxKWV4drjE0Qn-HvB_zawA'

class TriviaTestCase(unittest.TestCase):

    def setUp(self):

        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgres://bboafxezreihwv:a8b57bcf9ee1f036b78377d5a0adea0fe257fa182db47cba22c4518997a43f9f@ec2-3-209-65-193.compute-1.amazonaws.com:5432/dbibhl32k6odde'

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

            self.db.create_all()

    def tearDown(self):
        pass

    def test_get_airplanes(self):
        res = self.client().get("/airplanes")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["airplanes"])
    
    def test_get_airports(self):
        res = self.client().get("/airports")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["airports"])

    def test_post_airplanes_unauth(self):
        data = {'name': '747', 'manufacturer': 'boeing', 'built_in': '1969'}
        res = self.client().post('/airplanes', data)

        self.assertEqual(res.status_code, 401)

    def test_post_airports_unauth(self):
        data = {'name': 'John F. Kennedy International', 'code': 'KJFK', 'country': 'USA'}
        res = self.client().post('/airplanes', data)

        self.assertEqual(res.status_code, 401)

    def test_delete_airplane_unauth(self):
        res = self.client().delete('/airplanes/1')

        self.assertEqual(res.status_code, 401)

    def test_delete_airport_unauth(self):
        res = self.client().delete('/airport/1')

        self.assertEqual(res.status_code, 401)

    def test_post_airplanes_auth(self):
        data = {'name': '747', 'manufacturer': 'boeing', 'built_in': '1969'}
        header = {'Authorization': 'Bearer {}'.format(FA_JWT)}
        res = self.client().post('/airplanes', data=data, headers=header)

        self.assertEqual(res.status_code, 200)

    def test_post_airports_auth(self):
        data = {'name': 'John F. Kennedy International', 'code': 'KJFK', 'country': 'USA'}
        header = {'Authorization': 'Bearer {}'.format(FA_JWT)}
        res = self.client().post('/airplanes', data=data, headers=header)

        self.assertEqual(res.status_code, 200)

    def test_delete_airplane_auth(self):
        header = {'Authorization': 'Bearer {}'.format(FA_JWT)}
        res = self.client().delete('/airplanes/1', headers=header)

        self.assertEqual(res.status_code, 200)

    def test_delete_airport_auth(self):
        header = {'Authorization': 'Bearer {}'.format(FA_JWT)}
        res = self.client().delete('/airport/1', headers=header)

        self.assertEqual(res.status_code, 200)

    def test_patch_airplanes_auth(self):
        data = {'name': '747', 'manufacturer': 'boeing', 'built_in': '1969'}
        header = {'Authorization': 'Bearer {}'.format(FA_JWT)}
        res = self.client().patch('/airplanes/1', data=data, headers=header)

        self.assertEqual(res.status_code, 200)

    def test_patch_airplanes_unauth(self):
        data = {'name': '747', 'manufacturer': 'boeing', 'built_in': '1969'}
        res = self.client().post('/airplanes/1', data=data)

        self.assertEqual(res.status_code, 401)

    def test_patch_airports_auth(self):
        data = {'name': 'John F. Kennedy International', 'code': 'KJFK', 'country': 'USA'}
        header = {'Authorization': 'Bearer {}'.format(FA_JWT)}
        res = self.client().patch('/airports/1', data=data, headers=header)

        self.assertEqual(res.status_code, 200)

    def test_patch_airports_unauth(self):
        data = {'name': 'John F. Kennedy International', 'code': 'KJFK', 'country': 'USA'}
        res = self.client().patch('/airports/1', data=data)

        self.assertEqual(res.status_code, 401)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()