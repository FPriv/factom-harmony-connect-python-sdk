import factom_sdk.utils.consts
from factom_sdk.request_handler.request_handler import RequestHandler
from factom_sdk.utils.entry_util import EntryUtil
from factom_sdk.utils.validate_signature_util import ValidateSignatureUtil


class ChainClient:
    def __init__(self, base_url: str, app_id: str, app_key: str, automatic_signing: bool, chain_id: str,
                 signature_validation=None):
        if not chain_id:
            raise Exception("chain_id is required.")
        self.request_handler = RequestHandler(base_url, app_id, app_key)
        self.automatic_signing = automatic_signing
        response = self.request_handler.get("/".join([factom_sdk.utils.consts.CHAINS_URL, chain_id]))
        self.data = response["data"]
        if not callable(signature_validation) and not isinstance(signature_validation, bool):
            signature_validation = True
        if signature_validation and isinstance(signature_validation, bool):
            self.status = ValidateSignatureUtil.validate_signature(response, True, self.request_handler)
        elif callable(signature_validation):
            self.status = signature_validation(response)

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
