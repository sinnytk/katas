import shutil
import sys
from pathlib import Path


def copy_missing_files(src: Path, dst: Path):
    """Copies files to `dst` that are only in `src`"""
    src_files = set(file.name for file in src.iterdir())
    dst_files = set(file.name for file in dst.iterdir())

    files_only_in_src = src_files - dst_files

    for file in files_only_in_src:
        shutil.copyfile(src / file, dst / file)


def remove_redundant_files(src: Path, dst: Path):
    """Deletes files that are in `dst` but not in `src"""
    src_files = set(file.name for file in src.iterdir())
    dst_files = set(file.name for file in dst.iterdir())

    files_only_in_dst = dst_files - src_files

    for file in files_only_in_dst:
        (dst / file).unlink()


def sync(dir1: Path, dir2: Path) -> None:
    """Synchronises two directories.
    1. If a file exists in dir1 but not in dir2, it should be copied over ✅
    2. If a file exists in dir1 but has a different name in dir2, rename the file in dir2 to match ❌
    3. If a file exists in dir2 but not in dir1, it should be deleted ✅
    """
    copy_missing_files(dir1, dir2)
    remove_redundant_files(dir1, dir2)


def main():
    input_dirs = sys.argv[1:]
    dir1, dir2 = map(Path, input_dirs)

    sync(dir1, dir2)


if __name__ == "__main__":
    main()
