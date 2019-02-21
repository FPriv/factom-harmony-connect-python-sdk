from factom_sdk.client.chain_client import ChainClient
from factom_sdk.client.chains_client import ChainsClient
from factom_sdk.client.entries_client import EntriesClient
from factom_sdk.client.identity_client import IdentityClient
from factom_sdk.client.info_client import InfoClient
from factom_sdk.utils.key_util import KeyUtil


class FactomClient:
    def __init__(self, base_url: str, app_id: str, app_key: str, automatic_signing=None):
        if not isinstance(automatic_signing, bool):
            automatic_signing = True
        self.base_url = base_url
        self.app_id = app_id
        self.app_key = app_key
        self.automatic_signing = automatic_signing
        self.key_util = KeyUtil
        self._identity = None
        self._info = None
        self._chains = None
        self._entries = None

    def chain(self, chain_id: str, signature_validation=None):
        return ChainClient(self.base_url, self.app_id, self.app_key, self.automatic_signing, chain_id,
                           signature_validation)

    @property
    def identity(self):
        if self._identity is None:
            self._identity = IdentityClient(self.base_url, self.app_id, self.app_key)
        return self._identity

    @property
    def info(self):
        if self._info is None:
            self._info = InfoClient(self.base_url, self.app_id, self.app_key)
        return self._info

    @property
    def chains(self):
        if self._chains is None:
            self._chains = ChainsClient(self.base_url, self.app_id, self.app_key, self.automatic_signing)
        return self._chains

    @property
    def entries(self):
        if self._entries is None:
            self._entries = EntriesClient(self.base_url, self.app_id, self.app_key, self.automatic_signing)
        return self._entries
