import os
import tempfile
import time
import pytest

from app.cleanup.file_cleanup import cleanup_old_files


# 🧪 Helper to create test file with custom age
def create_test_file(directory, name, days_old=0):
    file_path = os.path.join(directory, name)

    with open(file_path, "w") as f:
        f.write("test data")

    # Modify file time
    old_time = time.time() - (days_old * 86400)
    os.utime(file_path, (old_time, old_time))

    return file_path


# 🧪 Test: old file should be deleted
def test_old_file_deleted(monkeypatch):
    with tempfile.TemporaryDirectory() as temp_dir:
        # Override config dynamically
        monkeypatch.setattr("app.config.CLEANUP_DIRECTORY", temp_dir)
        monkeypatch.setattr("app.config.RETENTION_DAYS", 7)

        old_file = create_test_file(temp_dir, "old.txt", days_old=10)

        result = cleanup_old_files()

        assert result["deleted_files"] == 1
        assert not os.path.exists(old_file)


# 🧪 Test: new file should NOT be deleted
def test_new_file_not_deleted(monkeypatch):
    with tempfile.TemporaryDirectory() as temp_dir:
        monkeypatch.setattr("app.config.CLEANUP_DIRECTORY", temp_dir)
        monkeypatch.setattr("app.config.RETENTION_DAYS", 7)

        new_file = create_test_file(temp_dir, "new.txt", days_old=1)

        result = cleanup_old_files()

        assert result["deleted_files"] == 0
        assert os.path.exists(new_file)


# 🧪 Test: directory does not exist
def test_directory_not_found(monkeypatch):
    monkeypatch.setattr("app.config.CLEANUP_DIRECTORY", "/invalid/path")

    result = cleanup_old_files()

    assert result["status"] == "failed"