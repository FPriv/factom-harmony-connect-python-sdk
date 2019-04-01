import datetime

import validators

import factom_sdk.utils.consts
from factom_sdk.client.entries_client import EntriesClient
from factom_sdk.request_handler.request_handler import RequestHandler
from factom_sdk.utils.common_util import CommonUtil
from factom_sdk.utils.key_common import KeyCommon
from factom_sdk.utils.utils import Utils
from factom_sdk.utils.validate_signature_util import ValidateSignatureUtil


class ChainsClient:
    def __init__(self, base_url: str, app_id: str, app_key: str, automatic_signing: bool):
        self.request_handler = RequestHandler(base_url, app_id, app_key)
        self.automatic_signing = automatic_signing
        self.entries = EntriesClient(base_url, app_id, app_key, automatic_signing)

    def get(self, chain_id: str, signature_validation=None):
        """Gets information about a specific chain from Connect.

        Args:
            chain_id (str): The unique identifier created for each chain.
            signature_validation (bool | custom function)

        Returns:
            Chain object.
        """
        if not chain_id:
            raise Exception("chain_id is required.")
        response = self.request_handler.get("/".join([factom_sdk.utils.consts.CHAINS_URL, chain_id]))
        if not callable(signature_validation) and not isinstance(signature_validation, bool):
            signature_validation = True
        if signature_validation and isinstance(signature_validation, bool):
            return {
                "chain": response,
                "status": ValidateSignatureUtil.validate_signature(response, True, self.request_handler)
            }
        elif callable(signature_validation):
            return {
                "chain": response,
                "status": signature_validation(response)
            }
        return response

    def create(self, content: str, external_ids: list = None, signer_private_key: str = "",
               signer_chain_id: str = "", callback_url: str = "", callback_stages: list = None):
        """Creates a new chain

        Args:
            content (str): This is the data that will make up the first entry in your new chain.
            external_ids (:obj:`list`, optional): Tags that can be used to identify your chain.
            signer_private_key (:obj:`str`, optional): base58 string in Idsec format. This parameter is optional for
            creating an unsigned chain.
            signer_chain_id (:obj:`str`, optional): The chain id of the signer identity. This parameter is optional for
            creating an unsigned chain.
            callback_url (:obj:`str`, optional): The URL where you would like to receive the callback from Connect.
            callback_stages (:obj:`list`, optional): The immutability stages you would like to be notified about.
            This list can include any or all of the three stages: `replicated`, `factom`, and `anchored`.

        Returns:
            Chain created info object.
        """
        if callback_stages is None:
            callback_stages = []
        if external_ids is None:
            external_ids = []
        if self.automatic_signing:
            if not isinstance(external_ids, list):
                raise Exception("external_ids must be an array.")
            if not signer_private_key:
                raise Exception("signer_private_key is required.")
            if not KeyCommon.validate_checksum(signer_private_key):
                raise Exception("signer_private_key is invalid.")
            if not signer_chain_id:
                raise Exception("signer_chain_id is required.")
        else:
            if not external_ids:
                raise Exception("at least 1 external_id is required.")
            if not isinstance(external_ids, list):
                raise Exception("external_ids must be an array.")
            if signer_private_key and not signer_chain_id:
                raise Exception("signer_chain_id is required when passing a signer_private_key.")
            if signer_private_key and not KeyCommon.validate_checksum(signer_private_key):
                raise Exception("signer_private_key is invalid.")
            if signer_chain_id and not signer_private_key:
                raise Exception("signer_private_key is required when passing a signer_chain_id.")
        if not content:
            raise Exception("content is required.")
        if callback_url and not validators.url(callback_url):
            raise Exception("callback_url is an invalid url format.")
        if not isinstance(callback_stages, list):
            raise Exception("callback_stages must be an array.")
        ids_base64 = []
        if self.automatic_signing:
            time_stamp = Utils.to_military_timezone_str(datetime.datetime.now(datetime.timezone.utc))
            message = signer_chain_id + content + time_stamp
            signature = KeyCommon.sign_content(signer_private_key, message)
            signer_public_key = KeyCommon.get_public_key_from_private_key(signer_private_key)
            ids_base64.append(CommonUtil.base64_encode("SignedChain"))
            ids_base64.append(CommonUtil.base64_encode(bytes([0x01])))
            ids_base64.append(CommonUtil.base64_encode(signer_chain_id))
            ids_base64.append(CommonUtil.base64_encode(signer_public_key))
            ids_base64.append(signature)
            ids_base64.append(CommonUtil.base64_encode(time_stamp))
        for val in external_ids:
            ids_base64.append(CommonUtil.base64_encode(val))
        data = {
            "external_ids": ids_base64,
            "content": CommonUtil.base64_encode(content)
        }
        if callback_url:
            data["callback_url"] = callback_url
        if callback_stages:
            data["callback_stages"] = callback_stages
        return self.request_handler.post(factom_sdk.utils.consts.CHAINS_URL, data)

    def list(self, limit: int = -1, offset: int = -1, stages: list = None):
        """Gets all of the chains on Factom.

        Args:
            limit (:obj:`int`, optional): The number of items you would like to return back in each stage.
            offset (:obj:`int`, optional): The offset parameter allows you to select which item you would like to start
            from when a list is returned from Connect.
            stages (:obj:`list`, optional): The immutability stages you want to restrict results to.
            You can choose any from `replicated`, `factom`, and `anchored`.

        Returns:
            List chains object.
        """
        if stages is None:
            stages = []
        data = {}
        if not isinstance(limit, int):
            raise Exception("limit must be an integer.")
        if limit > -1:
            data["limit"] = limit
        if not isinstance(offset, int):
            raise Exception("offset must be an integer.")
        if offset > -1:
            data["offset"] = offset
        if not isinstance(stages, list):
            raise Exception("stages must be an array.")
        if stages:
            data["stages"] = ",".join(stages)
        return self.request_handler.get(factom_sdk.utils.consts.CHAINS_URL, data)

    def search(self, external_ids: list, limit: int = -1, offset: int = -1):
        """Finds all of the chains with `external_ids` that match what you entered.

        Args:
            external_ids (list): A list of external IDs associated with the chains user would like to search by.
            limit (:obj:`int`, optional): The number of items you would like to return back in each stage.
            offset (:obj:`int`, optional): The offset parameter allows you to select which item you would like to start
            from when a list is returned from Connect.

        Returns:
            List chains object.
        """
        if not external_ids:
            raise Exception("at least 1 external_id is required.")
        if not isinstance(external_ids, list):
            raise Exception("external_ids must be an array.")
        url = "/".join([factom_sdk.utils.consts.CHAINS_URL, factom_sdk.utils.consts.SEARCH_URL])
        if not isinstance(limit, int):
            raise Exception("limit must be an integer.")
        if limit > -1:
            url += "?limit=" + str(limit)
        if not isinstance(offset, int):
            raise Exception("offset must be an integer.")
        if offset > -1:
            if limit > -1:
                url += "&offset=" + str(offset)
            else:
                url += "?offset=" + str(offset)
        ids_base64 = [CommonUtil.base64_encode(val) for val in external_ids]
        data = {"external_ids": ids_base64}
        return self.request_handler.post(url, data)
