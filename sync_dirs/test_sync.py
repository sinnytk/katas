"""Test sync syncs"""
from pathlib import Path

from sync import sync


def test_copies_file_to_other_directory(tmp_path: Path):
    """sync should copy files from one directory to other"""
    # setup
    host_dir = tmp_path / "host"
    host_dir.mkdir()

    (host_dir / "virus1.txt").write_text("alpha")
    (host_dir / "virus2.txt").write_text("beta")
    (host_dir / "virus3.txt").write_text("gamma")

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


def test_renames_files_in_dest_if_content_same(tmp_path: Path):
    """If a file exists in destination with same content but different name, rename it to match source"""

    # > trainer
    #   > strength.txt
    trainer_dir = tmp_path / "trainer"
    trainer_dir.mkdir()
    (trainer_dir / "strength.txt").write_text("foo1")

    # > novice
    #   > potential.txt
    novice_dir = tmp_path / "novice"
    novice_dir.mkdir()
    (novice_dir / "potential.txt").write_text("foo1")

    # training begins!
    # 💪🏋️🥋
    sync(trainer_dir, novice_dir)
    # 💪🏋️🥋

    # original file doesn't exist anymore
    assert not (novice_dir / "potential.txt").exists()
    # renamed file exists
    assert (novice_dir / "strength.txt").exists()
    # assert content not changed!
    assert (novice_dir / "strength.txt").read_text() == "foo1"
