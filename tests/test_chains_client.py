from unittest import TestCase
from unittest.mock import patch
from factom_sdk.client.chains_client import ChainsClient
from factom_sdk.request_handler.request_handler import RequestHandler


class TestChainsClientWithoutSigning(TestCase):
    """Test chains client without automatic signing"""

    def setUp(self):
        self.chains_client = ChainsClient("https://apicast.io", "123456", "123456789", False)

    def tearDown(self):
        self.chains_client = None

    def test_init(self):
        """Check init chains client"""
        self.assertTrue(isinstance(self.chains_client.request_handler, RequestHandler))

    def test_get(self):
        """Check get chain info"""
        with self.assertRaises(Exception) as cm:
            self.chains_client.get("")
        self.assertTrue("chain_id is required." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True

            def signature_validation(params: dict):
                return "valid_signature"

            response = self.chains_client.get("123124", signature_validation)
            self.assertIsNotNone(response)
        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = self.chains_client.get("123124", False)
            self.assertIsNotNone(response)

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = self.chains_client.get("123124")
            self.assertIsNotNone(response)

    def test_create(self):
        """Check create chain"""
        with self.assertRaises(Exception) as cm:
            self.chains_client.create("", ["123"])
        self.assertTrue("content is required." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.chains_client.create("123")
        self.assertTrue("at least 1 external_id is required." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.chains_client.create("123", "1")
        self.assertTrue("external_ids must be an array." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.chains_client.create("123", ["1"], "idsec")
        self.assertTrue("signer_chain_id is required when passing a signer_private_key." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.chains_client.create("123", ["1"], "idsec", "123")
        self.assertTrue("signer_private_key is invalid." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.chains_client.create("123", ["1"], "", "123")
        self.assertTrue("signer_private_key is required when passing a signer_chain_id." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.chains_client.create("123", ["1"], "", "", "google")
        self.assertTrue("callback_url is an invalid url format." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.chains_client.create("123", ["1"], "", "", "", "123")
        self.assertTrue("callback_stages must be an array." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_post:
            mock_post.return_value.ok = True
            response = self.chains_client.create("123", ["1"], "", "", "http://google.com", ["123"])
        self.assertIsNotNone(response)

    def test_list(self):
        """Check get all chains"""
        with self.assertRaises(Exception) as cm:
            self.chains_client.list("1")
        self.assertTrue("limit must be an integer." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.chains_client.list(1, "1")
        self.assertTrue("offset must be an integer." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.chains_client.list(1, 1, "1")
        self.assertTrue("stages must be an array." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = self.chains_client.list(1, 1, ["123"])
            self.assertIsNotNone(response)

    def test_search(self):
        """Check search chains"""
        with self.assertRaises(Exception) as cm:
            self.chains_client.search([])
        self.assertTrue("at least 1 external_id is required." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.chains_client.search("123")
        self.assertTrue("external_ids must be an array." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.chains_client.search(["123"], "1")
        self.assertTrue("limit must be an integer." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.chains_client.search(["123"], 1, "1")
        self.assertTrue("offset must be an integer." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_post:
            mock_post.return_value.ok = True
            response = self.chains_client.search(["123"], 1, 1)
            self.assertIsNotNone(response)

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_post:
            mock_post.return_value.ok = True
            response = self.chains_client.search(["123"], -1, 1)
            self.assertIsNotNone(response)


class TestChainsClientWithSigning(TestCase):
    """Test chains client with automatic signing"""

    def setUp(self):
        self.chains_client = ChainsClient("https://apicast.io", "123456", "123456789", True)

    def tearDown(self):
        self.chains_client = None

    def test_create(self):
        """Check create chain"""
        with self.assertRaises(Exception) as cm:
            self.chains_client.create("123", "123")
        self.assertTrue("external_ids must be an array." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.chains_client.create("123", [])
        self.assertTrue("signer_private_key is required." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.chains_client.create("123", [], "idsec")
        self.assertTrue("signer_private_key is invalid." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.chains_client.create("123", [], "idsec1Xbja4exmHFNgVSsk7VipNi4mwt6BjQFEZFCohs4Y7TzfhHoy6")
        self.assertTrue("signer_chain_id is required." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_post:
            mock_post.return_value.ok = True
            response = self.chains_client.create("123", [], "idsec1Xbja4exmHFNgVSsk7VipNi4mwt6BjQFEZFCohs4Y7TzfhHoy6",
                                            "171e5851451ce6f2d9730c1537da4375feb442870d835c54a1bca8ffa7e2bda7")
        self.assertIsNotNone(response)

