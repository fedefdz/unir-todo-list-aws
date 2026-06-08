import json
import os
import unittest
import uuid

import pytest
import requests

BASE_URL = os.environ.get("BASE_URL")
DEFAULT_TIMEOUT = 5


@pytest.mark.api
class TestApiReadOnly(unittest.TestCase):

    def setUp(self):
        self.assertIsNotNone(BASE_URL, "URL no configurada")
        self.assertTrue(len(BASE_URL) > 8, "URL no configurada")

    def test_api_listtodos_readonly(self):
        url = BASE_URL + "/todos"
        response = requests.get(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status_code, 200,
            f"GET {url} devolvio {response.status_code}"
        )
        body = response.json()
        self.assertIsInstance(
            body, list,
            "El endpoint /todos debe devolver una lista"
        )

    def test_api_gettodo_notfound_readonly(self):
        missing_id = str(uuid.uuid4())
        url = BASE_URL + "/todos/" + missing_id
        response = requests.get(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status_code, 404,
            f"GET {url} de un id inexistente debe ser 404"
        )
