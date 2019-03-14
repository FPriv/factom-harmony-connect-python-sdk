import base64


class CommonUtil:
    @staticmethod
    def decode_response(response: dict = None):
        if response is None:
            response = {}
        if "data" in response:
            array_decode = ["external_ids", "content", "names"]
            if isinstance(response["data"], list):
                for item in response["data"]:
                    for arr in array_decode:
                        if arr in item:
                            item[arr] = CommonUtil.decode(arr, item[arr])
            else:
                for arr in array_decode:
                    if arr in response["data"]:
                        response["data"][arr] = CommonUtil.decode(arr, response["data"][arr])
        return response

    @staticmethod
    def decode(name: str, data):
        if isinstance(data, list):
            decoded = []
            if name == "external_ids" and len(data) >= 6 \
                    and (base64.b64decode(data[0]) == b"SignedChain"
                         or base64.b64decode(data[0]) == b"SignedEntry") \
                    and base64.b64decode(data[1]).hex() == "01":
                for idx, val in enumerate(data):
                    if idx == 1:
                        decoded.append("0x" + base64.b64decode(val).hex())
                    elif idx == 4:
                        decoded.append(base64.b64decode(val).hex())
                    else:
                        decoded.append("".join(chr(x) for x in base64.b64decode(val)))
            else:
                decoded = ["".join(chr(x) for x in base64.b64decode(val)) for val in data]
            return decoded
        else:
            return "".join(chr(x) for x in base64.b64decode(data))

    @staticmethod
    def base64_encode(value):
        if isinstance(value, str):
            return "".join(chr(x) for x in base64.b64encode(value.encode()))
        return "".join(chr(x) for x in base64.b64encode(value))
