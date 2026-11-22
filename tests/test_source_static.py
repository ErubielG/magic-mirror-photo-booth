"""Static checks for the published source; not the original event test suite."""
import ast
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "src" / "booth20.py"

class SourceChecks(unittest.TestCase):
    def test_python_syntax(self):
        ast.parse(SOURCE.read_text(encoding="utf-8"))

    def test_embedded_event_password_not_published(self):
        contents = SOURCE.read_text(encoding="utf-8")
        self.assertNotIn("fotos2026", contents)
        self.assertNotIn('PIN_FABRICA = "2468"', contents)

if __name__ == "__main__":
    unittest.main()
