from urllib.parse import urljoin
import requests
import validators


class RequestHandler:
    def __init__(self, base_url: str, app_id: str, app_key: str):
        if not validators.url(base_url):
            raise Exception('The base_url provided is not valid.')
        if not isinstance(app_id, str):
            raise Exception('The app_id provided is not valid.')
        if not isinstance(app_key, str):
            raise Exception('The app_key provided is not valid.')

        self.base_url = base_url
        self.app_id = app_id
        self.app_key = app_key

    # pylint: disable=too-many-arguments
    def _generic_request(self, request_type, endpoint, payload: dict = None,
                         params: dict = None, json: dict = None):
        headers = {
            'content-type': 'appication/json',
            'app_id': self.app_id,
            'app_key': self.app_key
        }
        response = request_type(
            urljoin(self.base_url, endpoint),
            headers=headers,
            params=params,
            data=payload,
            json=json,
            verify=True
        )
        response.raise_for_status()
        print(response.json())
        try:
            return response.json()
        except ValueError:
            return {}

    def get(self, endpoint, params: dict = None):
        return self._generic_request(
            requests.get,
            endpoint,
            params=params
        )

    def post(self, endpoint, payload: dict = None, json: dict = None):
        return self._generic_request(
            request_type=requests.post,
            endpoint=endpoint,
            payload=payload,
            json=json
        )
