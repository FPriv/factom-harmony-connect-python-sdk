import base64


class CommonUtil:
    @staticmethod
    def decode_response(response={}):
        if "data" in response:
            array_decode = ["external_ids", "content", "name"]
            if type(response["data"]).__name__ == "list":
                for item in response["data"]:
                    for arr in array_decode:
                        if arr in item:
                            if type(item[arr]).__name__ == "list":
                                decoded = []
                                if arr == "external_ids" and len(item[arr]) >= 6 \
                                        and (base64.b64decode(item[arr][0]) == b"SignedChain"
                                             or base64.b64decode(item[arr][0]) == b"SignedEntry") \
                                        and base64.b64decode(item[arr][1]).hex() == "01":
                                    for idx, val in enumerate(item[arr]):
                                        if idx == 1:
                                            decoded.append("0x" + base64.b64decode(val).hex())
                                        elif idx == 4:
                                            decoded.append(base64.b64decode(val).hex())
                                        else:
                                            decoded.append(base64.b64decode(val))
                                else:
                                    for val in item[arr]:
                                        decoded.append(base64.b64decode(val))
                                item[arr] = decoded
                            else:
                                item[arr] = base64.b64decode(item[arr])
            else:
                for arr in array_decode:
                    if arr in response["data"]:
                        if type(response["data"][arr]).__name__ == "list":
                            decoded = []
                            if arr == "external_ids" and len(response["data"][arr]) >= 6 \
                                    and (base64.b64decode(response["data"][arr][0]) == b"SignedChain"
                                         or base64.b64decode(response["data"][arr][0]) == b"SignedEntry") \
                                    and base64.b64decode(response["data"][arr][1]).hex() == "01":
                                for idx, val in enumerate(response["data"][arr]):
                                    if idx == 1:
                                        decoded.append("0x" + base64.b64decode(val).hex())
                                    elif idx == 4:
                                        decoded.append(base64.b64decode(val).hex())
                                    else:
                                        decoded.append(base64.b64decode(val))
                            else:
                                for val in response["data"][arr]:
                                    decoded.append(base64.b64decode(val))
                            response["data"][arr] = decoded
                        else:
                            response["data"][arr] = base64.b64decode(response["data"][arr])
        return response

    @staticmethod
    def is_empty_string(value):
        _type = type(value).__name__
        return (_type == "string" and value.strip() == "") or _type != "string"

    @staticmethod
    def is_empty_arr(arr):
        return type(arr).__name__ == "list" and len(arr) == 0
