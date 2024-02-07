"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

from unittest import TestCase
from src.counter import app, COUNTERS
from src import status


class CounterTest(TestCase):
    """Counter tests"""

    def setUp(self):
        self.client = app.test_client()

    def test_create_a_counter(self):
        """Counter should be created"""
        result = self.client.post("/counters/foo")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        result = self.client.post("/counters/foo")
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        self.client.post("/counters/bar")
        result = self.client.post("/counters/bar")
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """Update create a counter"""
        result = self.client.post("/counters/test")

        self.assertEqual(COUNTERS["test"], 0)
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        result = self.client.put("/counters/test")
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(COUNTERS["test"], 1)

        result = self.client.put("/counters/test2")
        self.assertEqual(result.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_a_counter(self):
        self.client.post("/counters/hello")
        self.client.put("/counters/hello")

        result = self.client.get("/counters/hello")
        self.assertEqual(result.status_code, status.HTTP_200_OK)

        result = self.client.get("/counters/hello2")
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_a_counter(self):
        result = self.client.delete("/counters/asd")
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

        self.client.post("/counters/asd")
        result = self.client.delete("/counters/asd")
        self.assertEqual(result.status_code, status.HTTP_204_OK)
        self.assertEqual(len(COUNTERS), 0)
