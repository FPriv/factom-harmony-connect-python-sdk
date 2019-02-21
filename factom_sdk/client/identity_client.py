import validators
import base64
from factom_sdk.utils.key_util import KeyUtil
from factom_sdk.request_handler.request_handler import RequestHandler

IDENTITY_URL = "identities"
KEYS_STRING = "keys"
UTF8_ENCODE = "utf-8"


class IdentityClient:
    def __init__(self, base_url: str, app_id: str, app_key: str):
        self.request_handler = RequestHandler(base_url, app_id, app_key)

    # noinspection PyMethodMayBeStatic
    def create_identity_key_pair(self, number_of_key_pair: int = 3):
        return [KeyUtil.create_key_pair() for _ in list(range(number_of_key_pair))]

    def create_identity(self, name: list, keys: list, callback_url: str = "", callback_stages: list = None):
        if callback_stages is None:
            callback_stages = []
        if not name:
            raise Exception("name is required.")
        if not isinstance(name, list):
            raise Exception("name must be an array.")
        if not keys:
            raise Exception("at least 1 key is required.")
        if not isinstance(keys, list):
            raise Exception("keys must be an array.")
        if not isinstance(callback_stages, list):
            raise Exception("callback_stages must be an array.")
        invalid_keys = KeyUtil.get_invalid_keys(keys)
        if len(invalid_keys) > 0:
            raise Exception(invalid_keys)
        duplicate_keys = KeyUtil.get_duplicate_keys(keys)
        if len(duplicate_keys) > 0:
            raise Exception(duplicate_keys)
        if callback_url and not validators.url(callback_url):
            raise Exception("callback_url is an invalid url format.")
        name_base64 = [base64.b64encode(_name.encode(UTF8_ENCODE)) for _name in name]
        name_byte_count = 0
        for name in name_base64:
            name_byte_count += len(name)
        total_bytes = 37 + name_byte_count + (len(name_base64) * 2) + (len(keys) * 58)
        if total_bytes > 10240:
            raise Exception("calculated bytes of name and keys is " + str(total_bytes) +
                            ". It must be less than 10240, use less/shorter name or less keys.")
        data = {
            "name": name_base64,
            "keys": keys
        }
        if callback_url:
            data["callback_url"] = callback_url
        if callback_stages:
            data["callback_stages"] = callback_stages
        return self.request_handler.post(IDENTITY_URL, data)

    def get_identity(self, identity_chain_id: str):
        if not identity_chain_id:
            raise Exception("identity_chain_id is required.")
        return self.request_handler.get("/".join([IDENTITY_URL, identity_chain_id]))

    def get_all_identity_keys(self, identity_chain_id: str, active_at_height: int = -1, limit: int = -1,
                              offset: int = -1):
        if not identity_chain_id:
            raise Exception("identity_chain_id is required.")
        data = {}
        if not isinstance(active_at_height, int):
            raise Exception("active_at_height must be an integer.")
        if active_at_height > -1:
            data["active_at_height"] = active_at_height
        if not isinstance(limit, int):
            raise Exception("limit must be an integer.")
        if limit > -1:
            data["limit"] = limit
        if not isinstance(offset, int):
            raise Exception("offset must be an integer.")
        if offset > -1:
            data["offset"] = offset
        return self.request_handler.get("/".join([IDENTITY_URL, identity_chain_id, KEYS_STRING]), data)

    def create_identity_key_replacement(self, identity_chain_id: str, old_public_key: str, new_public_key: str,
                                        signer_private_key: str, callback_url: str = "", callback_stages: list = None):
        if callback_stages is None:
            callback_stages = []
        if not identity_chain_id:
            raise Exception("identity_chain_id is required.")
        if not old_public_key:
            raise Exception("old_public_key is required.")
        if not new_public_key:
            raise Exception("new_public_key is required.")
        if not signer_private_key:
            raise Exception("signer_private_key is required.")
        if not KeyUtil.validate_checksum(old_public_key):
            raise Exception("old_public_key is an invalid public key.")
        if not KeyUtil.validate_checksum(new_public_key):
            raise Exception("new_public_key is an invalid public key.")
        if not KeyUtil.validate_checksum(signer_private_key):
            raise Exception("signer_private_key is invalid.")
        if not isinstance(callback_stages, list):
            raise Exception("callback_stages must be an array.")
        if callback_url and not validators.url(callback_url):
            raise Exception("callback_url is an invalid url format.")
        message = identity_chain_id + old_public_key + new_public_key
        signature = KeyUtil.sign_content(signer_private_key, message)
        signer_key = KeyUtil.get_public_key_from_private_key(signer_private_key)
        data = {
            "old_key": old_public_key,
            "new_key": new_public_key,
            "signature": signature,
            "signer_key": signer_key
        }
        if callback_url:
            data["callback_url"] = callback_url
        if callback_stages:
            data["callback_stages"] = callback_stages
        return self.request_handler.post("/".join([IDENTITY_URL, identity_chain_id, KEYS_STRING]), data)
