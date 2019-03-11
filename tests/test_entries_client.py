from unittest import TestCase
from unittest.mock import patch
from factom_sdk.client.entries_client import EntriesClient
from factom_sdk.request_handler.request_handler import RequestHandler


class TestEntriesClientWithoutSigning(TestCase):
    def setUp(self):
        self.entries_client = EntriesClient("https://apicast.io", "123456", "123456789", False)

    def tearDown(self):
        self.entries_client = None

    def test_init(self):
        """Check init chains client"""
        self.assertTrue(isinstance(self.entries_client.request_handler, RequestHandler))

    def test_get(self):
        """Check get entry info"""
        with self.assertRaises(Exception) as cm:
            self.entries_client.get("", "", False)
        self.assertTrue("chain_id is required." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.entries_client.get("123", "", False)
        self.assertTrue("entry_hash is required." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = self.entries_client.get("123", "123", False)
            self.assertIsNotNone(response)

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = self.entries_client.get("123", "123")
            self.assertIsNotNone(response)

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True

            def signature_validation(params: dict):
                return "valid_signature"

            response = self.entries_client.get("123", "123", signature_validation)
            self.assertIsNotNone(response)

    def test_create(self):
        """Check create entry"""
        with self.assertRaises(Exception) as cm:
            self.entries_client.create("", "")
        self.assertTrue("chain_id is required." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.entries_client.create("123", "")
        self.assertTrue("at least 1 external_id is required." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.entries_client.create("123", "", "123")
        self.assertTrue("external_ids must be an array." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.entries_client.create("123", "", ["123"], "idsec")
        self.assertTrue("signer_chain_id is required when passing a signer_private_key." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.entries_client.create("123", "", ["123"], "idsec", "123")
        self.assertTrue("signer_private_key is invalid." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.entries_client.create("123", "", ["123"], "", "123")
        self.assertTrue("signer_private_key is required when passing a signer_chain_id." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.entries_client.create("123", "", ["123"])
        self.assertTrue("content is required." in str(cm.exception))

    def test_list(self):
        """Check get entries"""
        with self.assertRaises(Exception) as cm:
            self.entries_client.list("")
        self.assertTrue("chain_id is required." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.entries_client.list("123", "1")
        self.assertTrue("limit must be an integer." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.entries_client.list("123", 1, "1")
        self.assertTrue("offset must be an integer." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.entries_client.list("123", 1, 1, "1")
        self.assertTrue("stages must be an array." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = self.entries_client.list("123", 1, 1, ["1"])
        self.assertIsNotNone(response)

    def test_get_first(self):
        """Check get first entry"""
        with self.assertRaises(Exception) as cm:
            self.entries_client.get_first("")
        self.assertTrue("chain_id is required." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = self.entries_client.get_first("123")
        self.assertIsNotNone(response)

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = self.entries_client.get_first("123", False)
        self.assertIsNotNone(response)

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True

            def signature_validation(params: dict):
                return "valid_signature"

            response = self.entries_client.get_first("123", signature_validation)
        self.assertIsNotNone(response)

    def test_get_last(self):
        """Check get last entry"""
        with self.assertRaises(Exception) as cm:
            self.entries_client.get_last("")
        self.assertTrue("chain_id is required." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = self.entries_client.get_last("123")
        self.assertIsNotNone(response)

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = self.entries_client.get_last("123", False)
        self.assertIsNotNone(response)

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True

            def signature_validation(params: dict):
                return "valid_signature"

            response = self.entries_client.get_last("123", signature_validation)
        self.assertIsNotNone(response)

    def test_search(self):
        """Check search entries"""
        with self.assertRaises(Exception) as cm:
            self.entries_client.search("", [])
        self.assertTrue("chain_id is required." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.entries_client.search("123", [])
        self.assertTrue("at least 1 external_id is required." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.entries_client.search("123", "123")
        self.assertTrue("external_ids must be an array." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.entries_client.search("123", ["1"], "1")
        self.assertTrue("limit must be an integer." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.entries_client.search("123", ["1"], 1, "1")
        self.assertTrue("offset must be an integer." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_post:
            mock_post.return_value.ok = True
            response = self.entries_client.search("123", ["1"], 1, 1)
        self.assertIsNotNone(response)

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_post:
            mock_post.return_value.ok = True
            response = self.entries_client.search("123", ["1"], -1, 1)
        self.assertIsNotNone(response)


class TestEntriesClientWithSigning(TestCase):
    def setUp(self):
        self.entries_client = EntriesClient("https://apicast.io", "123456", "123456789", True)

    def tearDown(self):
        self.entries_client = None

    def test_create(self):
        """Check create entry"""
        with self.assertRaises(Exception) as cm:
            self.entries_client.create("123", "", "123", "idsec", "123")
        self.assertTrue("external_ids must be an array." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.entries_client.create("123", "", ["123"], "", "")
        self.assertTrue("signer_private_key is required." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.entries_client.create("123", "", ["123"], "idsec", "")
        self.assertTrue("signer_private_key is invalid." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.entries_client.create("123", "", ["123"],
                                       "idsec1Xbja4exmHFNgVSsk7VipNi4mwt6BjQFEZFCohs4Y7TzfhHoy6", "")
        self.assertTrue("signer_chain_id is required." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.entries_client.create("123", "123", ["123"],
                                       "idsec1Xbja4exmHFNgVSsk7VipNi4mwt6BjQFEZFCohs4Y7TzfhHoy6", "123", "google")
        self.assertTrue("callback_url is an invalid url format." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.entries_client.create("123", "123", ["123"],
                                       "idsec1Xbja4exmHFNgVSsk7VipNi4mwt6BjQFEZFCohs4Y7TzfhHoy6",
                                       "123", "", "123")
        self.assertTrue("callback_stages must be an array." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_post:
            mock_post.return_value.ok = True
            response = self.entries_client.create("123", "123", ["123"],
                                                  "idsec1Xbja4exmHFNgVSsk7VipNi4mwt6BjQFEZFCohs4Y7TzfhHoy6",
                                                  "123", "http://google.com", ["123"])
        self.assertIsNotNone(response)
