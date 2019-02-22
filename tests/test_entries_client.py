from nose.tools import assert_true, assert_is_not_none
from unittest import TestCase
from unittest.mock import patch
from factom_sdk.client.entries_client import EntriesClient
from factom_sdk.request_handler.request_handler import RequestHandler


class TestEntriesClient(TestCase):
    def setUp(self):
        self.entries_client = EntriesClient("https://apicast.io", "123456", "123456789", False)

    def tearDown(self):
        self.entries_client = None

    def test_init(self):
        """Check init chains client"""
        assert_true(isinstance(self.entries_client.request_handler, RequestHandler))

    def test_get_entry_info(self):
        """Check get entry info"""
        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = self.entries_client.get_entry_info("123", "123")
        assert_is_not_none(response)

    def test_create_entry(self):
        """Check create entry"""
        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_post:
            mock_post.return_value.ok = True
            response = self.entries_client.create_entry("123", "123", ["123"],
                                             "idsec1Xbja4exmHFNgVSsk7VipNi4mwt6BjQFEZFCohs4Y7TzfhHoy6",
                                             "171e5851451ce6f2d9730c1537da4375feb442870d835c54a1bca8ffa7e2bda7")
        assert_is_not_none(response)

    def test_get_entries_of_chain(self):
        """Check get entries of chain"""
        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = self.entries_client.get_entries_of_chain("123", 1, 1, ["1"])
        assert_is_not_none(response)

    def test_get_first_entry_of_chain(self):
        """Check get first entry of chain"""
        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = self.entries_client.get_first_entry_of_chain("123")
        assert_is_not_none(response)

    def test_get_last_entry_of_chain(self):
        """Check get last entry of chain"""
        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = self.entries_client.get_last_entry_of_chain("123")
        assert_is_not_none(response)

    def test_search_entries_of_chain(self):
        """Check search entries of chain"""
        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_post:
            mock_post.return_value.ok = True
            response = self.entries_client.search_entries_of_chain("123", ["1"], 1, 1)
        assert_is_not_none(response)
