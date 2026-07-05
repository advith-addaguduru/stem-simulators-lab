import sqlite3
from unittest.mock import patch

from core import audit


class RaisingConn:
    def execute(self, *args, **kwargs):
        raise sqlite3.IntegrityError("FOREIGN KEY constraint failed")


class RaisingDB:
    def __enter__(self):
        return RaisingConn()

    def __exit__(self, exc_type, exc, tb):
        return False


def test_log_handles_invalid_user_id():
    with patch("core.audit.get_db", return_value=RaisingDB()):
        with patch("core.audit._audit.info") as mock_info:
            audit.log("SIM_ACCESS", user_id=0, username="guest", detail="simulator")

    mock_info.assert_called_once()
