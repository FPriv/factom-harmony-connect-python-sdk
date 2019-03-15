from factom_sdk.request_handler.request_handler import RequestHandler


class ApiInfoClient:
    def __init__(self, base_url: str, app_id: str, app_key: str):
        self.request_handler = RequestHandler(base_url, app_id, app_key)

    def get(self):
        """Gets general information about the Connect API.

        Returns:
            API Info object.
        """
        return self.request_handler.get()
