"""Test sync syncs"""
from pathlib import Path

from sync import prepare_operations


def test_if_directories_are_synced_no_operations():
    """If both directories are same, there shouldn't be any operations to perform"""
    src_dir_map = {"somehash": "file1.txt"}
    dst_dir_map = {"somehash": "file1.txt"}

    assert [] == prepare_operations(src_dir_map, dst_dir_map, Path("src"), Path("dst"))


def test_copies_file_to_other_directory():
    """sync should copy files from one directory to other"""

    host_dir_map = {"alpha": "virus1.txt", "beta": "virus2.txt", "gamma": "virus3.txt"}
    target_dir_map = {}

    excepted_operations = [
        ["COPY", Path("host/virus1.txt"), Path("target/virus1.txt")],
        ["COPY", Path("host/virus2.txt"), Path("target/virus2.txt")],
        ["COPY", Path("host/virus3.txt"), Path("target/virus3.txt")],
    ]

    assert excepted_operations == prepare_operations(
        host_dir_map, target_dir_map, Path("host"), Path("target")
    )


def test_removes_files_that_are_not_in_source():
    """If a file exists in destination but not in source, it should be removed"""

    # > monk
    monk_dir_map = {}

    # > fool
    #   > attachment1.txt
    #   > attachment2.txt
    fool_dir_map = {"foo": "attachment1.txt", "bar": "attachment2.txt"}

    # all of fool's attachements should be removed
    expected_operations = [
        ["DELETE", Path("fool/attachment1.txt")],
        ["DELETE", Path("fool/attachment2.txt")],
    ]
    assert expected_operations == prepare_operations(
        monk_dir_map, fool_dir_map, Path("monk"), Path("fool")
    )


def test_renames_files_in_dest_if_content_same():
    """If a file exists in destination with same content but different name, rename it to match source"""

    # > trainer
    #   > strength.txt
    trainer_dir_map = {"foo1": "strength.txt"}

    # > novice
    #   > potential.txt
    novice_dir_map = {"foo1": "potential.txt"}  # same hash (foo1), but different name

    # after training, novice's potential is now strength
    expected_operations = [
        ["RENAME", Path("novice/potential.txt"), Path("novice/strength.txt")]
    ]

    assert expected_operations == prepare_operations(
        trainer_dir_map, novice_dir_map, Path("trainer"), Path("novice")
    )
