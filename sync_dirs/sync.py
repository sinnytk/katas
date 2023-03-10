import shutil
import sys
from pathlib import Path


def sync(dir1: Path, dir2: Path) -> None:
    dir_files = lambda dir: [file.name for file in dir.iterdir()]
    dir1_files = set(dir_files(dir1))
    dir2_files = set(dir_files(dir2))

    files_in_dir1_only = dir1_files - dir2_files

    for file in files_in_dir1_only:
        shutil.copyfile(dir1 / file, dir2 / file)


def main():
    input_dirs = sys.argv[1:]
    dir1, dir2 = map(Path, input_dirs)

    sync(dir1, dir2)


if __name__ == "__main__":
    main()
