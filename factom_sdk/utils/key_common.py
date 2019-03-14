import os
import hashlib
import base58
import ed25519
import base64
import factom_sdk.utils.consts


class KeyCommon:
    @staticmethod
    def create_key_pair():
        private_key_bytes = os.urandom(32)
        tmp = hashlib.sha256(hashlib.sha256(factom_sdk.utils.consts.PRIVATE_PREFIX_BYTES +
                                            private_key_bytes).digest()).digest()
        checksum = tmp[:4]
        private_key = base58.b58encode(bytes(factom_sdk.utils.consts.PRIVATE_PREFIX_BYTES +
                                             private_key_bytes + checksum))
        signing_key = ed25519.SigningKey(private_key_bytes)
        public_key_bytes = signing_key.get_verifying_key().to_bytes()
        tmp = hashlib.sha256(hashlib.sha256(factom_sdk.utils.consts.PUBLIC_PREFIX_BYTES +
                                            public_key_bytes).digest()).digest()
        checksum = tmp[:4]
        public_key = base58.b58encode(bytes(factom_sdk.utils.consts.PUBLIC_PREFIX_BYTES +
                                            public_key_bytes + checksum))
        return {
            "private_key": "".join(chr(x) for x in private_key),
            "public_key": "".join(chr(x) for x in public_key)
        }

    @staticmethod
    def validate_checksum(signer_key: str):
        if not signer_key:
            return False
        signer_key_bytes = base58.b58decode(signer_key)
        if len(signer_key_bytes) != 41:
            return False
        prefix_bytes = signer_key_bytes[:5]
        key_bytes = signer_key_bytes[5:37]
        checksum = signer_key_bytes[37:]
        tmp = hashlib.sha256(hashlib.sha256(prefix_bytes + key_bytes).digest()).digest()
        tmp_checksum = tmp[:4]
        if checksum != tmp_checksum:
            return False
        return True

    @staticmethod
    def get_invalid_keys(signer_keys: list):
        if not signer_keys:
            return []
        return [{"key": key, "error": "key is invalid"} for key in signer_keys if not KeyCommon.validate_checksum(key)]

    @staticmethod
    def get_duplicate_keys(signer_keys: list):
        if not signer_keys:
            return []

        seen = {}
        duplicates = []
        for key in signer_keys:
            if key not in seen:
                seen[key] = 1
            else:
                if seen[key] == 1:
                    duplicates.append({"key": key, "error": "key is duplicated, keys must be unique."})
                seen[key] += 1

        return duplicates

    @staticmethod
    def get_key_bytes_from_key(signer_key: str):
        if not KeyCommon.validate_checksum(signer_key):
            raise Exception("key is invalid.")
        signer_key_bytes = base58.b58decode(signer_key)
        return signer_key_bytes[5:37]

    @staticmethod
    def get_public_key_from_private_key(signer_private_key: str):
        if not KeyCommon.validate_checksum(signer_private_key):
            raise Exception("signer_private_key is invalid.")
        private_key_bytes = KeyCommon.get_key_bytes_from_key(signer_private_key)
        signing_key = ed25519.SigningKey(private_key_bytes)
        public_key_bytes = signing_key.get_verifying_key().to_bytes()
        tmp = hashlib.sha256(hashlib.sha256(factom_sdk.utils.consts.PUBLIC_PREFIX_BYTES +
                                            public_key_bytes).digest()).digest()
        checksum = tmp[:4]
        return "".join(chr(x) for x in base58.b58encode(bytes(factom_sdk.utils.consts.PUBLIC_PREFIX_BYTES +
                                                              public_key_bytes + checksum)))

    @staticmethod
    def sign_content(signer_private_key: str, message: str):
        if not signer_private_key:
            raise Exception("signer_private_key is required.")
        if not KeyCommon.validate_checksum(signer_private_key):
            raise Exception("signer_private_key is invalid.")
        if not message:
            raise Exception("message is required.")
        private_key_bytes = KeyCommon.get_key_bytes_from_key(signer_private_key)
        secret_key = ed25519.SigningKey(private_key_bytes)
        message_bytes = message.encode()
        return "".join(chr(x) for x in base64.b64encode(secret_key.sign(message_bytes)))

    @staticmethod
    def validate_signature(signer_public_key: str, signature: str, message: str):
        if not signer_public_key:
            raise Exception("signer_public_key is required.")
        if not KeyCommon.validate_checksum(signer_public_key):
            raise Exception("signer_public_key is invalid.")
        if not signature:
            raise Exception("signature is required.")
        if not message:
            raise Exception("message is required.")
        signature_bytes = base64.b64decode(signature)
        message_bytes = message.encode()
        key_bytes = KeyCommon.get_key_bytes_from_key(signer_public_key)
        verify_key = ed25519.VerifyingKey(key_bytes)
        try:
            verify_key.verify(signature_bytes, message_bytes)
            return True
        except ed25519.BadSignatureError:
            return False
