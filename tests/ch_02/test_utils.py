import shutil
import tempfile
from pathlib import Path

from ch_03.utils import sync


def test_when_a_file_exists_int_the_source_but_not_in_destination():
    try:
        source = tempfile.mkdtemp()
        dest = tempfile.mkdtemp()
        content = 'Я тестовый файл!'
        (Path(source) / 'my-file').write_text(content)
        sync(source, dest)

        expected_path = Path(dest) / 'my-file'
        assert expected_path.exists()
        assert expected_path.read_text() == content
    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)


def test_when_a_file_has_been_renamed__in_the_source():
    try:
        source = tempfile.mkdtemp()
        dest = tempfile.mkdtemp()
        content = 'Я переименованный тестовый файл!'
        source_path = Path(source) / 'source-filename'
        old_dest_path = Path(dest) / 'dest-filename'
        expected_dest_path = Path(dest) / 'source-filename'
        source_path.write_text(content)
        old_dest_path.write_text(content)

        sync(source, dest)

        assert old_dest_path.exists() is False
        assert expected_dest_path.read_text() == content
    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)