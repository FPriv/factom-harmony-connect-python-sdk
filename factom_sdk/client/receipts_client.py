import factom_sdk.utils.consts
from factom_sdk.request_handler.request_handler import RequestHandler


class ReceiptsClient:
    def __init__(self, base_url: str, app_id: str, app_key: str):
        self.request_handler = RequestHandler(base_url, app_id, app_key)

    def get(self, entry_hash: str, **kwargs):
        """Gets a receipt for a specific entry from Connect.

        Args:
            entry_hash (str): The unique identifier created for the entry.

        Returns:
            Receipt object.
        """
        base_url = kwargs.get("base_url")
        app_id = kwargs.get("app_id")
        app_key = kwargs.get("app_key")
        assert isinstance(entry_hash, str) and len(entry_hash) == 64, "entry_hash must be a string of length 64"

        return self.request_handler.get("/".join([factom_sdk.utils.consts.RECEIPTS_URL, entry_hash]),
                                        base_url=base_url, app_id=app_id, app_key=app_key)
