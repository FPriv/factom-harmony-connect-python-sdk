class IdentityClient:
    IDENTITY_URL = "identities"
    KEYS_STRING = "keys"

    def __init__(self, request_handler):
        self.request_handler = request_handler
