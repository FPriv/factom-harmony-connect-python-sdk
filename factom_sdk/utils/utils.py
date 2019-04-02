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
