from factom_sdk.client.chains_client import ChainsClient
from factom_sdk.client.identities_client import IdentitiesClient
from factom_sdk.client.api_info_client import ApiInfoClient
from factom_sdk.utils.utils import Utils


class FactomClient:
    def __init__(self, base_url: str, app_id: str, app_key: str, automatic_signing: bool = True):
        """The Factom SDK is initialized.

        Args:
            base_url (str): The URL with the account domain
            app_id (str): Your app id
            app_id (str): Your app key
            automatic_signing (bool)

        Returns:
            Factom SDK client object.
        """
        if not isinstance(automatic_signing, bool):
            automatic_signing = True
        self.base_url = base_url
        self.app_id = app_id
        self.app_key = app_key
        self.automatic_signing = automatic_signing
        self._api_info = None
        self._chains = None
        self._identities = None
        self.utils = Utils

    @property
    def identities(self):
        if self._identities is None:
            self._identities = IdentitiesClient(self.base_url, self.app_id, self.app_key)
        return self._identities

    @property
    def api_info(self):
        if self._api_info is None:
            self._api_info = ApiInfoClient(self.base_url, self.app_id, self.app_key)
        return self._api_info

    @property
    def chains(self):
        if self._chains is None:
            self._chains = ChainsClient(self.base_url, self.app_id, self.app_key, self.automatic_signing)
        return self._chains
