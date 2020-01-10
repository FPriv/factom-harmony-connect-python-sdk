from factom_sdk.utils.key_common import KeyCommon


class Utils:
    @staticmethod
    def to_military_timezone_str(dt):
        return dt.isoformat().replace("+00:00", "Z")

    @staticmethod
    def generate_key_pair():
        """Creates a Public/Private Key Pair.

        Returns:
            A key pair object with Public and Private keys.
        """
        return KeyCommon.create_key_pair()
raw_private_key: str = None
    @staticmethod
    def convert_raw_to_key_pair(raw_private_key):
        """Convert standard ed25519 keys into idpub/idsec formatted keys.

        Returns:
            A key bytes array
        """
        return KeyCommon.create_key_pair(raw_private_key)

    @staticmethod
    def convert_to_raw(signer_key: str):
        """Convert idpub/idsec formatted keys into standard ed25519.

        Returns:
            A key bytes array
        """
        return KeyCommon.get_key_bytes_from_key(signer_key)
