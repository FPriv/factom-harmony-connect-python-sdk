from nose.tools import *
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
        assert_true(isinstance(self.chains_client.request_handler, RequestHandler))

    def test_get_chain_info(self):
        """Check get chain info"""
        with assert_raises(Exception) as cm:
            self.chains_client.get_chain_info("")
        assert_true("chain_id is required." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True

            def signature_validation(params: dict):
                return "valid_signature"

            response = self.chains_client.get_chain_info("123124", signature_validation)
            assert_is_not_none(response)
        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = self.chains_client.get_chain_info("123124", False)
            assert_is_not_none(response)
        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = self.chains_client.get_chain_info("123124", True)
            assert_is_not_none(response)

    def test_validate_signature(self):
        """Check validate signature"""
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
            json = [{
                "key": "123"
            }]
            mock_get.return_value.ok = True
            mock_get.return_value.json.return_value = json
            response = self.chains_client.validate_signature(chain)
            assert_is_not_none(response)

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            json = [{
                "key": "idpub3NegGMKn2CDcx3A9JkpoMm2jE9KxchxqHTmXPvJnmUJGizfrb7"
            }]
            mock_get.return_value.ok = True
            mock_get.return_value.json.return_value = json
            response = self.chains_client.validate_signature(chain)
            assert_is_not_none(response)

    def test_create_chain(self):
        """Check create chain"""
        with assert_raises(Exception) as cm:
            self.chains_client.create_chain("", ["123"])
        assert_true("content is required." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.chains_client.create_chain("123")
        assert_true("at least 1 external_ids is required." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.chains_client.create_chain("123", "1")
        assert_true("external_ids must be an array." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.chains_client.create_chain("123", ["1"], "idsec")
        assert_true("signer_chain_id is required when passing a signer_private_key." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.chains_client.create_chain("123", ["1"], "idsec", "123")
        assert_true("signer_private_key is invalid." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.chains_client.create_chain("123", ["1"], "", "123")
        assert_true("signer_private_key is required when passing a signer_chain_id." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.chains_client.create_chain("123", ["1"], "", "", "google")
        assert_true("callback_url is an invalid url format." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.chains_client.create_chain("123", ["1"], "", "", "", "123")
        assert_true("callback_stages must be an array." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_post:
            mock_post.return_value.ok = True
            response = self.chains_client.create_chain("123", ["1"], "", "", "http://google.com", ["123"])
        assert_is_not_none(response)

    def test_get_all_chains(self):
        """Check get all chains"""
        with assert_raises(Exception) as cm:
            self.chains_client.get_all_chains("1")
        assert_true("limit must be an integer." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.chains_client.get_all_chains(1, "1")
        assert_true("offset must be an integer." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.chains_client.get_all_chains(1, 1, "1")
        assert_true("stages must be an array." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = self.chains_client.get_all_chains(1, 1, ["123"])
            assert_is_not_none(response)

    def test_search_chains(self):
        """Check search chains"""
        with assert_raises(Exception) as cm:
            self.chains_client.search_chains([])
        assert_true("at least 1 external_ids is required." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.chains_client.search_chains("123")
        assert_true("external_ids must be an array." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.chains_client.search_chains(["123"], "1")
        assert_true("limit must be an integer." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.chains_client.search_chains(["123"], 1, "1")
        assert_true("offset must be an integer." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_post:
            mock_post.return_value.ok = True
            response = self.chains_client.search_chains(["123"], 1, 1)
            assert_is_not_none(response)

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_post:
            mock_post.return_value.ok = True
            response = self.chains_client.search_chains(["123"], -1, 1)
            assert_is_not_none(response)


class TestChainsClientWithSigning(TestCase):
    """Test chains client with automatic signing"""

    def setUp(self):
        self.chains_client = ChainsClient("https://apicast.io", "123456", "123456789", True)

    def tearDown(self):
        self.chains_client = None

    def test_create_chain(self):
        """Check create chain"""
        with assert_raises(Exception) as cm:
            self.chains_client.create_chain("123", "123")
        assert_true("external_ids must be an array." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.chains_client.create_chain("123", [])
        assert_true("signer_private_key is required." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.chains_client.create_chain("123", [], "idsec")
        assert_true("signer_private_key is invalid." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.chains_client.create_chain("123", [], "idsec1Xbja4exmHFNgVSsk7VipNi4mwt6BjQFEZFCohs4Y7TzfhHoy6")
        assert_true("signer_chain_id is required." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_post:
            mock_post.return_value.ok = True
            response = self.chains_client.create_chain("123", [], "idsec1Xbja4exmHFNgVSsk7VipNi4mwt6BjQFEZFCohs4Y7TzfhHoy6",
                                            "171e5851451ce6f2d9730c1537da4375feb442870d835c54a1bca8ffa7e2bda7")
        assert_is_not_none(response)

