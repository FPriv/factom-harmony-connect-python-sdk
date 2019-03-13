from unittest import TestCase
from factom_sdk.utils.common_util import CommonUtil


class TestCommonUtil(TestCase):
    """Test Request Handler Params"""

    def test_decode_empty_object(self):
        """Check decode response empty"""
        self.assertEqual(CommonUtil.decode_response(), {})

    def test_decode_data_array(self):
        """Check decode response data array"""
        data = {
            "data": [{
                "version": 1,
                "stage": "anchored",
                "created_height": 118460,
                "chain_id": "171e5851451ce6f2d9730c1537da4375feb442870d835c54a1bca8ffa7e2bda7",
                "all_keys_href": "/v1/identities/<chain_id>/keys",
                "external_ids": [
                    "U2lnbmVkRW50cnk=",
                    "AQ==",
                    "MTcxZTU4NTE0NTFjZTZmMmQ5NzMwYzE1MzdkYTQzNzVmZWI0NDI4NzBkODM1YzU0YTFiY2E4ZmZhN2UyYmRhNw==",
                    "aWRwdWIzTmVnR01LbjJDRGN4M0E5Smtwb01tMmpFOUt4Y2h4cUhUbVhQdkpubVVKR2l6ZnJiNw==",
                    "d5Ip0jzbc4CGnmPlFWpUlxcLzuwTmzfnrypNGq4U0FPRn3Ym4I1LuwA9SwXZQfQ0AvEoivL/A5Gi3uSr8JGbBw==",
                    "MjAxOS0wMS0xOFQxNDoxNzo1MFo=",
                ],
            }],
            "offset": 0,
            "limit": 15,
            "count": 1,
        }
        decoded_data = {
            "data": [{
                "version": 1,
                "stage": "anchored",
                "created_height": 118460,
                "chain_id": "171e5851451ce6f2d9730c1537da4375feb442870d835c54a1bca8ffa7e2bda7",
                "all_keys_href": "/v1/identities/<chain_id>/keys",
                "external_ids": [
                    "SignedEntry",
                    "0x01",
                    "171e5851451ce6f2d9730c1537da4375feb442870d835c54a1bca8ffa7e2bda7",
                    "idpub3NegGMKn2CDcx3A9JkpoMm2jE9KxchxqHTmXPvJnmUJGizfrb7",
                    "779229d23cdb7380869e63e5156a5497170bceec139b37e7af2a4d1aae14d053d19f7626e08d4bbb003d4b05d941f43402f1288af2ff0391a2dee4abf0919b07",
                    "2019-01-18T14:17:50Z",
                ],
            }],
            "offset": 0,
            "limit": 15,
            "count": 1,
        }
        response = CommonUtil.decode_response(data)
        self.assertEqual(response, decoded_data)

    def test_decode_data_object(self):
        """Check decode response data object"""
        data = {
            "data": {
                "version": 1,
                "stage": "anchored",
                "created_height": 118460,
                "chain_id": "171e5851451ce6f2d9730c1537da4375feb442870d835c54a1bca8ffa7e2bda7",
                "all_keys_href": "/v1/identities/<chain_id>/keys",
                "external_ids": [
                    "U2lnbmVkRW50cnk=",
                    "AQ==",
                    "MTcxZTU4NTE0NTFjZTZmMmQ5NzMwYzE1MzdkYTQzNzVmZWI0NDI4NzBkODM1YzU0YTFiY2E4ZmZhN2UyYmRhNw==",
                    "aWRwdWIzTmVnR01LbjJDRGN4M0E5Smtwb01tMmpFOUt4Y2h4cUhUbVhQdkpubVVKR2l6ZnJiNw==",
                    "d5Ip0jzbc4CGnmPlFWpUlxcLzuwTmzfnrypNGq4U0FPRn3Ym4I1LuwA9SwXZQfQ0AvEoivL/A5Gi3uSr8JGbBw==",
                    "MjAxOS0wMS0xOFQxNDoxNzo1MFo=",
                ],
            },
        }
        decoded_data = {
            "data": {
                "version": 1,
                "stage": "anchored",
                "created_height": 118460,
                "chain_id": "171e5851451ce6f2d9730c1537da4375feb442870d835c54a1bca8ffa7e2bda7",
                "all_keys_href": "/v1/identities/<chain_id>/keys",
                "external_ids": [
                    "SignedEntry",
                    "0x01",
                    "171e5851451ce6f2d9730c1537da4375feb442870d835c54a1bca8ffa7e2bda7",
                    "idpub3NegGMKn2CDcx3A9JkpoMm2jE9KxchxqHTmXPvJnmUJGizfrb7",
                    "779229d23cdb7380869e63e5156a5497170bceec139b37e7af2a4d1aae14d053d19f7626e08d4bbb003d4b05d941f43402f1288af2ff0391a2dee4abf0919b07",
                    "2019-01-18T14:17:50Z",
                ],
            },
        }
        response = CommonUtil.decode_response(data)
        self.assertEqual(response, decoded_data)

        data = {
            "data": {
                "version": 1,
                "stage": "anchored",
                "created_height": 118460,
                "chain_id": "171e5851451ce6f2d9730c1537da4375feb442870d835c54a1bca8ffa7e2bda7",
                "all_keys_href": "/v1/identities/<chain_id>/keys",
                "names": "RU1QTE9ZRUU=",
            },
        }
        decoded_data = {
            "data": {
                "version": 1,
                "stage": "anchored",
                "created_height": 118460,
                "chain_id": "171e5851451ce6f2d9730c1537da4375feb442870d835c54a1bca8ffa7e2bda7",
                "all_keys_href": "/v1/identities/<chain_id>/keys",
                "names": "EMPLOYEE",
            },
        }
        response = CommonUtil.decode_response(data)
        self.assertEqual(response, decoded_data)
