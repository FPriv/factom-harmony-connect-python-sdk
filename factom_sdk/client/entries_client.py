import datetime

import validators

import factom_sdk.utils.consts
from factom_sdk.request_handler.request_handler import RequestHandler
from factom_sdk.utils.common_util import CommonUtil
from factom_sdk.utils.key_common import KeyCommon
from factom_sdk.utils.utils import Utils
from factom_sdk.utils.validate_signature_util import ValidateSignatureUtil


class EntriesClient:
    def __init__(self, base_url: str, app_id: str, app_key: str, automatic_signing: bool):
        self.request_handler = RequestHandler(base_url, app_id, app_key)
        self.automatic_signing = automatic_signing

    def get(self, chain_id: str, entry_hash: str, **kwargs):
        """Gets information about a specific entry on Connect.

        Args:
            chain_id (str): The chain identifier.
            entry_hash (str): The SHA256 hash of the entry.

        Returns:
            Entry object.
        """
        signature_validation = kwargs.get("signature_validation", None)
        client_overrides = kwargs.get("client_overrides", {})
        if not chain_id:
            raise Exception("chain_id is required.")
        if not entry_hash:
            raise Exception("entry_hash is required.")
        response = self.request_handler.get("/".join([factom_sdk.utils.consts.CHAINS_URL, chain_id,
                                                      factom_sdk.utils.consts.ENTRIES_URL, entry_hash]),
                                            client_overrides=client_overrides)
        if not callable(signature_validation) and not isinstance(signature_validation, bool):
            signature_validation = True
        if signature_validation and isinstance(signature_validation, bool):
            return {
                "entry": response,
                "status": ValidateSignatureUtil.validate_signature(response,
                                                                   validate_for_chain=False,
                                                                   request_handler=self.request_handler,
                                                                   client_overrides=client_overrides)
            }
        elif callable(signature_validation):
            return {
                "entry": response,
                "status": signature_validation(response)
            }
        return response

    def create(self, chain_id: str, content: str, **kwargs):
        """Creates a new entry for the selected chain.

        Args:
            chain_id (str): The chain identifier.
            content (str): This is the data that will be stored directly on the blockchain.

        Returns:
            Entry created object.
        """
        external_ids = kwargs.get("external_ids", [])
        signer_private_key = kwargs.get("signer_private_key", "")
        signer_chain_id = kwargs.get("signer_chain_id", "")
        callback_url = kwargs.get("callback_url", "")
        callback_stages = kwargs.get("callback_stages", [])
        client_overrides = kwargs.get("client_overrides", {})
        automatic_signing = client_overrides.get("automatic_signing", self.automatic_signing)

        if not chain_id:
            raise Exception("chain_id is required.")
        if automatic_signing:
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
        if automatic_signing:
            time_stamp = Utils.to_military_timezone_str(datetime.datetime.now(datetime.timezone.utc))
            message = signer_chain_id + content + time_stamp
            signature = KeyCommon.sign_content(signer_private_key, message)
            signer_public_key = KeyCommon.get_public_key_from_private_key(signer_private_key)
            ids_base64.append(CommonUtil.base64_encode("SignedEntry"))
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
        return self.request_handler.post("/".join([factom_sdk.utils.consts.CHAINS_URL, chain_id,
                                                   factom_sdk.utils.consts.ENTRIES_URL]),
                                         data=data,
                                         client_overrides=client_overrides)

    def list(self, chain_id: str, **kwargs):
        """Gets list of all entries contained on a specified chain.

        Args:
            chain_id (str): The chain identifier.

        Returns:
            List entry object.
        """
        limit = kwargs.get("limit", -1)
        offset = kwargs.get("offset", -1)
        stages = kwargs.get("stages", [])
        client_overrides = kwargs.get("client_overrides", {})
        if not chain_id:
            raise Exception("chain_id is required.")
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
        return self.request_handler.get("/".join([factom_sdk.utils.consts.CHAINS_URL, chain_id,
                                                  factom_sdk.utils.consts.ENTRIES_URL]),
                                        params=data,
                                        client_overrides=client_overrides)

    def get_first(self, chain_id: str, **kwargs):
        """Retrieves the first entry that has been saved to this chain.

        Args:
            chain_id (str): The chain identifier.

        Returns:
            Entry object.
        """
        signature_validation = kwargs.get("signature_validation", None)
        client_overrides = kwargs.get("client_overrides", {})
        if not chain_id:
            raise Exception("chain_id is required.")
        response = self.request_handler.get("/".join([factom_sdk.utils.consts.CHAINS_URL, chain_id,
                                                      factom_sdk.utils.consts.ENTRIES_URL,
                                                      factom_sdk.utils.consts.FIRST_URL]),
                                            client_overrides=client_overrides)
        if not callable(signature_validation) and not isinstance(signature_validation, bool):
            signature_validation = True
        if signature_validation and isinstance(signature_validation, bool):
            return {
                "entry": response,
                "status": ValidateSignatureUtil.validate_signature(response,
                                                                   validate_for_chain=False,
                                                                   request_handler=self.request_handler,
                                                                   client_overrides=client_overrides)
            }
        elif callable(signature_validation):
            return {
                "entry": response,
                "status": signature_validation(response)
            }
        return response

    def get_last(self, chain_id: str, **kwargs):
        """Gets the last entry that has been saved to this chain.

        Args:
            chain_id (str): The chain identifier.

        Returns:
            Entry object.
        """
        signature_validation = kwargs.get("signature_validation", None)
        client_overrides = kwargs.get("client_overrides", {})
        if not chain_id:
            raise Exception("chain_id is required.")
        response = self.request_handler.get("/".join([factom_sdk.utils.consts.CHAINS_URL, chain_id,
                                                      factom_sdk.utils.consts.ENTRIES_URL,
                                                      factom_sdk.utils.consts.LAST_URL]),
                                            client_overrides=client_overrides)
        if not callable(signature_validation) and not isinstance(signature_validation, bool):
            signature_validation = True
        if signature_validation and isinstance(signature_validation, bool):
            return {
                "entry": response,
                "status": ValidateSignatureUtil.validate_signature(response,
                                                                   validate_for_chain=False,
                                                                   request_handler=self.request_handler,
                                                                   client_overrides=client_overrides)
            }
        elif callable(signature_validation):
            return {
                "entry": response,
                "status": signature_validation(response)
            }
        return response

    def search(self, chain_id: str, external_ids: list, **kwargs):
        """Finds all of the entries with `external_ids` that match what you entered.

        Args:
            chain_id (str): The chain identifier.
            external_ids (list): A list of external IDs.

        Returns:
            List entry object.
        """
        limit = kwargs.get("limit", -1)
        offset = kwargs.get("offset", -1)
        client_overrides = kwargs.get("client_overrides", {})
        if not chain_id:
            raise Exception("chain_id is required.")
        if not external_ids:
            raise Exception("at least 1 external_id is required.")
        if not isinstance(external_ids, list):
            raise Exception("external_ids must be an array.")
        url = "/".join([factom_sdk.utils.consts.CHAINS_URL, chain_id, factom_sdk.utils.consts.ENTRIES_URL,
                        factom_sdk.utils.consts.SEARCH_URL])
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
        return self.request_handler.post(url, data=data, client_overrides=client_overrides)
