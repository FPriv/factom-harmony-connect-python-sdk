import codecs
import factom_sdk.utils.consts
from factom_sdk.utils.key_util import KeyUtil


class ValidateSignatureUtil:
    @staticmethod
    def validate_signature(obj: dict, validate_for_chain: bool = True, request_handler=None):
        external_ids = obj["data"]["external_ids"]
        status = "valid_signature"
        type_name = "SignedChain"
        invalid_format = "not_signed/invalid_chain_format"
        if not validate_for_chain:
            type_name = "SignedEntry"
            invalid_format = "not_signed/invalid_entry_format"

        if len(external_ids) < 6 or external_ids[0] != type_name or external_ids[1] != "0x01":
            status = invalid_format
        else:
            signer_chain_id = external_ids[2]
            signer_public_key = external_ids[3]
            signature = codecs.encode(codecs.decode(external_ids[4], "hex"), "base64").decode()
            time_stamp = external_ids[5]
            data = {}
            if "dblock" in obj["data"] \
                    and obj["data"]["dblock"] is not None \
                    and "height" in obj["data"]["dblock"]:
                data["active_at_height"] = obj["data"]["dblock"]["height"]
            key_response = request_handler.get("/".join([factom_sdk.utils.consts.IDENTITIES_URL, signer_chain_id,
                                                         factom_sdk.utils.consts.KEYS_STRING]), data)
            if len([item for item in key_response["data"] if item["key"] == signer_public_key]) == 0:
                status = "inactive_key"
            else:
                message = signer_chain_id + obj["data"]["content"] + time_stamp
                if not KeyUtil.validate_signature(signer_public_key, signature, message):
                    status = "invalid_signature"
        return status
