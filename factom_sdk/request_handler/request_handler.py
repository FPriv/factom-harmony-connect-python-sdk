import requests
import validators
from factom_sdk.utils.common_util import CommonUtil


class RequestHandler:
    def __init__(self, base_url: str, app_id: str, app_key: str):
        if not validators.url(base_url):
            raise Exception("The base_url provided is not valid.")
        if not isinstance(app_id, str):
            raise Exception("The app_id provided is not valid.")
        if not isinstance(app_key, str):
            raise Exception("The app_key provided is not valid.")

        self.base_url = base_url
        self.app_id = app_id
        self.app_key = app_key

    def _generic_request(self, request_type, endpoint, payload: dict = None,
                         params: dict = None, json: dict = None):
        headers = {
            "content-type": "appication/json",
            "app_id": self.app_id,
            "app_key": self.app_key
        }
        response = request_type(
            "/".join(map(lambda x: str(x).rstrip("/"), [self.base_url, endpoint])),
            headers=headers,
            params=params,
            data=payload,
            json=json,
            verify=True
        )
        response.raise_for_status()
        try:
            return CommonUtil.decode_response(response.json())
        except ValueError:
            return {}

    def request(self, method: str, url: str = "", kwargs: dict = {}):
        if method.upper() == "GET":
            params = None
            if "params" in kwargs:
                params = kwargs["params"]
            return self._generic_request(requests.get, url, None, params, None)
        else:
            data = None
            json = None
            if "data" in kwargs:
                data = kwargs["data"]
            if "json" in kwargs:
                json = kwargs["json"]
            return self._generic_request(requests.post, url, data, None, json)
