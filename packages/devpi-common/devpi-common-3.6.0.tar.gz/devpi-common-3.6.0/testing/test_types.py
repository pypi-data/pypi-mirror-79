from devpi_common.types import CompareMixin
from devpi_common.types import parse_hash_spec
import hashlib


def test_CompareMixin():
    class A(CompareMixin):
        def __init__(self, count):
            self.cmpval = count
    l = list(map(A, range(10)))
    assert max(reversed(l)).cmpval == 9


def test_parsehashspec():
    hash_algo, hash_value = parse_hash_spec("l1kj23")
    assert hash_algo is None and hash_value is None
    hash_algo, hash_value = parse_hash_spec("xyz=123098123")
    assert hash_algo is None and hash_value is None

    digest = hashlib.md5(b'123').hexdigest()
    hash_algo, hash_value = parse_hash_spec("md5=" + digest)
    assert hash_algo(b'123').hexdigest() == digest

    digest = hashlib.sha256(b'123').hexdigest()
    hash_algo, hash_value = parse_hash_spec("sha256=" + digest)
    assert hash_algo(b'123').hexdigest() == digest
