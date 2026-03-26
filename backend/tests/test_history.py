import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from backend.app import history


class HistoryTests(unittest.TestCase):
    def test_save_and_fetch_conversation_round_trip(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            history_path = Path(temp_dir) / "history.json"
            messages = [{"id": 1, "type": "user", "content": "tomatoes"}]

            with patch.object(history, "HISTORY_FILE", history_path):
                saved = history.save_conversation("abc", "Tomato Pasta", messages)
                fetched = history.get_conversation("abc")
                all_conversations = history.get_all_conversations()

            self.assertEqual(saved["id"], "abc")
            self.assertEqual(fetched["messages"], messages)
            self.assertEqual(len(all_conversations), 1)
            self.assertTrue(history_path.exists())

    def test_delete_conversation_removes_saved_record(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            history_path = Path(temp_dir) / "history.json"

            with patch.object(history, "HISTORY_FILE", history_path):
                history.save_conversation("abc", "Title", [])
                deleted = history.delete_conversation("abc")
                remaining = history.load_history()

            self.assertTrue(deleted)
            self.assertEqual(remaining, {})

    def test_clear_all_history_writes_empty_object(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            history_path = Path(temp_dir) / "history.json"

            with patch.object(history, "HISTORY_FILE", history_path):
                history.save_conversation("abc", "Title", [])
                history.clear_all_history()
                payload = json.loads(history_path.read_text(encoding="utf-8"))

            self.assertEqual(payload, {})


if __name__ == "__main__":
    unittest.main()
