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
