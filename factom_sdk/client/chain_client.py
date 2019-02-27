import factom_sdk.utils.consts
from factom_sdk.request_handler.request_handler import RequestHandler
from factom_sdk.utils.entry_util import EntryUtil
from factom_sdk.utils.validate_signature_util import ValidateSignatureUtil


def lazy_property(fn):
    attr_name = '_lazy_' + fn.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazy_property


class ChainClient:
    def __init__(self, base_url: str, app_id: str, app_key: str, automatic_signing: bool, chain_id: str,
                 signature_validation=None):
        if not chain_id:
            raise Exception("chain_id is required.")
        self.chain_id = chain_id
        self.request_handler = RequestHandler(base_url, app_id, app_key)
        self.automatic_signing = automatic_signing
        if not callable(signature_validation) and not isinstance(signature_validation, bool):
            self.signature_validation = True
        else:
            self.signature_validation = signature_validation
        self._response = None

    @lazy_property
    def response(self):
        return self.request_handler.get("/".join([factom_sdk.utils.consts.CHAINS_URL, self.chain_id]))

    @lazy_property
    def data(self):
        return self.response["data"]

    @lazy_property
    def status(self):
        if self.signature_validation and isinstance(self.signature_validation, bool):
            return ValidateSignatureUtil.validate_signature(self.response, True, self.request_handler)
        elif callable(self.signature_validation):
            return self.signature_validation(self.response)
        return ""

    def get_entry_info(self, entry_hash: str, signature_validation=None):
        return EntryUtil.get_entry_info(self.chain_id, entry_hash, signature_validation, self.request_handler)

    def create_entry(self, content: str, external_ids: list = None, signer_private_key: str = "",
                     signer_chain_id: str = "", callback_url: str = "", callback_stages: list = None):
        if callback_stages is None:
            callback_stages = []
        if external_ids is None:
            external_ids = []
        return EntryUtil.create_entry(self.chain_id, self.automatic_signing, content, external_ids,
                                      signer_private_key, signer_chain_id, callback_url, callback_stages,
                                      self.request_handler)

    def get_entries(self, limit: int = -1, offset: int = -1, stages: list = None):
        if stages is None:
            stages = []
        return EntryUtil.get_entries(self.chain_id, limit, offset, stages, self.request_handler)

    def get_first_entry(self):
        return EntryUtil.get_first_entry(self.chain_id, self.request_handler)

    def get_last_entry(self):
        return EntryUtil.get_last_entry(self.chain_id, self.request_handler)

    def search_entries(self, external_ids: list, limit: int = -1, offset: int = -1):
        return EntryUtil.search_entries(self.chain_id, external_ids, limit, offset, self.request_handler)
