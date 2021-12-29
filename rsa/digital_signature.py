from typing import Callable
from . import rsa


def sign_message(message: str, private_key: tuple[int, int], hash_function: Callable[[str], str]) -> int:
    message_hash = hash_function(message)
    message_hash = int(message_hash, 16)
    return rsa.encode_int(private_key, message_hash)


def verify_signature(message: str,
                     signature: int,
                     public_key: tuple[int, int],
                     hash_function: Callable[[str], str]) -> bool:
    signature_message_hash = rsa.encode_int(public_key, signature)
    expected_message_hash = int(hash_function(message), 16)
    return signature_message_hash == expected_message_hash
