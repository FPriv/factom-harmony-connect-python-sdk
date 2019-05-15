from unittest import TestCase
from unittest.mock import patch
from factom_sdk.client.api_info_client import ApiInfoClient
from factom_sdk.request_handler.request_handler import RequestHandler


class TestInfoClient(TestCase):
    def setUp(self):
        self.info_client = ApiInfoClient("https://apicast.io", "123456", "123456789")

    def tearDown(self):
        self.info_client = None

    def test_init(self):
        """Check init api info client"""
        self.assertTrue(isinstance(self.info_client.request_handler, RequestHandler))

    def test_get_info(self):
        """Check get info"""
        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = self.info_client.get()
        self.assertIsNotNone(response)
