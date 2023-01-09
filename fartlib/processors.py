import base64
import binascii
import hashlib


def b64e(string: str):
    return base64.b64encode(string.encode("utf-8")).decode("utf-8")


def enhex(string: str):
    return binascii.b2a_hex(string.encode("utf-8")).decode("utf-8")


def md5(string: str):
    return hashlib.md5(string.encode("utf-8")).hexdigest()


def sha1(string: str):
    return hashlib.sha1(string.encode("utf-8")).hexdigest()


def sha256(string: str):
    return hashlib.sha256(string.encode("utf-8")).hexdigest()


def sha512(string: str):
    return hashlib.sha256(string.encode("utf-8")).hexdigest()
