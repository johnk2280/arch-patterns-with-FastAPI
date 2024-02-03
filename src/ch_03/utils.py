import hashlib
import os
import shutil
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


def read_path_and_hashes(root: str) -> dict[str, str]:
    hashes = {}
    for folder, _, files in os.walk(root):
        for file in files:
            hashes[hash_file(Path(folder, file))] = file

    return hashes


# TODO: реализовать
def determine_actions(
    source_hashes: dict[str, str],
    dest_hashes: dict[str, str],
    source: str,
    dest: str,
) -> list[tuple[str, str, str]]:
    pass


def sync(source: str, dest: str) -> None:
    # Шаг 1 с императивным ядром: собрать входные данные
    source_hashes = read_path_and_hashes(source)
    dest_hashes = read_path_and_hashes(dest)

    # Шаг 2: Вызвать функциональное ядро
    actions = determine_actions(source_hashes, dest_hashes, source, dest)

    # Шаг 3 С императивным ядром: применить операции ввода-вывода данных
    for action, *paths in actions:
        match action.upper():
            case 'COPY':
                shutil.copyfile(*paths)
            case 'MOVE':
                shutil.move(*paths)
            case 'DELETE':
                os.unlink(paths[0])
            case _:
                raise ValueError(f'Unknown action: {action}')

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
