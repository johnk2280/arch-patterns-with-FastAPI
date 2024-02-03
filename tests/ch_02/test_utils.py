import shutil
import tempfile
from pathlib import Path

from ch_03.utils import determine_actions
from ch_03.utils import sync


def test_when_a_file_exists_int_the_source_but_not_in_destination():
    src_hashes = {'hash1': 'fn1'}
    dst_hashes = {}
    actions = determine_actions(
        src_hashes,
        dst_hashes,
        Path('/src'),
        Path('/dest'),
    )
    assert list(actions) == [('COPY', Path('/src/fn1'), Path('/dest/fn1'))]


def test_when_a_file_has_been_renamed__in_the_source():
    src_hashes = {'hash1': 'fn1'}
    dst_hashes = {'hash1': 'fn2'}
    actions = determine_actions(
        src_hashes,
        dst_hashes,
        Path('/src'),
        Path('/dest'),
    )
    assert list(actions) == [('MOVE', Path('/dest/fn2'), Path('/dest/fn1'))]
