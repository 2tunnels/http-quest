from base64 import standard_b64decode, standard_b64encode


def reverse(text: str) -> str:
    return text[::-1]


def base64_encode(text: str) -> str:
    return standard_b64encode(text.encode("utf-8")).decode("utf-8")


def base64_decode(text: str) -> str:
    return standard_b64decode(text.encode("utf-8")).decode("utf-8")
