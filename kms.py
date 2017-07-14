"""
Manage key securely
"""
import argparse
import re
import random
import string
import hashlib
import base64
import logging
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import AES
from google.cloud import datastore

LOGGER = logging.getLogger(__name__)

class NotFoundError(Exception):
    """
    Key not found execption
    """
    def __init__(self, key):
        super(NotFoundError, self).__init__("key {} not found".format(key))


class KeyManager(object):
    """
    Manage all keys
    """
    PUBLIC_KEY_ID = "publicKeyId"
    PRIVATE_KEY_ID = "privateKeyId"
    SECRET_KEY = "secretKey"
    NAMESPACE = "KMS"
    FIELD = "_field"
    NUM_BITS = 1024
    BLOCK_SIZE = 32
    PROJECT = None

    def __init__(self, fetch=True):
        """
        fetch the public and private keys from datastore and
        initialize it
        """
        self._client = datastore.Client(project=self.PROJECT)
        if fetch:
            self._public_key = RSA.importKey(self.get(self.PUBLIC_KEY_ID))
            self._private_key = RSA.importKey(self.get(self.PRIVATE_KEY_ID))
            self._secretKey = self._private_key.decrypt(self.get(self.SECRET_KEY))

    def _create_key(self, path, namespace=None):
        namespace = namespace or self.NAMESPACE
        return self._client.key(self.NAMESPACE, path, namespace=namespace)

    def _save(self, key, value):
        entity = datastore.Entity(key=key)
        entity.update({self.FIELD: value})
        self._client.put(entity)

    def _pad(self, value):
        pad = (self.BLOCK_SIZE - len(value) % self.BLOCK_SIZE)
        return value + pad * chr(pad)

    @staticmethod
    def _unpad(value):
        return value[:-ord(value[-1])]

    def encrypt(self, value):
        """
        encrypt public key
        """
        init_vector = Random.new().read(AES.block_size)
        cipher = AES.new(self._secretKey, AES.MODE_CBC, init_vector)
        return base64.b64encode(init_vector + cipher.encrypt(self._pad(value)))

    def encrypt_and_save(self, name, value):
        """
        encrypt the key value and save it to
        cloud datastore
        """
        key = self._create_key(name)
        encrypted_value = self.encrypt(value)
        self._save(key, encrypted_value[0])

    def get(self, name):
        """
        return value stored in datastore
        """
        data = self._client.get(self._create_key(name))
        if data is None:
            raise NotFoundError(name)
        return data.get(self.FIELD, None)

    def decrypt(self, value):
        """
        decrypt the value
        """
        value = base64.b64decode(value)
        init_vector = value[:AES.block_size]
        cipher = AES.new(self._secretKey, AES.MODE_CBC, init_vector)
        return self._unpad(cipher.decrypt(value[AES.block_size:]).decode("utf-8"))

    def get_and_decrypt(self, name):
        """
        return decrypted key
        """
        return self.decrypt(self.get(name))

    def delete(self, name):
        """
        remove key from storage
        """
        self._client.delete(self._create_key(name))

    def init(self, filename=None, passphrase=None):
        """
        initialize key manager
        """
        if isinstance(filename, basestring):
            rsa_key = RSA.importKey(open(filename, "rb").readlines(), passphrase=passphrase)
            if not rsa_key.has_private():
                raise ValueError("Private is missing")
        else:
            rsa_key = RSA.generate(self.NUM_BITS, Random.new().read)

        chars = string.ascii_letters + string.digits + "!@#$~`.,}{[]()"
        password_plain_text = ''.join([random.choice(chars) for _ in range(15)])
        password_hash = hashlib.sha256(password_plain_text).digest()
        password_encrypted = rsa_key.publickey().encrypt(password_hash)

        self._save(self._create_key(self.PRIVATE_KEY_ID), rsa_key.exportKey())
        self._save(self._create_key(self.PUBLIC_KEY_ID), rsa_key.publickey().exportKey())
        self._save(self._create_key(self.SECRET_KEY), password_encrypted)

def _save(args):
    regex = re.compile("^file://", re.I)
    if regex.search(args.source):
        data = "\n".join([l[:-1] for l in open(args.source[len("file://"):], "rb").readlines()])
    else:
        data = args.source
    key_manager = KeyManager()
    father = key_manager.encrypt(data)
    print father
    print key_manager.decrypt(father)
    key_manager.encrypt_and_save(args.name, data)

def _get(args):
    key_manager = KeyManager()
    try:
        key = key_manager.get_and_decrypt(args.name)
        print "*" * 50
        print key
        print "*" * 50
    except NotFoundError as ex:
        LOGGER.critical(ex)

def _delete(args):
    key_manager = KeyManager()
    key_manager.delete(args.name)

def _init(*args):
    key_manager = KeyManager(fetch=False)
    key_manager.init()

def _main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command")

    save = subparser.add_parser("save")
    save.add_argument("--name", "-n", help="Name of the key")
    save.add_argument("--source", help="source of data")

    get = subparser.add_parser("get")
    get.add_argument("--name", "-n", help="Name of the key")

    delete = subparser.add_parser("delete")
    delete.add_argument("--name", "-n", help="Name of the key")

    subparser.add_parser("init")

    func = {
        "save": _save,
        "get": _get,
        "delete": _delete,
        "init": _init
    }

    args = parser.parse_args()

    func[args.command](args)

KeyManager.PROJECT = "equifax-au-digital-dev"

if __name__ == '__main__':
    _main()
