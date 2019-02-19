import os
import hashlib
import base58
import ed25519
import base64

PRIVATE_PREFIX_BYTES = bytearray([0x03, 0x45, 0xf3, 0xd0, 0xd6])
PUBLIC_PREFIX_BYTES = bytearray([0x03, 0x45, 0xef, 0x9d, 0xe0])
BASE64_ENCODE = 'base64'
UTF8_ENCODE = 'utf-8'


class KeyUtil:
    @staticmethod
    def create_key_pair():
        private_key_bytes = os.urandom(32)
        tmp = hashlib.sha256(hashlib.sha256(PRIVATE_PREFIX_BYTES + private_key_bytes).digest()).digest()
        check_sum = tmp[:4]
        private_key = base58.b58encode(bytes(PRIVATE_PREFIX_BYTES + private_key_bytes + check_sum))
        signing_key = ed25519.SigningKey(private_key_bytes)
        public_key_bytes = signing_key.get_verifying_key().to_bytes()
        tmp = hashlib.sha256(hashlib.sha256(PUBLIC_PREFIX_BYTES + public_key_bytes).digest()).digest()
        check_sum = tmp[:4]
        public_key = base58.b58encode(bytes(PUBLIC_PREFIX_BYTES + public_key_bytes + check_sum))
        return {
            "private_key": private_key,
            "public_key": public_key
        }

    @staticmethod
    def validate_check_sum(params: dict = {}):
        if "signer_key" not in params:
            return False
        signer_key_bytes = base58.b58decode(params["signer_key"])
        if len(signer_key_bytes) != 41:
            return False
        prefix_bytes = signer_key_bytes[:5]
        key_bytes = signer_key_bytes[5:37]
        check_sum = signer_key_bytes[37:]
        tmp = hashlib.sha256(hashlib.sha256(prefix_bytes + key_bytes).digest()).digest()
        tmp_check_sum = tmp[:4]
        if check_sum != tmp_check_sum:
            return False
        return True

    @staticmethod
    def get_invalid_keys(params: dict = {}):
        if "signer_keys" not in params:
            return []
        errors = []
        for key in params["signer_keys"]:
            if not KeyUtil.validate_check_sum({"signer_key": key}):
                errors.append({"key": key, "error": "key is invalid"})
        return errors

    @staticmethod
    def get_duplicate_keys(params: dict = {}):
        if "signer_keys" not in params:
            return []
        duplicates = []
        unique = []
        for key in params["signer_keys"]:
            if key not in unique:
                unique.append(key)
            else:
                if len([item for item in duplicates if item["key"] == key]) == 0:
                    duplicates.append({"key": key, "error": "key is duplicated, keys must be unique."})
        return duplicates

    @staticmethod
    def get_key_bytes_from_key(params: dict = {}):
        if not KeyUtil.validate_check_sum({"signer_key": params["signer_key"]}):
            raise Exception('key is invalid.')
        signer_key_bytes = base58.b58decode(params["signer_key"])
        return signer_key_bytes[5:37]

    @staticmethod
    def get_public_key_from_private_key(params: dict = {}):
        if not KeyUtil.validate_check_sum({"signer_key": params["signer_private_key"]}):
            raise Exception('signer_private_key is invalid.')
        private_key_bytes = KeyUtil.get_key_bytes_from_key({"signer_key": params["signer_private_key"]})
        signing_key = ed25519.SigningKey(private_key_bytes)
        public_key_bytes = signing_key.get_verifying_key().to_bytes()
        tmp = hashlib.sha256(hashlib.sha256(PUBLIC_PREFIX_BYTES + public_key_bytes).digest()).digest()
        check_sum = tmp[:4]
        return "".join(chr(x) for x in base58.b58encode(bytes(PUBLIC_PREFIX_BYTES + public_key_bytes + check_sum)))

    @staticmethod
    def sign_content(params: dict = {}):
        if "signer_private_key" not in params:
            raise Exception("signer_private_key is required.")
        if not KeyUtil.validate_check_sum({"signer_key": params["signer_private_key"]}):
            raise Exception('signer_private_key is invalid.')
        if "message" not in params:
            raise Exception("message is required.")
        private_key_bytes = KeyUtil.get_key_bytes_from_key({"signer_key": params["signer_private_key"]})
        secret_key = ed25519.SigningKey(private_key_bytes)
        message_bytes = params["message"].encode(UTF8_ENCODE)
        return "".join(chr(x) for x in base64.b64encode(secret_key.sign(message_bytes)))

    @staticmethod
    def validate_signature(params: dict = {}):
        if "signer_public_key" not in params:
            raise Exception("signer_public_key is required.")
        if not KeyUtil.validate_check_sum({"signer_key": params["signer_public_key"]}):
            raise Exception('signer_public_key is invalid.')
        if "signature" not in params:
            raise Exception("signature is required.")
        if "message" not in params:
            raise Exception("message is required.")
        signature_bytes = base64.b64decode(params["signature"])
        message_bytes = params["message"].encode(UTF8_ENCODE)
        key_bytes = KeyUtil.get_key_bytes_from_key({"signer_key": params["signer_public_key"]})
        verify_key = ed25519.VerifyingKey(key_bytes)
        try:
            verify_key.verify(signature_bytes, message_bytes)
            return True
        except ed25519.BadSignatureError:
            return False
