from nose.tools import *
from unittest import TestCase
from unittest.mock import patch
from factom_sdk.client.identity_client import IdentityClient
from factom_sdk.request_handler.request_handler import RequestHandler


class TestIdentityClient(TestCase):
    def setUp(self):
        self.identity_client = IdentityClient({
            "base_url": "https://apicast.io",
            "app_id": "123456",
            "app_key": "123456789"
        })

    def tearDown(self):
        self.identity_client = None

    def test_init(self):
        """Check init identity client"""
        assert_true(isinstance(self.identity_client.request_handler, RequestHandler))

    def test_create_identity_key_pair(self):
        """Check create identity key pair"""
        key_pairs = self.identity_client.create_identity_key_pair()
        assert_true(len(key_pairs) == 3)

    def test_create_identity(self):
        """Check create identity"""
        with assert_raises(Exception) as cm:
            self.identity_client.create_identity()
        assert_true("name is required." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.identity_client.create_identity({"name": "123"})
        assert_true("name must be an array." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.identity_client.create_identity({"name": ["123"]})
        assert_true("at least 1 key is required." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.identity_client.create_identity({
                "name": ["123"],
                "keys": "idpub",
            })
        assert_true("keys must be an array." in str(cm.exception))
        with assert_raises(Exception) as cm:
            self.identity_client.create_identity({
                "name": ["123"],
                "keys": "idpub",
            })
        assert_true("keys must be an array." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.identity_client.create_identity({
                "name": ["123"],
                "keys": ["idpub"],
                "callback_stages": "factom"
            })
        assert_true("callback_stages must be an array." in str(cm.exception))

        with assert_raises(Exception) as cm:
            errors = [
                {
                    "key": "123",
                    "error": "key is invalid",
                },
                {
                    "key": "123",
                    "error": "key is invalid",
                },
            ]
            self.identity_client.create_identity({
                "name": ["123"],
                "keys": [
                    "123",
                    "123",
                    "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                ]
            })
        assert_true(str(errors) in str(cm.exception))

        with assert_raises(Exception) as cm:
            errors = [
                {
                    "key": "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                    "error": "key is duplicated, keys must be unique.",
                },
            ]
            self.identity_client.create_identity({
                "name": ["123"],
                "keys": [
                    "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                    "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                    "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                ]
            })
        assert_true(str(errors) in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.identity_client.create_identity({
                "name": ["123"],
                "keys": [
                    "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                    "idpub2FEZg6PwVuDXfsxEMinnqVfgjuNS2GzMSQwJgTdmUFQaoYpTnv",
                    "idpub1tkTRwxonwCfsvTkk5enWzbZgQSRpWDYtdzPUnq83AgQtecSgc",
                ],
                "callback_url": "callback.com",
                "callback_stages": ["factom", "replicated"],
            })
        assert_true("callback_url is an invalid url format." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.identity_client.create_identity({
                "name": [
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already",
                    "The primary benefit of using Identities within your application the ability to verify that a certain user/device/organization/etc. actually signed and published a certain message that you see in your chain. Let is go through an example of how this creation of a signed entry works for an identity we made already", ],
                "keys": [
                    "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                    "idpub2FEZg6PwVuDXfsxEMinnqVfgjuNS2GzMSQwJgTdmUFQaoYpTnv",
                    "idpub1tkTRwxonwCfsvTkk5enWzbZgQSRpWDYtdzPUnq83AgQtecSgc",
                ],
                "callback_url": "https://callback.com",
                "callback_stages": ["factom", "replicated"],
            })
        assert_true("calculated bytes of name and keys is 16931. It must be less than 10240, use less/shorter name or less keys." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.post") as mock_post:
            mock_post.return_value.ok = True
            response = self.identity_client.create_identity({
                "name": ["123"],
                "keys": [
                    "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                    "idpub2FEZg6PwVuDXfsxEMinnqVfgjuNS2GzMSQwJgTdmUFQaoYpTnv",
                    "idpub1tkTRwxonwCfsvTkk5enWzbZgQSRpWDYtdzPUnq83AgQtecSgc",
                ],
                "callback_url": "https://callback.com",
                "callback_stages": ["factom", "replicated"],
            })
            assert_is_not_none(response)

    def test_get_identity(self):
        """Check get identity"""
        with assert_raises(Exception) as cm:
            self.identity_client.get_identity({
                "identity_chain_id": ""
            })
        assert_true("identity_chain_id is required." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.get") as mock_get:
            mock_get.return_value.ok = True
            response = self.identity_client.get_identity({
                "identity_chain_id": "1214124"
            })
            assert_is_not_none(response)

    def test_get_all_identity_keys(self):
        """Check get all identity keys """
        with assert_raises(Exception) as cm:
            self.identity_client.get_all_identity_keys({
                "identity_chain_id": ""
            })
        assert_true("identity_chain_id is required." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.identity_client.get_all_identity_keys({
                "identity_chain_id": "123124",
                "active_at_height": "123",
            })
        assert_true("active_at_height must be an integer." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.identity_client.get_all_identity_keys({
                "identity_chain_id": "123124",
                "active_at_height": 123,
                "limit": "12312"
            })
        assert_true("limit must be an integer." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.identity_client.get_all_identity_keys({
                "identity_chain_id": "123124",
                "active_at_height": 123,
                "limit": 12312,
                "offset": "123124"
            })
        assert_true("offset must be an integer." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.get") as mock_get:
            mock_get.return_value.ok = True
            response =  self.identity_client.get_all_identity_keys({
                "identity_chain_id": "123124",
                "active_at_height": 123,
                "limit": 12312,
                "offset": 123
            })
            assert_is_not_none(response)

    def test_create_identity_key_replacement(self):
        """Check create identity key replacement"""
        with assert_raises(Exception) as cm:
            self.identity_client.create_identity_key_replacement({
                "identity_chain_id": ""
            })
        assert_true("identity_chain_id is required." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.identity_client.create_identity_key_replacement({
                "identity_chain_id": "123",
            })
        assert_true("old_public_key is required." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.identity_client.create_identity_key_replacement({
                "identity_chain_id": "123",
                "old_public_key": "idpub1"
            })
        assert_true("new_public_key is required." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.identity_client.create_identity_key_replacement({
                "identity_chain_id": "123",
                "old_public_key": "idpub1",
                "new_public_key": "idpub2",
            })
        assert_true("signer_private_key is required." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.identity_client.create_identity_key_replacement({
                "identity_chain_id": "123",
                "old_public_key": "idpub1",
                "new_public_key": "idpub2",
            })
        assert_true("signer_private_key is required." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.identity_client.create_identity_key_replacement({
                "identity_chain_id": "123",
                "old_public_key": "idpub1",
                "new_public_key": "idpub2",
                "signer_private_key": "idsec1"
            })
        assert_true("old_public_key is an invalid public key." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.identity_client.create_identity_key_replacement({
                "identity_chain_id": "123",
                "old_public_key": "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                "new_public_key": "idpub2",
                "signer_private_key": "idsec1"
            })
        assert_true("new_public_key is an invalid public key." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.identity_client.create_identity_key_replacement({
                "identity_chain_id": "123",
                "old_public_key": "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                "new_public_key": "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                "signer_private_key": "idsec1"
            })
        assert_true("signer_private_key is invalid." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.identity_client.create_identity_key_replacement({
                "identity_chain_id": "123",
                "old_public_key": "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                "new_public_key": "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                "signer_private_key": "idsec1Xbja4exmHFNgVSsk7VipNi4mwt6BjQFEZFCohs4Y7TzfhHoy6",
                "callback_stages": "factom"
            })
        assert_true("callback_stages must be an array." in str(cm.exception))

        with assert_raises(Exception) as cm:
            self.identity_client.create_identity_key_replacement({
                "identity_chain_id": "123",
                "old_public_key": "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                "new_public_key": "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                "signer_private_key": "idsec1Xbja4exmHFNgVSsk7VipNi4mwt6BjQFEZFCohs4Y7TzfhHoy6",
                "callback_stages": ["factom", "test"],
                "callback_url": "appcast.io"
            })
        assert_true("callback_url is an invalid url format." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.post") as mock_post:
            mock_post.return_value.ok = True
            response = self.identity_client.create_identity_key_replacement({
                "identity_chain_id": "123",
                "old_public_key": "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                "new_public_key": "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                "signer_private_key": "idsec1Xbja4exmHFNgVSsk7VipNi4mwt6BjQFEZFCohs4Y7TzfhHoy6",
                "callback_stages": ["factom", "test"],
                "callback_url": "https://appcast.io"
            })
            assert_is_not_none(response)







