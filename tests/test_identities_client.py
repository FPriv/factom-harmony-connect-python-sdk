from unittest import TestCase
from unittest.mock import patch
from factom_sdk.client.identity_client import IdentityClient
from factom_sdk.request_handler.request_handler import RequestHandler


class TestIdentityClient(TestCase):
    def setUp(self):
        self.identity_client = IdentityClient("https://apicast.io", "123456", "123456789")

    def tearDown(self):
        self.identity_client = None

    def test_init(self):
        """Check init identity client"""
        self.assertTrue(isinstance(self.identity_client.request_handler, RequestHandler))

    def test_create(self):
        """Check create identity"""
        with self.assertRaises(Exception) as cm:
            self.identity_client.create("", "")
        self.assertTrue("name is required." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identity_client.create("123", "123")
        self.assertTrue("name must be an array." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identity_client.create(["123"], [])
        self.assertTrue("at least 1 key is required." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identity_client.create(["123"], "123")
        self.assertTrue("keys must be an array." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identity_client.create(["123"], ["idpub"], "", "factom")
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
            self.identity_client.create(["123"], [
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
            self.identity_client.create(["123"], [
                "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
            ])
        self.assertTrue(str(errors) in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identity_client.create(["123"], [
                "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                "idpub2FEZg6PwVuDXfsxEMinnqVfgjuNS2GzMSQwJgTdmUFQaoYpTnv",
                "idpub1tkTRwxonwCfsvTkk5enWzbZgQSRpWDYtdzPUnq83AgQtecSgc",
            ], "callback.com", ["factom", "replicated"])
        self.assertTrue("callback_url is an invalid url format." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identity_client.create([
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
                [
                    "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                    "idpub2FEZg6PwVuDXfsxEMinnqVfgjuNS2GzMSQwJgTdmUFQaoYpTnv",
                    "idpub1tkTRwxonwCfsvTkk5enWzbZgQSRpWDYtdzPUnq83AgQtecSgc",
                ],
                "https://callback.com",
                ["factom", "replicated"]
            )
        self.assertTrue(
            "calculated bytes of name and keys is 12771. It must be less than 10240, use less/shorter name or less keys." in str(
                cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_post:
            mock_post.return_value.ok = True
            response = self.identity_client.create(
                ["123"],
                [
                    "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                    "idpub2FEZg6PwVuDXfsxEMinnqVfgjuNS2GzMSQwJgTdmUFQaoYpTnv",
                    "idpub1tkTRwxonwCfsvTkk5enWzbZgQSRpWDYtdzPUnq83AgQtecSgc",
                ],
                "https://callback.com",
                ["factom", "replicated"]
            )
            self.assertIsNotNone(response)

    def test_get(self):
        """Check get identity"""
        with self.assertRaises(Exception) as cm:
            self.identity_client.get("")
        self.assertTrue("identity_chain_id is required." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = self.identity_client.get("123")
            self.assertIsNotNone(response)

    def test_list(self):
        """Check get all identity keys """
        with self.assertRaises(Exception) as cm:
            self.identity_client.keys.list("")
        self.assertTrue("identity_chain_id is required." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identity_client.keys.list("123", "123")
        self.assertTrue("active_at_height must be an integer." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identity_client.keys.list("123", 123, "123")
        self.assertTrue("limit must be an integer." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identity_client.keys.list("123", 123, 123, "123")
        self.assertTrue("offset must be an integer." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_get:
            mock_get.return_value.ok = True
            response = self.identity_client.keys.list("123", 123, 123, 123)
            self.assertIsNotNone(response)

    def test_replace(self):
        """Check create identity key replacement"""
        with self.assertRaises(Exception) as cm:
            self.identity_client.keys.replace("", "", "", "")
        self.assertTrue("identity_chain_id is required." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identity_client.keys.replace("123", "", "", "")
        self.assertTrue("old_public_key is required." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identity_client.keys.replace("123", "123", "", "")
        self.assertTrue("new_public_key is required." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identity_client.keys.replace("123", "123", "123", "")
        self.assertTrue("signer_private_key is required." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identity_client.keys.replace("123", "idpub1", "idpub2", "idsec")
        self.assertTrue("old_public_key is an invalid public key." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identity_client.keys.replace("123",
                                                                 "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                                                                 "idpub2", "idsec")
        self.assertTrue("new_public_key is an invalid public key." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identity_client.keys.replace("123",
                                                                 "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                                                                 "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                                                                 "idsec")
        self.assertTrue("signer_private_key is invalid." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identity_client.keys.replace("123",
                                                                 "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                                                                 "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                                                                 "idsec1Xbja4exmHFNgVSsk7VipNi4mwt6BjQFEZFCohs4Y7TzfhHoy6",
                                                                 "", "factom")
        self.assertTrue("callback_stages must be an array." in str(cm.exception))

        with self.assertRaises(Exception) as cm:
            self.identity_client.keys.replace("123",
                                                                 "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                                                                 "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                                                                 "idsec1Xbja4exmHFNgVSsk7VipNi4mwt6BjQFEZFCohs4Y7TzfhHoy6",
                                                                 "io.com", ["factom"])
        self.assertTrue("callback_url is an invalid url format." in str(cm.exception))

        with patch("factom_sdk.request_handler.request_handler.requests.request") as mock_post:
            mock_post.return_value.ok = True
            response = self.identity_client.keys.replace("123",
                                                                            "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                                                                            "idpub2TWHFrWrJxVEmbeXnMRWeKBdFp7bEByosS1phV1bH7NS99zHF9",
                                                                            "idsec1Xbja4exmHFNgVSsk7VipNi4mwt6BjQFEZFCohs4Y7TzfhHoy6",
                                                                            "https://appcast.io", ["factom"])
            self.assertIsNotNone(response)
