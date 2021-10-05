import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import *
from models import *


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

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["categories"])
#################################################################
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

    def test_post_airplanes(self):
        res = self.client().post()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()