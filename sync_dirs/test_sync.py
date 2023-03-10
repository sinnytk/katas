"""Test sync syncs"""
from pathlib import Path

from sync import sync


def test_copies_file_to_other_directory(tmp_path: Path):
    """sync should copy files from one directory to other"""
    # setup
    host_dir = tmp_path / "host"
    host_dir.mkdir()

    (host_dir / "virus1.txt").touch()
    (host_dir / "virus2.txt").touch()
    (host_dir / "virus3.txt").touch()

    ## target
    target_dir = tmp_path / "target"
    target_dir.mkdir()

    # before, the directories are out of sync (bc target doesn't have virus)
    assert not (target_dir / "virus1.txt").exists()
    assert not (target_dir / "virus2.txt").exists()
    assert not (target_dir / "virus3.txt").exists()

    # ✨✨✨
    sync(host_dir, target_dir)
    # ✨✨✨

    assert (target_dir / "virus1.txt").exists()
    assert (target_dir / "virus2.txt").exists()
    assert (target_dir / "virus3.txt").exists()


def test_removes_files_that_are_not_in_source(tmp_path: Path):
    """If a file exists in destination but not in source, it should be removed"""

    # > monk
    monk_dir = tmp_path / "monk"
    monk_dir.mkdir()

    # > fool
    #   > attachment1.txt
    #   > attachment2.txt
    fool_dir = tmp_path / "fool"
    fool_dir.mkdir()
    (fool_dir / "attachment1.txt").touch()
    (fool_dir / "attachment2.txt").touch()

    # fool discovers attachments through introspection
    assert (fool_dir / "attachment1.txt").exists()
    assert (fool_dir / "attachment2.txt").exists()

    # monk trains fool
    sync(monk_dir, fool_dir)

    # fool should not have any attachments anymore
    assert not (fool_dir / "attachment1.txt").exists()
    assert not (fool_dir / "attachment2.txt").exists()
