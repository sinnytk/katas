import hashlib
import shutil
import sys
from pathlib import Path
from typing import Dict, List


def hash_file(file: Path) -> str:
    """Returns the contents of given file as a hashed hex digest"""
    return hashlib.sha256(file.read_bytes()).hexdigest()


def directory_map(dir: Path) -> str:
    """Given a directory, returns a dictionary of hashed file content to their file name"""
    return {hash_file(file): file.name for file in dir.iterdir() if file.is_file()}


def prepare_operations(
    src_dir_map: Dict, dst_dir_map: Dict, src_dir: Path, dst_dir: Path
) -> List[Dict]:
    """Returns a list of operations to perform for syncing the directories
    e.g
    input: {"foo": "f1.txt"}, {"bar": "f2.txt"}, Path("src"), Path("dst")
    output: [{"COPY", "src/f1.txt", "dst/f1.txt"}, {"DELETE", "dst/f2.txt"}]
    """

    # if directories are already synced, no operations!
    if src_dir_map == dst_dir_map:
        return []

    operations = []

    for src_file_hash, src_file_name in src_dir_map.items():
        dst_file_name = dst_dir_map.get(src_file_hash)

        # if file is in source but not in destination, copy it over
        if not dst_file_name:
            operations.append(
                ["COPY", src_dir / src_file_name, dst_dir / src_file_name]
            )

        # if file is in destination with a different name, rename it
        elif dst_file_name != src_file_name:
            operations.append(
                ["RENAME", dst_dir / dst_file_name, dst_dir / src_file_name]
            )

    for dst_file_hash, dst_file_name in dst_dir_map.items():
        if dst_file_hash not in src_dir_map:
            operations.append(["DELETE", dst_dir / dst_file_name])

    return operations


def perform_operations(operations: List[dict]):
    for operation in operations:
        opcode = operation[0]
        if opcode == "COPY":
            src, dst = operation[1:]
            print(f"COPYING {src} to {dst}")
            shutil.copyfile(src, dst)
        elif opcode == "RENAME":
            dst, src = operation[1:]
            print(f"RENAMING {dst} to {src}")
            dst.rename(src)
        elif opcode == "DELETE":
            dst = operation[1]
            print(f"DELETING {dst}")
            dst.unlink()
        else:
            raise Exception("Incorrect operation!")


def sync(dir1: Path, dir2: Path) -> None:
    """Synchronises two directories.
    1. If a file exists in dir1 but not in dir2, it should be copied over ✅
    2. If a file exists in dir1 but has a different name in dir2, rename the file in dir2 to match ✅
    3. If a file exists in dir2 but not in dir1, it should be deleted ✅
    """
    operations = prepare_operations(
        directory_map(dir1), directory_map(dir2), dir1, dir2
    )
    perform_operations(operations)


def main():
    input_dirs = sys.argv[1:]
    dir1, dir2 = map(Path, input_dirs)

    sync(dir1, dir2)


if __name__ == "__main__":
    main()
