import unittest
import os
import tempfile
import shutil
from paser.tools import file_tools

class MockContext:
    def get_safe_path(self, path):
        return os.path.abspath(path)

file_tools.context = MockContext()

class TestFileTools(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_read_file_success(self):
        path = os.path.join(self.test_dir, "test.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write("Hola Mundo")
        self.assertEqual(file_tools.read_file(path), "Hola Mundo")

    def test_read_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            file_tools.read_file("non_existent.txt")

    def test_write_file_success(self):
        path = os.path.join(self.test_dir, "nuevo.txt")
        result = file_tools.write_file(path, "Contenido nuevo")
        self.assertIn("exitosamente", result)
        with open(path, "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), "Contenido nuevo")

if __name__ == '__main__':
    unittest.main()