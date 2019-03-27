from unittest import TestCase
from unittest.mock import patch, Mock
from requests import HTTPError
from factom_sdk.request_handler.request_handler import RequestHandler
from factom_sdk.utils.validate_signature_util import ValidateSignatureUtil


class TestValidateSignatureUtil(TestCase):
    def setUp(self):
        self.request_handler = RequestHandler('http://google.com', '1', '2')

    def tearDown(self):
        self.request_handler = None

    def test_validate_signature(self):
        """Check validate signature"""
        data = {
            "data": {
                "external_ids": [
                    'SignedChain'
                ],
                "dblock": {
                    "height": 10000
                },
                "content": "123"
            }
        }
        result = ValidateSignatureUtil.validate_signature(data, True, self.request_handler)
        self.assertEqual("not_signed/invalid_chain_format", result)

        data = {
            "data": {
                "external_ids": [
                    'SignedChain',
                    '0x01',
                    '171e5851451ce6f2d9730c1537da4375feb442870d835c54a1bca8ffa7e2bda7',
                    'idpub',
                    '779229d23cdb7380869e63e5156a5497170bceec139b37e7af2a4d1aae14d053d19f7626e08d4bbb003d4b05d941f43402f1288af2ff0391a2dee4abf0919b07',
                    '2019-01-18T14:17:50Z',
                ],
                "dblock": {
                    "height": 10000
                },
                "content": "123"
            }
        }
        result = ValidateSignatureUtil.validate_signature(data, True, self.request_handler)
        self.assertEqual("not_signed/invalid_chain_format", result)

        data = {
            "data": {
                "external_ids": [
                    'SignedChain',
                    '0x01',
                    '171e5851451ce6f2d9730c1537da4375feb442870d835c54a1bca8ffa7e2bda7',
                    'idpub3NegGMKn2CDcx3A9JkpoMm2jE9KxchxqHTmXPvJnmUJGizfrb7',
                    '779229d23cdb7380869e63e5156a5497170bceec139b37e7af2a4d1aae14d053d19f7626e08d4bbb003d4b05d941ty3402f1288af2ff0391a2dee4abf0919b07',
                    '2019-01-18T14:17:50Z',
                ],
                "dblock": {
                    "height": 10000
                },
                "content": "123"
            }
        }
        result = ValidateSignatureUtil.validate_signature(data, True, self.request_handler)
        self.assertEqual("not_signed/invalid_chain_format", result)

        data = {
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
            mock_error = HTTPError()
            mock_error.response = Mock()
            mock_error.response.status_code = 404
            mock_get.side_effect = mock_error
            response = ValidateSignatureUtil.validate_signature(data, True, self.request_handler)
            self.assertEqual("key_not_found", response)

        with self.assertRaises(HTTPError) as cm:
            with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
                mock_error = HTTPError()
                mock_error.response = Mock()
                mock_error.response.status_code = 500
                mock_get.side_effect = mock_error
                ValidateSignatureUtil.validate_signature(data, True, self.request_handler)
        self.assertTrue("" in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            json = {
                "data": {
                    "key": "123",
                    "retired_height": 1001,
                    "activated_height": 1001,
                }
            }
            mock_get.return_value.ok = True
            mock_get.return_value.json.return_value = json
            response = ValidateSignatureUtil.validate_signature(data, True, self.request_handler)
            self.assertEqual("retired_key", response)

        data = {
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
                    "height": 1000
                },
                "content": "123"
            }
        }

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            json = {
                "data": {
                    "key": "123",
                    "retired_height": 900,
                    "activated_height": 1001,
                }
            }
            mock_get.return_value.ok = True
            mock_get.return_value.json.return_value = json
            response = ValidateSignatureUtil.validate_signature(data, False, self.request_handler)
            self.assertEqual("retired_key", response)

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            json = {
                "data": {
                    "key": "idpub3NegGMKn2CDcx3A9JkpoMm2jE9KxchxqHTmXPvJnmUJGizfrb7",
                    "retired_height": 1001,
                    "activated_height": 900,
                }
            }
            mock_get.return_value.ok = True
            mock_get.return_value.json.return_value = json
            response = ValidateSignatureUtil.validate_signature(data, False, self.request_handler)
            self.assertEqual("invalid_signature", response)
