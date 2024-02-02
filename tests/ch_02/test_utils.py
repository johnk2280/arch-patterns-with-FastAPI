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

