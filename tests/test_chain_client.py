from nose.tools import assert_true, assert_raises, assert_is_not_none
from unittest import TestCase
from unittest.mock import patch
from factom_sdk.client.chain_client import ChainClient


class TestChainClientInit(TestCase):
    def test_init(self):
        """Check init chain"""
        with assert_raises(Exception) as cm:
            ChainClient("http://google.com", "1", "1", True, "")
        assert_true("chain_id is required." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = ChainClient("http://google.com", "1", "1", True, "123")
            assert_is_not_none(response)

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True

            def signature_validation(params: dict):
                return "valid_signature"

            response = ChainClient("http://google.com", "1", "1", False, "123", signature_validation)
            assert_is_not_none(response)


class TestChainClient(TestCase):
    def setUp(self):
        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            mock_get.return_value.json.return_value = {
                "data": {
                    "chain_id": "123"
                }
            }

            self.chain = ChainClient("http://google.com", "1", "1", False, "123", False)

    def test_validate_signature(self):
        """Check validate signature"""
        print(self.chain)
        chain = {
            "data": {
                "external_ids": [
                    'SignedChain',
                    '0x01',
                    '171e5851451ce6f2d9730c1537da4375feb442870d835c54a1bca8ffa7e2bda7',
                    'idpub3NegGMKn2CDcx3A9JkpoMm2jE9KxchxqHTmXPvJnmUJGizfrb7',
                    '779229d23cdb7380869e63e5156a5497170bceec139b37e7af2a4d1aae14d053d19f7626e08d4bbb003d4b05d941f43402f1288af2ff0391a2dee4abf0919b07',
                    '2019-01-18T14:17:50Z',
                ],
                "dblock": {
                    "height": 10000
                },
                "content": "123"
            }
        }

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            json = {
                "data": [{
                    "key": "123"
                }]
            }
            mock_get.return_value.ok = True
            mock_get.return_value.json.return_value = json
            response = self.chain.validate_signature(chain)
            assert_is_not_none(response)

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            json = {
                "data": [{
                    "key": "idpub3NegGMKn2CDcx3A9JkpoMm2jE9KxchxqHTmXPvJnmUJGizfrb7"
                }]
            }
            mock_get.return_value.ok = True
            mock_get.return_value.json.return_value = json
            response = self.chain.validate_signature(chain)
            assert_is_not_none(response)

    def test_get_entry_info(self):
        """Check get entry info"""
        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = self.chain.get_entry_info("123")
        assert_is_not_none(response)

    def test_create_entry(self):
        """Check get entry info"""
        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_post:
            mock_post.return_value.ok = True
            response = self.chain.create_entry("123", ["123"],
                                               "idsec1Xbja4exmHFNgVSsk7VipNi4mwt6BjQFEZFCohs4Y7TzfhHoy6",
                                               "171e5851451ce6f2d9730c1537da4375feb442870d835c54a1bca8ffa7e2bda7",
                                               "http://google.com", ["123"])
        assert_is_not_none(response)

    def test_get_entries(self):
        """Check get entries"""
        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = self.chain.get_entries(1, 1, ["1"])
        assert_is_not_none(response)

    def test_get_first_entry(self):
        """Check get first entry"""
        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = self.chain.get_first_entry()
        assert_is_not_none(response)

    def test_get_last_entry(self):
        """Check get last entry"""
        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = self.chain.get_last_entry()
        assert_is_not_none(response)

    def test_search_entries(self):
        """Check search entries"""
        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_post:
            mock_post.return_value.ok = True
            response = self.chain.search_entries(["1"], 1, 1)
        assert_is_not_none(response)
