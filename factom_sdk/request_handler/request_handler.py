import requests
import validators
from urllib.parse import urljoin
from factom_sdk.utils.common_util import CommonUtil


class RequestHandler:
    def __init__(self, base_url: str, app_id: str, app_key: str):
        if not validators.url(base_url):
            raise Exception("The base_url provided is not valid.")
        if not isinstance(app_id, str):
            raise Exception("The app_id provided is not valid.")
        if not isinstance(app_key, str):
            raise Exception("The app_key provided is not valid.")

        if not base_url.endswith("/"):
            base_url += "/"

        self.base_url = base_url
        self.app_id = app_id
        self.app_key = app_key

    def _generic_request(self, method, endpoint, **kwargs):
        data = kwargs.get("data", None)
        params = kwargs.get("params", None)
        client_overrides = kwargs.get("client_overrides", {})
        app_id = client_overrides.get("app_id", self.app_id)
        if not isinstance(app_id, str):
            raise Exception("The app_id provided for override is not valid.")
        app_key = client_overrides.get("app_key", self.app_key)
        if not isinstance(app_key, str):
            raise Exception("The app_key provided for override is not valid.")
        headers = {
            "app_id": client_overrides.get("app_id", self.app_id),
            "app_key": client_overrides.get("app_key", self.app_key)
        }
        base_url = client_overrides.get("base_url", self.base_url)
        if not validators.url(base_url):
            raise Exception("The base_url provided for override is not valid.")
        if not base_url.endswith("/"):
            base_url += "/"

        response = requests.request(method,
                                    urljoin(base_url, endpoint),
                                    params=params,
                                    json=data,
                                    headers=headers)
        try:
            response.raise_for_status()
            return CommonUtil.decode_response(response.json())
        except requests.HTTPError as error:
            raise error

    def get(self, endpoint: str = "", **kwargs):
        params = kwargs.get("params", None)
        client_overrides = kwargs.get("client_overrides", {})
        return self._generic_request("GET", endpoint, params=params,
                                     client_overrides=client_overrides)

    def post(self, endpoint: str = "", **kwargs):
        data = kwargs.get("data", None)
        client_overrides = kwargs.get("client_overrides", {})
        return self._generic_request("POST", endpoint, data=data,
                                     client_overrides=client_overrides)
