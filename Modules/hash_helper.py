import base64
import hashlib


def file_to_b32_hash(filename):
    with open(filename, "rb") as f:
        m = hashlib.sha256()
        m.update(f.read())
        sha = m.digest()
        return base64.b32encode(sha).strip("=")

