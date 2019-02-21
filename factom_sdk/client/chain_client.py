import codecs
from factom_sdk.request_handler.request_handler import RequestHandler
from factom_sdk.utils.key_util import KeyUtil
from factom_sdk.utils.entry_util import EntryUtil

CHAINS_URL = "chains"
IDENTITIES_URL = "identities"
KEYS_STRING = "keys"


class ChainClient:
    def __init__(self, base_url: str, app_id: str, app_key: str, automatic_signing: bool, chain_id: str,
                 signature_validation=None):
        if not chain_id:
            raise Exception("chain_id is required.")
        self.request_handler = RequestHandler(base_url, app_id, app_key)
        self.automatic_signing = automatic_signing
        response = self.request_handler.get("/".join([CHAINS_URL, chain_id]))
        self.data = response["data"]
        if not callable(signature_validation) and not isinstance(signature_validation, bool):
            signature_validation = True
        if signature_validation and isinstance(signature_validation, bool):
            self.status = self.validate_signature(response)
        elif callable(signature_validation):
            self.status = signature_validation(response)

    def validate_signature(self, chain: dict):
        external_ids = chain["data"]["external_ids"]
        status = "valid_signature"
        if len(external_ids) < 6 or external_ids[0] != "SignedChain" or external_ids[1] != "0x01":
            status = "not_signed/invalid_chain_format"
        else:
            signer_chain_id = external_ids[2]
            signer_public_key = external_ids[3]
            signature = codecs.encode(codecs.decode(external_ids[4], "hex"), "base64").decode()
            time_stamp = external_ids[5]
            data = {}
            if "dblock" in chain["data"] and "height" in chain["data"]["dblock"]:
                data["active_at_height"] = chain["data"]["dblock"]["height"]
            key_response = self.request_handler.get("/".join([IDENTITIES_URL, signer_chain_id, KEYS_STRING]), data)
            if len([item for item in key_response if item["key"] == signer_public_key]) == 0:
                status = "inactive_key"
            else:
                message = signer_chain_id + chain["data"]["content"] + time_stamp
                if not KeyUtil.validate_signature(signer_public_key, signature, message):
                    status = "invalid_signature"
        return status

    def get_entry_info(self, entry_hash: str, signature_validation=None):
        return EntryUtil.get_entry_info(self.data["chain_id"], entry_hash, signature_validation, self.request_handler)

    def create_entry(self, content: str, external_ids: list = None, signer_private_key: str = "",
                     signer_chain_id: str = "", callback_url: str = "", callback_stages: list = None):
        if callback_stages is None:
            callback_stages = []
        if external_ids is None:
            external_ids = []
        return EntryUtil.create_entry(self.data["chain_id"], self.automatic_signing, content, external_ids,
                                      signer_private_key, signer_chain_id, callback_url, callback_stages,
                                      self.request_handler)

    def get_entries(self, limit: int = -1, offset: int = -1, stages: list = None):
        if stages is None:
            stages = []
        return EntryUtil.get_entries(self.data["chain_id"], limit, offset, stages, self.request_handler)

    def get_first_entry(self):
        return EntryUtil.get_first_entry(self.data["chain_id"], self.request_handler)

    def get_last_entry(self):
        return EntryUtil.get_last_entry(self.data["chain_id"], self.request_handler)

    def search_entries(self, external_ids: list, limit: int = -1, offset: int = -1):
        return EntryUtil.search_entries(self.data["chain_id"], external_ids, limit, offset, self.request_handler)
