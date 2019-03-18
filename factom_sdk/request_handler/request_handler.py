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

    def _generic_request(self, method, endpoint, data: dict = None, params: dict = None):
        headers = {
            "app_id": self.app_id,
            "app_key": self.app_key
        }
        response = requests.request(method, urljoin(self.base_url, endpoint), params=params, json=data, headers=headers)
        try:
            response.raise_for_status()
            return CommonUtil.decode_response(response.json())
        except requests.HTTPError as error:
            raise error

    def get(self, endpoint: str = "", params: dict = None):
        return self._generic_request("GET", endpoint, params=params)

    def post(self, endpoint: str = "", data: dict = None):
        return self._generic_request("POST", endpoint, data)
