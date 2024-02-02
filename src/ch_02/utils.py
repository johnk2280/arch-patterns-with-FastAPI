import hashlib
from pathlib import Path

BLOCK_SIZE = 65536


def hash_file(path: Path) -> str:
    hasher = hashlib.sha1()
    with path.open('rb') as file:
        buf = file.read(BLOCK_SIZE)
        while buf:
            hasher.update(buf)
            buf = file.read(BLOCK_SIZE)

    return hasher.hexdigest()


