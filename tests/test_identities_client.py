from unittest import TestCase
from unittest.mock import patch
from factom_sdk.client.identities_client import IdentitiesClient
from factom_sdk.request_handler.request_handler import RequestHandler


class TestIdentityClient(TestCase):
    def setUp(self):
        self.identities_client = IdentitiesClient("https://apicast.io", "123456", "123456789")

    def tearDown(self):
        self.identities_client = None

    def test_init(self):
        """Check init identity client"""
        self.assertTrue(isinstance(self.identities_client.request_handler, RequestHandler))

    def test_create(self):
        """Check create identity"""
        with self.assertRaises(Exception) as cm:
            self.identities_client.create("")
        self.assertTrue("at least 1 name is required." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identities_client.create("123")
        self.assertTrue("names must be an array." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identities_client.create(["123"], keys=[])
        self.assertTrue("at least 1 key is required." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identities_client.create(["123"], keys="123")
        self.assertTrue("keys must be an array." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identities_client.create(["123"], keys=["idpub"], callback_stages="factom")
        self.assertTrue("callback_stages must be an array." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
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
            self.identities_client.create(["123"], keys=[
                "123",
                "123",
                "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9"
            ])
        self.assertTrue(str(errors) in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            errors = [
                {
                    "key": "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                    "error": "key is duplicated, keys must be unique.",
                },
            ]
            self.identities_client.create(["123"], keys=[
                "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
            ])
        self.assertTrue(str(errors) in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identities_client.create(["123"], keys=[
                "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                "idpub2FEZg6PwVuDXfsxEMinnqVfgjuNS2GzMSQwJgTdmUFQaoYpTnv",
                "idpub1tkTRwxonwCfsvTkk5enWzbZgQSRpWDYtdzPUnq83AgQtecSgc",
            ], callback_url="callback.com",
                                          callback_stages=["factom", "replicated"])
        self.assertTrue("callback_url is an invalid url format." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identities_client.create([
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
                callback_url="https://callback.com",
                callback_stages=["factom", "replicated"]
            )
        self.assertTrue("Entry size 12771 must be less than 10240. Use less/shorter names or less keys."
                        in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_post:
            mock_post.return_value.ok = True
            response = self.identities_client.create(
                ["123"],
                callback_url="https://callback.com",
                callback_stages=["factom", "replicated"]
            )
            self.assertIsNotNone(response)

    def test_get(self):
        """Check get identity"""
        with self.assertRaises(Exception) as cm:
            self.identities_client.get("")
        self.assertTrue("identity_chain_id is required." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = self.identities_client.get("123")
            self.assertIsNotNone(response)

    def test_key_get(self):
        """Check get identity key"""
        with self.assertRaises(Exception) as cm:
            self.identities_client.keys.get("", "")
        self.assertTrue("identity_chain_id is required." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identities_client.keys.get("123", "")
        self.assertTrue("key is required." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identities_client.keys.get("123", "idpub")
        self.assertTrue("key is invalid." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = self.identities_client.keys.get("123", "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9")
            self.assertIsNotNone(response)

    def test_key_list(self):
        """Check get all identity keys """
        with self.assertRaises(Exception) as cm:
            self.identities_client.keys.list("")
        self.assertTrue("identity_chain_id is required." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identities_client.keys.list("123", limit="123", offset="123")
        self.assertTrue("limit must be an integer." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identities_client.keys.list("123", limit=123, offset="123")
        self.assertTrue("offset must be an integer." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = self.identities_client.keys.list("123", limit=123, offset=123)
            self.assertIsNotNone(response)

    def test_key_replace(self):
        """Check create identity key replacement"""
        with self.assertRaises(Exception) as cm:
            self.identities_client.keys.replace("", "", "")
        self.assertTrue("identity_chain_id is required." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identities_client.keys.replace("123", "", "")
        self.assertTrue("old_public_key is required." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identities_client.keys.replace("123", "123", "")
        self.assertTrue("signer_private_key is required." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identities_client.keys.replace("123", "123", "123", new_public_key="")
        self.assertTrue("new_public_key is required." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identities_client.keys.replace("123", "idpub1", "idsec")
        self.assertTrue("old_public_key is an invalid public key." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identities_client.keys.replace("123",
                                                "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                                                "idsec")
        self.assertTrue("signer_private_key is invalid." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identities_client.keys.replace("123",
                                                "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                                                "idsec1Xbja4exmHFNgVSsk7VipNi4mwt6BjQFEZFCohs4Y7TzfhHoy6",
                                                new_public_key="idpub2")
        self.assertTrue("new_public_key is an invalid public key." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identities_client.keys.replace("123",
                                                "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                                                "idsec1Xbja4exmHFNgVSsk7VipNi4mwt6BjQFEZFCohs4Y7TzfhHoy6",
                                                new_public_key="idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                                                callback_stages="factom")
        self.assertTrue("callback_stages must be an array." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identities_client.keys.replace("123",
                                                "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                                                "idsec1Xbja4exmHFNgVSsk7VipNi4mwt6BjQFEZFCohs4Y7TzfhHoy6",
                                                new_public_key="idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                                                callback_url="io.com", callback_stages=["factom"])
        self.assertTrue("callback_url is an invalid url format." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_post:
            mock_post.return_value.ok = True
            response = self.identities_client.keys.replace("123",
                                                           "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                                                           "idsec1Xbja4exmHFNgVSsk7VipNi4mwt6BjQFEZFCohs4Y7TzfhHoy6")
            self.assertIsNotNone(response)
