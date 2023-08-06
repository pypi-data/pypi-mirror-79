import json
import os
import time

import pgpy
from redis import StrictRedis

from om.utils import config


class Encryption:
    key = None
    key_expiration = 0
    REDIS_HKEY = "kv"
    REDIS_KEY = "encryption_key"

    def __init__(self):
        self.redis = StrictRedis(host=config.string("REDIS_HOST", "localhost"),
                                 port=config.int("REDIS_PORT", 6379),
                                 db=config.int("REDIS_DB", 0))

    def get_key(self):
        if time.time() > self.key_expiration:
            data = self.redis.hget(self.REDIS_HKEY, self.REDIS_KEY)
            if not data:
                return None
            data = json.loads(data)
            self.key, _ = pgpy.PGPKey.from_blob(data["pubkey"])
            self.key_expiration = data["expiration"]
        return self.key

    def encrypt_file(self, file_name, out_file_name=None):
        with open(file_name, "rb") as file:
            compress = True
            ending = file_name.rsplit(".", 1)
            if ending in ["gz", "jpg", "jpeg"]:
                compress = False
            encrypted = self.encrypt_data(file.read(), compress)
        if encrypted:
            new_name = out_file_name or f"{file_name}.pgp"
            if not new_name.endswith(".pgp"):
                new_name = new_name + ".pgp"
            with open(new_name, "wb") as out:
                out.write(encrypted)
            os.remove(file_name)
            return True
        return False

    def encrypt_data(self, data, compress=True):
        compression = pgpy.constants.CompressionAlgorithm.ZLIB if compress else \
            pgpy.constants.CompressionAlgorithm.Uncompressed
        key = self.get_key()
        if not key:
            return None
        encrypted = key.encrypt(pgpy.PGPMessage.new(data), compression=compression)
        return bytes(encrypted)


if __name__ == "__main__":
    text = b"please decrypt me"
    encryption = Encryption()

    encrypted_text = encryption.encrypt_data(text, True)
    if encrypted_text:
        with open("/data/upload/files/test_encryption.txt.pgp", "wb") as outfile:
            outfile.write(encrypted_text)
    else:
        print("ENCRYPTION FAILED")

    with open("/data/test_encryption.txt", "wb") as new_file:
        new_file.write(text)
    encryption.encrypt_file("/data/test_encryption.txt", "/data/upload/files/test_encryption2.txt")
