from unittest import TestCase
from unittest.mock import patch
from factom_sdk.client.receipts_client import ReceiptsClient
from factom_sdk.request_handler.request_handler import RequestHandler


class TestReceiptsClient(TestCase):
    """Test receipts client"""

    def setUp(self):
        self.receipts_client = ReceiptsClient("https://apicast.io", "123456", "123456789")

    def tearDown(self):
        self.receipts_client = None

    def test_init(self):
        """Check init receipts client"""
        self.assertTrue(isinstance(self.receipts_client.request_handler, RequestHandler))

    def test_get(self):
        """Check get receipt"""
        with self.assertRaises(AssertionError) as cm:
            self.receipts_client.get(entry_hash=None)
        self.assertTrue("entry_hash must be a string of length 64" in str(cm.exception))

        with self.assertRaises(AssertionError) as cm:
            self.receipts_client.get(entry_hash="")
        self.assertTrue("entry_hash must be a string of length 64" in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            h = "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
            response = self.receipts_client.get(entry_hash=h)
            self.assertIsNotNone(response)
