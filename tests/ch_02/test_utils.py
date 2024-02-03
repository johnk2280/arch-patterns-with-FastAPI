from pathlib import Path

from ch_03.utils import FakeFileSystem
from ch_03.utils import sync


def test_when_a_file_exists_int_the_source_but_not_in_destination():
    src_hashes = {'hash1': 'fn1'}
    dst_hashes = {}

    filesystem = FakeFileSystem()

    # fake reader
    reader = {'/src': src_hashes, '/dest': dst_hashes}

    sync(reader.pop, filesystem, '/src', '/dest')
    assert filesystem.commands == [
        ('COPY', Path('/src/fn1'), Path('/dest/fn1')),
    ]


def test_when_a_file_has_been_renamed__in_the_source():
    src_hashes = {'hash1': 'fn1'}
    dst_hashes = {'hash1': 'fn2'}
    filesystem = FakeFileSystem()

    # fake reader
    reader = {'/src': src_hashes, '/dest': dst_hashes}

    sync(reader.pop, filesystem, '/src', '/dest')
    assert filesystem.commands == [
        ('MOVE', Path('/dest/fn2'), Path('/dest/fn1')),
    ]
