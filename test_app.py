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

    def test_get_categories_wrong_method(self):
        res = self.client().post("/categories")

        self.assertEqual(res.status_code, 405)

    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"] >= 1)
        self.assertTrue(data["current_category"])
        self.assertTrue(data["categories"])

    def test_get_questions_wrong_method(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)

    def test_delete_question(self):
        res = self.client().delete("/questions/1")

        self.assertEqual(res.status_code, 200)

    def test_delete_question_out_of_range(self):
        res = self.client().delete("/questions/1000")

        self.assertEqual(res.status_code, 404)

    def test_create_question(self):
        res = self.client().post("/questions", {
                                                "question": 'Test',
                                                "answer": "Test",
                                                "category": "Test",
                                                "difficulty": "Test"
                                                }
                                 )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"] >= 1)
        self.assertTrue(data["current_category"])

    def test_create_question_wrong_method(self):
        res = self.client().delete("/questions", {
                                                "question": 'Test',
                                                "answer": "Test",
                                                "category": "Test",
                                                "difficulty": "Test"
                                                }
                                   )

        self.assertEqual(res.status_code, 422)

    def test_get_questions_by_category(self):
        res = self.client().get("/category/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"] >= 1)
        self.assertTrue(data["current_category"])

    def test_play_game(self):
        res = self.client().post("/quizzes", {
                                            "category": "science"
                                            }
                                 )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["question"])
        self.assertTrue(data["current_category"])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()