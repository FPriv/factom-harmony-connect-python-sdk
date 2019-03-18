import requests
import codecs
import factom_sdk.utils.consts
from factom_sdk.utils.key_common import KeyCommon


class ValidateSignatureUtil:
    @staticmethod
    def validate_signature(obj: dict, validate_for_chain: bool = True, request_handler=None):
        external_ids = obj["data"]["external_ids"]
        type_name = "SignedChain"
        invalid_format = "not_signed/invalid_chain_format"
        if not validate_for_chain:
            type_name = "SignedEntry"
            invalid_format = "not_signed/invalid_entry_format"

        if len(external_ids) < 6 or external_ids[0] != type_name or external_ids[1] != "0x01":
            return invalid_format

        signer_chain_id = external_ids[2]
        signer_public_key = external_ids[3]
        signature = codecs.encode(codecs.decode(external_ids[4], "hex"), "base64").decode()
        time_stamp = external_ids[5]
        key_height = 0
        if "dblock" in obj["data"] \
                and obj["data"]["dblock"] is not None \
                and "height" in obj["data"]["dblock"]:
            key_height = obj["data"]["dblock"]["height"]
        try:
            key_response = request_handler.get("/".join([factom_sdk.utils.consts.IDENTITIES_URL, signer_chain_id,
                                                         factom_sdk.utils.consts.KEYS_STRING, signer_public_key]))
            if key_response["data"]["retired_height"] is not None and \
                    not((key_response["data"]["activated_height"] <= key_height) and
                        (key_height <= key_response["data"]["retired_height"])):
                return "retired_key"
        except requests.HTTPError:
            return "retired_key"

        message = signer_chain_id + obj["data"]["content"] + time_stamp
        if not KeyCommon.validate_signature(signer_public_key, signature, message):
            return "invalid_signature"

        return "valid_signature"
