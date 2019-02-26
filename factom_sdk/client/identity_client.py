import validators
import factom_sdk.utils.consts
from factom_sdk.utils.common_util import CommonUtil
from factom_sdk.utils.key_util import KeyUtil
from factom_sdk.request_handler.request_handler import RequestHandler


class IdentityClient:
    def __init__(self, base_url: str, app_id: str, app_key: str):
        self.request_handler = RequestHandler(base_url, app_id, app_key)

    def create_identity_key_pair(self, number_of_key_pair: int = 3):
        return [KeyUtil.create_key_pair() for _ in range(number_of_key_pair)]

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
        name_byte_count = 0
        for _name in name:
            name_byte_count += len(_name)

        # 2 bytes for the size of extid + 13 for actual IdentityChain ext-id text
        # 2 bytes per name for size * (number of names) + size of all names
        # 23 bytes for `{"keys":[],"version":1}`
        # 58 bytes per `"idpub2PHPArpDF6S86ys314D3JDiKD8HLqJ4HMFcjNJP6gxapoNsyFG",` array element
        # -1 byte because last key element has no comma
        # = 37 + name_byte_count + 2(number_of_names) + 58(number_of_keys)
        total_bytes = 37 + name_byte_count + (len(name) * 2) + (len(keys) * 58)
        if total_bytes > 10240:
            raise Exception("calculated bytes of name and keys is " + str(total_bytes) +
                            ". It must be less than 10240, use less/shorter name or less keys.")

        name_base64 = [CommonUtil.base64_encode(_name) for _name in name]
        data = {
            "name": name_base64,
            "keys": keys
        }
        if callback_url:
            data["callback_url"] = callback_url
        if callback_stages:
            data["callback_stages"] = callback_stages
        return self.request_handler.post(factom_sdk.utils.consts.IDENTITY_URL, data)

    def get_identity(self, identity_chain_id: str):
        if not identity_chain_id:
            raise Exception("identity_chain_id is required.")
        return self.request_handler.get("/".join([factom_sdk.utils.consts.IDENTITY_URL, identity_chain_id]))

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
        return self.request_handler.get("/".join([factom_sdk.utils.consts.IDENTITY_URL, identity_chain_id,
                                                  factom_sdk.utils.consts.KEYS_STRING]), data)

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
        return self.request_handler.post("/".join([factom_sdk.utils.consts.IDENTITY_URL, identity_chain_id,
                                                   factom_sdk.utils.consts.KEYS_STRING]), data)
