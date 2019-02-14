import validators
import base64
from factom_sdk.utils.key_util import KeyUtil
from factom_sdk.utils.common_util import CommonUtil
from factom_sdk.request_handler.request_handler import RequestHandler

IDENTITY_URL = "identities"
KEYS_STRING = "keys"
UTF8_ENCODE = "utf-8"


class IdentityClient:
    def __init__(self, options: dict = {}):
        self.request_handler = RequestHandler(options["base_url"], options["app_id"], options["app_key"])

    def create_identity_key_pair(self, params: dict = {}):
        if "number_of_key_pair" not in params:
            params["number_of_key_pair"] = 3
        result = []
        n = 0
        while n < params["number_of_key_pair"]:
            result.append(KeyUtil.create_key_pair())
            n += 1
        return result

    def create_identity(self, params: dict = {}):
        if "name" not in params or CommonUtil.is_empty_arr(params["name"]):
            raise Exception("name is required.")
        if not CommonUtil.is_array(params["name"]):
            raise Exception("name must be an array.")
        if "keys" not in params or CommonUtil.is_empty_arr(params["keys"]):
            raise Exception("at least 1 key is required.")
        if not CommonUtil.is_array(params["keys"]):
            raise Exception("keys must be an array.")
        if "callback_stages" in params and not CommonUtil.is_array(params["callback_stages"]):
            raise Exception("callback_stages must be an array.")
        invalid_keys = KeyUtil.get_invalid_keys({"signer_keys": params["keys"]})
        if len(invalid_keys) > 0:
            raise Exception(invalid_keys)
        duplicate_keys = KeyUtil.get_duplicate_keys({"signer_keys": params["keys"]})
        if len(duplicate_keys) > 0:
            raise Exception(duplicate_keys)
        if "callback_url" in params \
                and not CommonUtil.is_empty_string(params["callback_url"]) \
                and not validators.url(params["callback_url"]):
            raise Exception("callback_url is an invalid url format.")
        name_base64 = []
        for name in params["name"]:
            name_base64.append(base64.b64encode(name.encode(UTF8_ENCODE)))
        name_byte_count = 0
        for name in name_base64:
            name_byte_count += len(name)
        total_bytes = 37 + name_byte_count + (len(name_base64) * 2) + (len(params["keys"]) * 58)
        if total_bytes > 10240:
            raise Exception("calculated bytes of name and keys is " + str(total_bytes) +
                            ". It must be less than 10240, use less/shorter name or less keys.")
        data = {
            "name": name_base64,
            "keys": params["keys"]
        }
        if "callback_url" in params and not CommonUtil.is_empty_string(params["callback_url"]):
            data["callback_url"] = params["callback_url"]
        if "callback_stages" in params and CommonUtil.is_array(params["callback_stages"]):
            data["callback_stages"] = params["callback_stages"]
        return self.request_handler.post(IDENTITY_URL, data)

    def get_identity(self, params: dict = {}):
        if "identity_chain_id" not in params or CommonUtil.is_empty_string(params["identity_chain_id"]):
            raise Exception("identity_chain_id is required.")
        return self.request_handler.get("/".join(
            map(lambda x: str(x).rstrip('/'), [IDENTITY_URL, params["identity_chain_id"]])))

    def get_all_identity_keys(self, params: dict = {}):
        if "identity_chain_id" not in params or CommonUtil.is_empty_string(params["identity_chain_id"]):
            raise Exception("identity_chain_id is required.")
        data = {}
        if "active_at_height" in params:
            if type(params["active_at_height"]).__name__ != "int":
                raise Exception("active_at_height must be an integer.")
            data["active_at_height"] = params["active_at_height"]
        if "limit" in params:
            if type(params["limit"]).__name__ != "int":
                raise Exception("limit must be an integer.")
            data["limit"] = params["limit"]
        if "offset" in params:
            if type(params["offset"]).__name__ != "int":
                raise Exception("offset must be an integer.")
            data["offset"] = params["offset"]
        return self.request_handler.get("/".join(
            map(lambda x: str(x).rstrip('/'), [IDENTITY_URL, params["identity_chain_id"], KEYS_STRING])), data)

    def create_identity_key_replacement(self, params: dict = {}):
        if "identity_chain_id" not in params or CommonUtil.is_empty_string(params["identity_chain_id"]):
            raise Exception("identity_chain_id is required.")
        if "old_public_key" not in params or CommonUtil.is_empty_string(params["old_public_key"]):
            raise Exception("old_public_key is required.")
        if "new_public_key" not in params or CommonUtil.is_empty_string(params["new_public_key"]):
            raise Exception("new_public_key is required.")
        if "signer_private_key" not in params or CommonUtil.is_empty_string(params["signer_private_key"]):
            raise Exception("signer_private_key is required.")
        if not KeyUtil.validate_check_sum({"signer_key": params["old_public_key"]}):
            raise Exception("old_public_key is an invalid public key.")
        if not KeyUtil.validate_check_sum({"signer_key": params["new_public_key"]}):
            raise Exception("new_public_key is an invalid public key.")
        if not KeyUtil.validate_check_sum({"signer_key": params["signer_private_key"]}):
            raise Exception("signer_private_key is invalid.")
        if "callback_stages" in params and not CommonUtil.is_array(params["callback_stages"]):
            raise Exception("callback_stages must be an array.")
        if "callback_url" in params \
                and not CommonUtil.is_empty_string(params["callback_url"]) \
                and not validators.url(params["callback_url"]):
            raise Exception("callback_url is an invalid url format.")
        message = params["identity_chain_id"] + params["old_public_key"] + params["new_public_key"]
        signature = KeyUtil.sign_content({"signer_private_key": params["signer_private_key"], "message": message})
        signer_key = KeyUtil.get_public_key_from_private_key({"signer_private_key": params["signer_private_key"]})
        data = {
            "old_key": params["old_public_key"],
            "new_key": params["new_public_key"],
            "signature": signature,
            "signer_key": signer_key
        }
        if "callback_url" in params and not CommonUtil.is_empty_string(params["callback_url"]):
            data["callback_url"] = params["callback_url"]
        if "callback_stages" in params and CommonUtil.is_array(params["callback_stages"]):
            data["callback_stages"] = params["callback_stages"]
        return self.request_handler.post("/".join(
            map(lambda x: str(x).rstrip('/'), [IDENTITY_URL, params["identity_chain_id"], KEYS_STRING])), data)
