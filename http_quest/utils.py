from base64 import standard_b64decode, standard_b64encode
from urllib.parse import urlencode


def get_banner() -> str:
    return """ ██░ ██ ▄▄▄█████▓▄▄▄█████▓ ██▓███       █████   █    ██ ▓█████   ██████ ▄▄▄█████▓
▓██░ ██▒▓  ██▒ ▓▒▓  ██▒ ▓▒▓██░  ██▒   ▒██▓  ██▒ ██  ▓██▒▓█   ▀ ▒██    ▒ ▓  ██▒ ▓▒
▒██▀▀██░▒ ▓██░ ▒░▒ ▓██░ ▒░▓██░ ██▓▒   ▒██▒  ██░▓██  ▒██░▒███   ░ ▓██▄   ▒ ▓██░ ▒░
░▓█ ░██ ░ ▓██▓ ░ ░ ▓██▓ ░ ▒██▄█▓▒ ▒   ░██  █▀ ░▓▓█  ░██░▒▓█  ▄   ▒   ██▒░ ▓██▓ ░ 
░▓█▒░██▓  ▒██▒ ░   ▒██▒ ░ ▒██▒ ░  ░   ░▒███▒█▄ ▒▒█████▓ ░▒████▒▒██████▒▒  ▒██▒ ░ 
 ▒ ░░▒░▒  ▒ ░░     ▒ ░░   ▒▓▒░ ░  ░   ░░ ▒▒░ ▒ ░▒▓▒ ▒ ▒ ░░ ▒░ ░▒ ▒▓▒ ▒ ░  ▒ ░░   
 ▒ ░▒░ ░    ░        ░    ░▒ ░         ░ ▒░  ░ ░░▒░ ░ ░  ░ ░  ░░ ░▒  ░ ░    ░    
 ░  ░░ ░  ░        ░      ░░             ░   ░  ░░░ ░ ░    ░   ░  ░  ░    ░      
 ░  ░  ░                                  ░       ░        ░  ░      ░           
                                                                                 """


def base64_encode(text: str) -> str:
    return standard_b64encode(text.encode("utf-8")).decode("utf-8")


def base64_decode(text: str) -> str:
    return standard_b64decode(text.encode("utf-8")).decode("utf-8")


def add_query_params(url: str, **params: str) -> str:
    return url + "?" + urlencode(params)


def get_masked_password(password: str, secret: str, given_secret: str) -> str:
    """
    Use secret correctness as a password mask.
    For each correct secret character, password character in the same position will be
    exposed.
    """

    if len(password) != len(secret):
        raise ValueError("Password and secret should be the same length")

    masked_password = ""

    for index in range(len(secret)):
        try:
            is_same_character = secret[index] == given_secret[index]
        except IndexError:
            masked_password += "*"
            continue

        if is_same_character:
            masked_password += password[index]
            continue

        masked_password += "*"

    return masked_password
