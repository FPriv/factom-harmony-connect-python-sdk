from factom_sdk.utils.key_common import KeyCommon


class Utils:
    @staticmethod
    def generate_key_pair():
        return KeyCommon.create_key_pair()
