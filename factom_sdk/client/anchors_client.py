import factom_sdk.utils.consts
from factom_sdk.request_handler.request_handler import RequestHandler


class AnchorsClient:
    def __init__(self, base_url: str, app_id: str, app_key: str):
        self.request_handler = RequestHandler(base_url, app_id, app_key)

    def get(self, **kwargs):
        """Gets the anchors for a specific entry or directory block from Connect.

        Args:
            object_hash (str): The unique identifier for an entry or directory block to request an anchor for
            height (int): The height fort the directory block to request an anchor for

        Returns:
            Anchors object.
        """
        base_url = kwargs.get("base_url")
        app_id = kwargs.get("app_id")
        app_key = kwargs.get("app_key")
        param = kwargs.get("object_identifier")
        is_valid_param = (isinstance(param, int) and param >= 0) or (isinstance(param, str) and len(param) == 64)
        assert is_valid_param, "object_identifier parameter must be a positive int or a string of length 64"

        return self.request_handler.get("/".join([factom_sdk.utils.consts.ANCHORS_URL, str(param)]),
                                        base_url=base_url, app_id=app_id, app_key=app_key)
