from nose.tools import *
from unittest import TestCase
from unittest.mock import patch
from factom_sdk.utils.entry_util import EntryUtil
from factom_sdk.request_handler.request_handler import RequestHandler


class TestEntryUtil(TestCase):
    def setUp(self):
        self.request_handler = RequestHandler('http://google.com', '1', '2')

    def tearDown(self):
        self.request_handler = None

    def test_get_entry_info(self):
        """Check get entry info"""
        with assert_raises(Exception) as cm:
            EntryUtil.get_entry_info("", "", False, self.request_handler)
        assert_true("chain_id is required." in str(cm.exception))

        with assert_raises(Exception) as cm:
            EntryUtil.get_entry_info("123", "", False, self.request_handler)
        assert_true("entry_hash is required." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = EntryUtil.get_entry_info("123", "123", False, self.request_handler)
            assert_is_not_none(response)

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True

            def signature_validation(params: dict):
                return "valid_signature"

            response = EntryUtil.get_entry_info("123", "123", signature_validation, self.request_handler)
            assert_is_not_none(response)

    def test_validate_signature(self):
        """Check validate signature"""
        entry = {
            "data": {
                "external_ids": [
                    'SignedEntry',
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
            response = EntryUtil.validate_signature(entry, self.request_handler)
            assert_is_not_none(response)

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            json = [{
                "key": "idpub3NegGMKn2CDcx3A9JkpoMm2jE9KxchxqHTmXPvJnmUJGizfrb7"
            }]
            mock_get.return_value.ok = True
            mock_get.return_value.json.return_value = json
            response = EntryUtil.validate_signature(entry, self.request_handler)
            assert_is_not_none(response)

    def test_create_entry(self):
        """Check create entry"""
        with assert_raises(Exception) as cm:
            EntryUtil.create_entry("", False, "")
        assert_true("chain_id is required." in str(cm.exception))

        with assert_raises(Exception) as cm:
            EntryUtil.create_entry("123", False, "")
        assert_true("at least 1 external_ids is required." in str(cm.exception))

        with assert_raises(Exception) as cm:
            EntryUtil.create_entry("123", False, "", "123")
        assert_true("external_ids must be an array." in str(cm.exception))

        with assert_raises(Exception) as cm:
            EntryUtil.create_entry("123", False, "", ["123"], "idsec")
        assert_true("signer_chain_id is required when passing a signer_private_key." in str(cm.exception))

        with assert_raises(Exception) as cm:
            EntryUtil.create_entry("123", False, "", ["123"], "idsec", "123")
        assert_true("signer_private_key is invalid." in str(cm.exception))

        with assert_raises(Exception) as cm:
            EntryUtil.create_entry("123", False, "", ["123"], "", "123")
        assert_true("signer_private_key is required when passing a signer_chain_id." in str(cm.exception))

        with assert_raises(Exception) as cm:
            EntryUtil.create_entry("123", False, "", ["123"])
        assert_true("content is required." in str(cm.exception))

        with assert_raises(Exception) as cm:
            EntryUtil.create_entry("123", True, "", "123", "idsec", "123")
        assert_true("external_ids must be an array." in str(cm.exception))

        with assert_raises(Exception) as cm:
            EntryUtil.create_entry("123", True, "", ["123"], "", "")
        assert_true("signer_private_key is required." in str(cm.exception))

        with assert_raises(Exception) as cm:
            EntryUtil.create_entry("123", True, "", ["123"], "idsec", "")
        assert_true("signer_private_key is invalid." in str(cm.exception))

        with assert_raises(Exception) as cm:
            EntryUtil.create_entry("123", True, "", ["123"], "idsec1Xbja4exmHFNgVSsk7VipNi4mwt6BjQFEZFCohs4Y7TzfhHoy6", "")
        assert_true("signer_chain_id is required." in str(cm.exception))

        with assert_raises(Exception) as cm:
            EntryUtil.create_entry("123", True, "123", ["123"], "idsec1Xbja4exmHFNgVSsk7VipNi4mwt6BjQFEZFCohs4Y7TzfhHoy6",
                                   "123", "google")
        assert_true("callback_url is an invalid url format." in str(cm.exception))

        with assert_raises(Exception) as cm:
            EntryUtil.create_entry("123", True, "123", ["123"], "idsec1Xbja4exmHFNgVSsk7VipNi4mwt6BjQFEZFCohs4Y7TzfhHoy6",
                                   "123", "", "123")
        assert_true("callback_stages must be an array." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_post:
            mock_post.return_value.ok = True
            response = EntryUtil.create_entry("123", True, "123", ["123"], "idsec1Xbja4exmHFNgVSsk7VipNi4mwt6BjQFEZFCohs4Y7TzfhHoy6",
                                   "123", "http://google.com", ["123"], self.request_handler)
        assert_is_not_none(response)

    def test_get_entries(self):
        """Check get entries"""
        with assert_raises(Exception) as cm:
            EntryUtil.get_entries("")
        assert_true("chain_id is required." in str(cm.exception))

        with assert_raises(Exception) as cm:
            EntryUtil.get_entries("123", "1")
        assert_true("limit must be an integer." in str(cm.exception))

        with assert_raises(Exception) as cm:
            EntryUtil.get_entries("123", 1, "1")
        assert_true("offset must be an integer." in str(cm.exception))

        with assert_raises(Exception) as cm:
            EntryUtil.get_entries("123", 1, 1, "1")
        assert_true("stages must be an array." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = EntryUtil.get_entries("123", 1, 1, ["1"], self.request_handler)
        assert_is_not_none(response)

    def test_get_first_entry(self):
        """Check get first entry"""
        with assert_raises(Exception) as cm:
            EntryUtil.get_first_entry("")
        assert_true("chain_id is required." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = EntryUtil.get_first_entry("123", self.request_handler)
        assert_is_not_none(response)

    def test_get_last_entry(self):
        """Check get last entry"""
        with assert_raises(Exception) as cm:
            EntryUtil.get_last_entry("")
        assert_true("chain_id is required." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = EntryUtil.get_last_entry("123", self.request_handler)
        assert_is_not_none(response)

    def test_search_entries(self):
        """Check search entries"""
        with assert_raises(Exception) as cm:
            EntryUtil.search_entries("", [])
        assert_true("chain_id is required." in str(cm.exception))

        with assert_raises(Exception) as cm:
            EntryUtil.search_entries("123", [])
        assert_true("at least 1 external_ids is required." in str(cm.exception))

        with assert_raises(Exception) as cm:
            EntryUtil.search_entries("123", "123")
        assert_true("external_ids must be an array." in str(cm.exception))

        with assert_raises(Exception) as cm:
            EntryUtil.search_entries("123", ["1"], "1")
        assert_true("limit must be an integer." in str(cm.exception))

        with assert_raises(Exception) as cm:
            EntryUtil.search_entries("123", ["1"], 1, "1")
        assert_true("offset must be an integer." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_post:
            mock_post.return_value.ok = True
            response = EntryUtil.search_entries("123", ["1"], 1, 1, self.request_handler)
        assert_is_not_none(response)

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_post:
            mock_post.return_value.ok = True
            response = EntryUtil.search_entries("123", ["1"], -1, 1, self.request_handler)
        assert_is_not_none(response)
