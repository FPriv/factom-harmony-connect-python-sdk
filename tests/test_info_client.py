from nose.tools import assert_true, assert_is_not_none
from unittest import TestCase
from unittest.mock import patch
from factom_sdk.client.info_client import InfoClient
from factom_sdk.request_handler.request_handler import RequestHandler


class TestInfoClient(TestCase):
    def setUp(self):
        self.info_client = InfoClient("https://apicast.io", "123456", "123456789")

    def tearDown(self):
        self.info_client = None

    def test_init(self):
        """Check init identity client"""
        assert_true(isinstance(self.info_client.request_handler, RequestHandler))

    def test_get_info(self):
        """Check get info"""
        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = self.info_client.get_info()
        assert_is_not_none(response)
