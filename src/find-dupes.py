from glob import glob
from hashlib import sha1
from collections import Counter


def file_list() -> list:
    return glob('**/*', recursive=True)


def calculate_file_hash(arr: list) -> tuple:
    hash_dict = []
    for file in arr:
        file_hash = hash_file(file)
        if file_hash is not None:
            hash_dict.append(file_hash)
    return hash_dict


def hash_file(filename: str) -> dict:
    debug = False
    hash_obj = sha1()
    try:
        with open(filename, 'rb') as file:
            chunk = 0
            while chunk != b'':
                chunk = file.read(4096)
                hash_obj.update(chunk)
    except IsADirectoryError:
        if debug:
            print(f'{filename} is a directory')
        return
    return (filename, hash_obj.hexdigest())


def find_duplicates(file_list: list) -> dict:
    hash_list = [hash[1] for hash in file_list]
    duplicate_dict = Counter(hash_list)
    dupes = [hash_element for hash_element,
             count in duplicate_dict.items() if count > 1]
    if len(dupes) > 0:
        # TODO - Improve performance of the line below.
        return {dupe: [file for file in file_list if file[1] == dupe] for dupe in dupes}
    return dupes


def output_dupes(dupes: dict) -> None:
    if dupes:
        for dupe, dupes in dupes.items():
            print(f'sha1-hash: {dupe}')
            for file in dupes:
                print(f'\t file: {file[0]}')


if __name__ == '__main__':
    dict_of_files = calculate_file_hash(file_list())
    output_dupes(find_duplicates(dict_of_files))
