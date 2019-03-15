import validators
import factom_sdk.utils.consts
from factom_sdk.utils.key_common import KeyCommon
from factom_sdk.request_handler.request_handler import RequestHandler


class IdentitiesKeyUtil:
    def __init__(self, base_url: str, app_id: str, app_key: str):
        self.request_handler = RequestHandler(base_url, app_id, app_key)

    def get(self, identity_chain_id: str, key: str):
        if not identity_chain_id:
            raise Exception("identity_chain_id is required.")
        if not key:
            raise Exception("key is required.")
        if not KeyCommon.validate_checksum(key):
            raise Exception("key is invalid.")
        return self.request_handler.get("/".join([factom_sdk.utils.consts.IDENTITY_URL, identity_chain_id,
                                                  factom_sdk.utils.consts.KEYS_STRING, key]))

    def list(self, identity_chain_id: str, limit: int = -1, offset: int = -1):
        if not identity_chain_id:
            raise Exception("identity_chain_id is required.")
        data = {}
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

    def replace(self, identity_chain_id: str, old_public_key: str, signer_private_key: str,
                new_public_key: str = None, callback_url: str = "", callback_stages: list = None):
        if callback_stages is None:
            callback_stages = []
        if not identity_chain_id:
            raise Exception("identity_chain_id is required.")
        if not old_public_key:
            raise Exception("old_public_key is required.")
        if not signer_private_key:
            raise Exception("signer_private_key is required.")
        key_pair = {}
        if new_public_key is not None:
            if not new_public_key:
                raise Exception("new_public_key is required.")
            new_key = new_public_key
        else:
            key_pair = KeyCommon.create_key_pair()
            new_key = key_pair["public_key"]
        if not KeyCommon.validate_checksum(old_public_key):
            raise Exception("old_public_key is an invalid public key.")
        if not KeyCommon.validate_checksum(signer_private_key):
            raise Exception("signer_private_key is invalid.")
        if not KeyCommon.validate_checksum(new_key):
            raise Exception("new_public_key is an invalid public key.")
        if not isinstance(callback_stages, list):
            raise Exception("callback_stages must be an array.")
        if callback_url and not validators.url(callback_url):
            raise Exception("callback_url is an invalid url format.")
        message = identity_chain_id + old_public_key + new_key
        signature = KeyCommon.sign_content(signer_private_key, message)
        signer_key = KeyCommon.get_public_key_from_private_key(signer_private_key)
        data = {
            "old_key": old_public_key,
            "new_key": new_key,
            "signature": signature,
            "signer_key": signer_key
        }
        if callback_url:
            data["callback_url"] = callback_url
        if callback_stages:
            data["callback_stages"] = callback_stages
        response = self.request_handler.post("/".join([factom_sdk.utils.consts.IDENTITY_URL, identity_chain_id,
                                                       factom_sdk.utils.consts.KEYS_STRING]), data)
        if new_public_key is None:
            response["key_pair"] = key_pair
        return response
