from factom_sdk.request_handler.request_handler import RequestHandler
from factom_sdk.utils.entry_util import EntryUtil


class EntriesClient:
    def __init__(self, base_url: str, app_id: str, app_key: str, automatic_signing: bool):
        self.request_handler = RequestHandler(base_url, app_id, app_key)
        self.automatic_signing = automatic_signing

    def get_entry_info(self, chain_id: str, entry_hash: str, signature_validation=None):
        return EntryUtil.get_entry_info(chain_id, entry_hash, signature_validation, self.request_handler)

    def create_entry(self, chain_id: str, content: str, external_ids: list = None,
                     signer_private_key: str = "", signer_chain_id: str = "", callback_url: str = "",
                     callback_stages: list = None):
        if callback_stages is None:
            callback_stages = []
        if external_ids is None:
            external_ids = []
        return EntryUtil.create_entry(chain_id, self.automatic_signing, content, external_ids, signer_private_key,
                                      signer_chain_id, callback_url, callback_stages, self.request_handler)

    def get_entries_of_chain(self, chain_id: str, limit: int = -1, offset: int = -1, stages: list = None):
        if stages is None:
            stages = []
        return EntryUtil.get_entries(chain_id, limit, offset, stages, self.request_handler)

    def get_first_entry_of_chain(self, chain_id: str):
        return EntryUtil.get_first_entry(chain_id, self.request_handler)

    def get_last_entry_of_chain(self, chain_id: str):
        return EntryUtil.get_last_entry(chain_id, self.request_handler)

    def search_entries_of_chain(self, chain_id: str, external_ids: list, limit: int = -1, offset: int = -1):
        return EntryUtil.search_entries(chain_id, external_ids, limit, offset, self.request_handler)
