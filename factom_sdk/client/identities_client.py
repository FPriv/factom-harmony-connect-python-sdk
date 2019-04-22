import validators
import factom_sdk.utils.consts
from factom_sdk.utils.common_util import CommonUtil
from factom_sdk.utils.key_common import KeyCommon
from factom_sdk.request_handler.request_handler import RequestHandler
from factom_sdk.utils.identities.identities_key_util import IdentitiesKeyUtil


class IdentitiesClient:
    def __init__(self, base_url: str, app_id: str, app_key: str):
        self.request_handler = RequestHandler(base_url, app_id, app_key)
        self.keys = IdentitiesKeyUtil(base_url, app_id, app_key)

    def create(self, names: list, keys: list = None, callback_url: str = "", callback_stages: list = None):
        """Creates a new Identity chain.

        Args:
            names (list): The names array for your identity must be unique.
            keys (:obj:`list`, optional): An array of public key strings in base58 idpub format, ordered from the
            highest to the lowest priority.
            callback_url (:obj:`str`, optional): The URL where you would like to receive the callback from Connect.
            callback_stages (:obj:`list`, optional): The immutability stages you would like to be notified about.
            This list can include any or all of the three stages: `replicated`, `factom`, and `anchored`.

        Returns:
            Identity chain created object.
        """
        if callback_stages is None:
            callback_stages = []
        if not names:
            raise Exception("at least 1 name is required.")
        if not isinstance(names, list):
            raise Exception("names must be an array.")

        key_pairs = []
        if keys is not None:
            if not keys:
                raise Exception("at least 1 key is required.")
            if not isinstance(keys, list):
                raise Exception("keys must be an array.")
            signer_keys = keys
        else:
            key_pairs = [KeyCommon.create_key_pair() for _ in range(3)]
            signer_keys = [val["public_key"] for val in key_pairs]

        if not isinstance(callback_stages, list):
            raise Exception("callback_stages must be an array.")
        invalid_keys = KeyCommon.get_invalid_keys(signer_keys)
        if len(invalid_keys) > 0:
            raise Exception(invalid_keys)
        duplicate_keys = KeyCommon.get_duplicate_keys(signer_keys)
        if len(duplicate_keys) > 0:
            raise Exception(duplicate_keys)
        if callback_url and not validators.url(callback_url):
            raise Exception("callback_url is an invalid url format.")
        name_byte_count = 0
        for _name in names:
            name_byte_count += len(_name)

        # 2 bytes for the size of extid + 13 for actual IdentityChain ext-id text
        # 2 bytes per name for size * (number of names) + size of all names
        # 23 bytes for `{"keys":[],"version":1}`
        # 58 bytes per `"idpub2PHPArpDF6S86ys314D3JDiKD8HLqJ4HMFcjNJP6gxapoNsyFG",` array element
        # -1 byte because last key element has no comma
        # = 37 + name_byte_count + 2(number_of_names) + 58(number_of_keys)
        total_bytes = 37 + name_byte_count + (len(names) * 2) + (len(signer_keys) * 58)
        if total_bytes > 10240:
            message = "Entry size {} must be less than 10240. Use less/shorter names or less keys.".format(total_bytes)
            raise Exception(message)

        names_base64 = [CommonUtil.base64_encode(_name) for _name in names]
        data = {
            "names": names_base64,
            "keys": signer_keys
        }
        if callback_url:
            data["callback_url"] = callback_url
        if callback_stages:
            data["callback_stages"] = callback_stages
        response = self.request_handler.post(factom_sdk.utils.consts.IDENTITY_URL, data)
        if keys is None:
            response["key_pairs"] = key_pairs
        return response

    def get(self, identity_chain_id: str):
        """Gets a summary of the identity chain's current state.

        Args:
            identity_chain_id (str): The unique identifier for the identity chain being requested.

        Returns:
            Identity chain object.
        """
        if not identity_chain_id:
            raise Exception("identity_chain_id is required.")
        return self.request_handler.get("/".join([factom_sdk.utils.consts.IDENTITY_URL, identity_chain_id]))
