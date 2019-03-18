import validators
import factom_sdk.utils.consts
from factom_sdk.utils.key_common import KeyCommon
from factom_sdk.request_handler.request_handler import RequestHandler


class IdentitiesKeyUtil:
    def __init__(self, base_url: str, app_id: str, app_key: str):
        self.request_handler = RequestHandler(base_url, app_id, app_key)

    def get(self, identity_chain_id: str, key: str):
        """Gets information about a specific public key for a given Identity, including the heights at which the key
        was activated and retired if applicable.

        Args:
            identity_chain_id (str): The unique identifier for the Identity that the key belongs to.
            key (str): The public key string to get information, which must be in base58 idpub format.

        Returns:
            Identity key object.
        """
        if not identity_chain_id:
            raise Exception("identity_chain_id is required.")
        if not key:
            raise Exception("key is required.")
        if not KeyCommon.validate_checksum(key):
            raise Exception("key is invalid.")
        return self.request_handler.get("/".join([factom_sdk.utils.consts.IDENTITY_URL, identity_chain_id,
                                                  factom_sdk.utils.consts.KEYS_STRING, key]))

    def list(self, identity_chain_id: str, limit: int = -1, offset: int = -1):
        """Returns all of the keys that were ever active for this Identity. Results are paginated.

        Args:
            identity_chain_id (str): The unique identifier of the identity chain whose keys are being requested.
            limit (:obj:`int`, optional): The maximum number of keys you would like to be returned.
            offset (:obj:`int`, optional): The key index (in number of keys from the first key) to start from in the
            list of all keys.

        Returns:
            List identity key object.
        """
        if not identity_chain_id:
            raise Exception("identity_chain_id is required.")
        data = {}
        if not isinstance(limit, int):
            raise Exception("limit must be an integer.")
        if limit > -1:
            data["limit"] = limit
        if not isinstance(offset, int):
            raise Exception("offset must be an integer.")
        if offset > -1:
            data["offset"] = offset
        return self.request_handler.get("/".join([factom_sdk.utils.consts.IDENTITY_URL, identity_chain_id,
                                                  factom_sdk.utils.consts.KEYS_STRING]), data)

    def replace(self, identity_chain_id: str, old_public_key: str, signer_private_key: str,
                new_public_key: str = None, callback_url: str = "", callback_stages: list = None):
        """Creates an entry in the Identity Chain for a key replacement.

        Args:
            identity_chain_id (str): The unique identifier of the identity chain being requested.
            old_public_key (str): base58 string in Idpub format. The public key to be retired and replaced.
            signer_private_key (str): base58 string in Idsec format. The private key to use to create the signature,
            which must be the same or higher priority than the public key to be replaced.
            new_public_key (:obj:`str`, optional): base58 string in Idpub format. The new public key to be activated
            and take its place.
            callback_url (:obj:`str`, optional): The URL you would like the callbacks to be sent to.
            callback_stages (:obj:`list`, optional): The immutability stages you'd like to be notified about. This list
            can include any or all of these three stages: `replicated`, `factom`, and `anchored`

        Returns:
            Replacement result object.
        """
        if callback_stages is None:
            callback_stages = []
        if not identity_chain_id:
            raise Exception("identity_chain_id is required.")
        if not old_public_key:
            raise Exception("old_public_key is required.")
        if not signer_private_key:
            raise Exception("signer_private_key is required.")
        key_pair = {}
        if new_public_key is not None:
            if not new_public_key:
                raise Exception("new_public_key is required.")
            new_key = new_public_key
        else:
            key_pair = KeyCommon.create_key_pair()
            new_key = key_pair["public_key"]
        if not KeyCommon.validate_checksum(old_public_key):
            raise Exception("old_public_key is an invalid public key.")
        if not KeyCommon.validate_checksum(signer_private_key):
            raise Exception("signer_private_key is invalid.")
        if not KeyCommon.validate_checksum(new_key):
            raise Exception("new_public_key is an invalid public key.")
        if not isinstance(callback_stages, list):
            raise Exception("callback_stages must be an array.")
        if callback_url and not validators.url(callback_url):
            raise Exception("callback_url is an invalid url format.")
        message = identity_chain_id + old_public_key + new_key
        signature = KeyCommon.sign_content(signer_private_key, message)
        signer_key = KeyCommon.get_public_key_from_private_key(signer_private_key)
        data = {
            "old_key": old_public_key,
            "new_key": new_key,
            "signature": signature,
            "signer_key": signer_key
        }
        if callback_url:
            data["callback_url"] = callback_url
        if callback_stages:
            data["callback_stages"] = callback_stages
        response = self.request_handler.post("/".join([factom_sdk.utils.consts.IDENTITY_URL, identity_chain_id,
                                                       factom_sdk.utils.consts.KEYS_STRING]), data)
        if new_public_key is None:
            response["key_pair"] = key_pair
        return response
