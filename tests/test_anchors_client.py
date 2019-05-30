from unittest import TestCase
from unittest.mock import patch
from factom_sdk.client.anchors_client import AnchorsClient
from factom_sdk.request_handler.request_handler import RequestHandler


class TestAnchorsClient(TestCase):
    """Test anchors client"""

    def setUp(self):
        self.anchors_client = AnchorsClient("https://apicast.io", "123456", "123456789")

    def tearDown(self):
        self.anchors_client = None

    def test_init(self):
        """Check init anchors client"""
        self.assertTrue(isinstance(self.anchors_client.request_handler, RequestHandler))

    def test_get(self):
        """Check get anchors"""
        error_expected = "object_identifier parameter must be a positive int or a string of length 64"
        with self.assertRaises(AssertionError) as cm:
            self.anchors_client.get(object_identifier=None)
        self.assertTrue(error_expected in str(cm.exception))

        with self.assertRaises(AssertionError) as cm:
            self.anchors_client.get(object_identifier="")
        self.assertTrue(error_expected in str(cm.exception))

        with self.assertRaises(AssertionError) as cm:
            self.anchors_client.get(object_identifier=-1)
        self.assertTrue(error_expected in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            h = "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
            response = self.anchors_client.get(object_identifier=h)
            self.assertIsNotNone(response)

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = self.anchors_client.get(object_identifier=123)
            self.assertIsNotNone(response)
