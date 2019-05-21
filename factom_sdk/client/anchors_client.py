import factom_sdk.utils.consts
from factom_sdk.request_handler.request_handler import RequestHandler


class AnchorsClient:
    def __init__(self, base_url: str, app_id: str, app_key: str):
        self.request_handler = RequestHandler(base_url, app_id, app_key)

    def get(self, object_hash: str = None, height: int = None):
        """Gets the anchors for a specific entry or directory block from Connect.

        Args:
            object_hash (str): The unique identifier for an entry or directory block to request an anchor for
            height (int): The height fort the directory block to request an anchor for

        Returns:
            Anchors object.
        """
        if object_hash is None:
            assert height is not None, "either object_hash or height must not be None"
            assert isinstance(height, int) and height > 0, "height must be a positive integer"
            return self.request_handler.get("/".join([factom_sdk.utils.consts.ANCHORS_URL, str(height)]))
        else:
            assert isinstance(object_hash, str) and len(object_hash) == 64, "object_hash must be a string of length 64"
            assert height is None, "object_hash provided, height must be None"
            return self.request_handler.get("/".join([factom_sdk.utils.consts.ANCHORS_URL, object_hash]))
