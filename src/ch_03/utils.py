import hashlib
import os
import shutil
from collections.abc import Callable
from collections.abc import Generator
from pathlib import Path
from typing import Protocol

BLOCK_SIZE = 65536


def hash_file(path: Path) -> str:
    hasher = hashlib.sha1()
    with path.open('rb') as file:
        buf = file.read(BLOCK_SIZE)
        while buf:
            hasher.update(buf)
            buf = file.read(BLOCK_SIZE)

    return hasher.hexdigest()


# Первая итерация
# def sync(source: str, dest: str) -> None:
#     # Обойти исходную папку и создать словарь имен файлов
#
#     source_hashes = {}
#     for folder, _, files in os.walk(source):
#         for file in files:
#             source_hashes[hash_file(Path(folder) / file)] = file
#
#     seen = set()  # Отслеживать фалы, найденные в целевой папке
#
#     # Обойти целевую папку и получить имена файлов и хеши
#     for folder, _, files in os.walk(dest):
#         for file in files:
#             dest_path = Path(folder) / file
#             dest_hash = hash_file(dest_path)
#             seen.add(dest_hash)
#
#             # Если в целевой папке есть файл,
#             # которого нет в источнике, то удалить
#             if dest_hash not in source_hashes:
#                 dest_path.unlink()
#
#             # если в целевой папке есть файл, который имеет другой путь
#             # в источнике, то переместить его в правильный путь
#             elif (dest_hash in source_hashes
#                   and file != source_hashes[dest_hash]):
#                 shutil.move(dest_path, Path(folder) / source_hashes[
#                 dest_hash])
#
#     # Каждый файл, который появляется в источнике, но не в месте назначения,
#     # скопировать в целевую папку
#     for src_hash, file in source_hashes.items():
#         if src_hash not in seen:
#             shutil.copy(Path(source) / file, Path(dest) / file)


# Вторая итерация: рефакторинг - разделение с использованием подхода
# "функциональное ядро - императивная оболочка"
def read_path_and_hashes(root: str) -> dict[str, str]:
    hashes = {}
    for folder, _, files in os.walk(root):
        for file in files:
            hashes[hash_file(Path(folder, file))] = file

    return hashes


def determine_actions(
    source_hashes: dict[str, str],
    dest_hashes: dict[str, str],
    source: Path,
    dest: Path,
) -> Generator[tuple[str, Path, Path], None, None]:
    # Обойти папку-источник и проверить наличие фалов в целевой папке
    for sha, filename in source_hashes.items():
        # Если в целевой папке отсутствует фал
        if sha not in dest_hashes:
            source_path = Path(source) / filename
            dest_path = Path(dest) / filename
            yield 'COPY', source_path, dest_path

        # Если в целевой папке имеется файл, который имеет другой путь
        elif dest_hashes[sha] != filename:
            old_dest_path = Path(dest) / dest_hashes[sha]
            new_dest_path = Path(dest) / filename
            yield 'MOVE', old_dest_path, new_dest_path

    # Если в целевой папке имеется файл, который отсутствует в источнике
    for sha, filename in dest_hashes.items():
        if sha not in source_hashes:
            yield 'DELETE', dest / filename, ''


# def sync(source: str, dest: str) -> None:
#     # Шаг 1 с императивным ядром: собрать входные данные
#     source_hashes = read_path_and_hashes(source)
#     dest_hashes = read_path_and_hashes(dest)
#
#     # Шаг 2: Вызвать функциональное ядро
#     actions = determine_actions(
#         source_hashes,
#         dest_hashes,
#         Path(source),
#         Path(dest),
#     )
#
#     # Шаг 3 С императивным ядром: применить операции ввода-вывода данных
#     for action, *paths in actions:
#         match action.upper():
#             case 'COPY':
#                 shutil.copyfile(*paths)
#             case 'MOVE':
#                 shutil.move(*paths)
#             case 'DELETE':
#                 os.unlink(paths[0])
#             case _:
#                 raise ValueError(f'Unknown action: {action}')


# Третья итерация. Внедряем новые зависимости в верхнеуровневую функцию sync().
# Теперь sync() принимает на вход (выставляет наружу) 2 новые зависимости:
# filesystem и reader.

class HasCopy(Protocol):
    def copy(self, src: Path, dest: Path) -> None: ...


class HasMove(Protocol):
    def move(self, src: Path, dest: Path) -> None: ...


class HasDelete(Protocol):
    def delete(self, src: Path, dest: Path) -> None: ...


class FileSystemProtocol(HasCopy, HasMove, HasDelete, Protocol):
    ...


class FakeFileSystem(FileSystemProtocol): ...

def sync(
    reader: Callable[[str], dict[str, str]],
    filesystem: FileSystemProtocol,
    source: str,
    dest: str
) -> None:
    # Шаг 1 с императивным ядром: собрать входные данные
    source_hashes = reader(source)
    dest_hashes = reader(dest)

    # Шаг 2: Вызвать функциональное ядро. Функциональное перенесено обратно
    # из determine_actions() в верхнеуровневую функцию sync().
    for sha, filename in source_hashes.items():
        # Если в целевой папке отсутствует фал
        if sha not in dest_hashes:
            source_path = Path(source) / filename
            dest_path = Path(dest) / filename
            yield 'COPY', source_path, dest_path

        # Если в целевой папке имеется файл, который имеет другой путь
        elif dest_hashes[sha] != filename:
            old_dest_path = Path(dest) / dest_hashes[sha]
            new_dest_path = Path(dest) / filename
            yield 'MOVE', old_dest_path, new_dest_path

    # Если в целевой папке имеется файл, который отсутствует в источнике
    for sha, filename in dest_hashes.items():
        if sha not in source_hashes:
            yield 'DELETE', dest / filename, ''

