import unittest
import os
from pathlib import Path
from paser.tools.file_tools import replace_string, update_line, write_file
from paser.tools.core_tools import ToolError

class TestFileMutation(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_mutation_target.txt"
        self.content = "Line 1: Hello World\nLine 2: Paser Integrity\nLine 3: Sentinel of Truth"
        write_file(self.test_file, self.content)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_replace_string_success(self):
        # Test basic replacement
        result = replace_string(self.test_file, "Hello World", "Sentinel")
        self.assertEqual(result, 'OK')
        with open(self.test_file, 'r') as f:
            self.assertIn("Line 1: Sentinel", f.read())

    def test_replace_string_not_found(self):
        # Test string not found
        with self.assertRaises(ToolError) as cm:
            replace_string(self.test_file, "NonExistentString", "Replacement")
        self.assertEqual(str(cm.exception), 'String not found')

    def test_replace_string_multiple_matches(self):
        # Setup file with multiple matches
        multi_content = "Match here\nMatch there"
        write_file(self.test_file, multi_content)
        with self.assertRaises(ToolError) as cm:
            replace_string(self.test_file, "Match", "Replacement")
        self.assertEqual(str(cm.exception), 'Multiple matches found')

    def test_update_line_success(self):
        # Test updating the middle line
        result = update_line(self.test_file, 2, "Line 2: Updated Content")
        self.assertEqual(result, 'OK')
        with open(self.test_file, 'r') as f:
            lines = f.read().splitlines()
            self.assertEqual(lines[1], "Line 2: Updated Content")

    def test_update_line_first_last(self):
        # Test updating first line
        update_line(self.test_file, 1, "New First Line")
        # Test updating last line
        update_line(self.test_file, 3, "New Last Line")
        with open(self.test_file, 'r') as f:
            lines = f.read().splitlines()
            self.assertEqual(lines[0], "New First Line")
            self.assertEqual(lines[2], "New Last Line")

    def test_update_line_out_of_range(self):
        # Test line number too high
        with self.assertRaises(ToolError) as cm:
            update_line(self.test_file, 10, "Out of range")
        self.assertEqual(str(cm.exception), 'Line out of range')
        
        # Test line number too low
        with self.assertRaises(ToolError) as cm:
            update_line(self.test_file, 0, "Out of range")
        self.assertEqual(str(cm.exception), 'Line out of range')


    def test_split_file_success(self):
        # Setup file for splitting
        split_content = "Part A: Header\n---SPLIT---\nPart B: Body"
        split_file_name = "test_split.txt"
        write_file(split_file_name, split_content)
        
        from paser.tools.file_tools import split_file
        result = split_file(split_file_name, "---SPLIT---")
        self.assertEqual(result, 'OK')
        
        with open("test_split_part1.txt", 'r') as f1:
            self.assertEqual(f1.read(), "Part A: Header\n")
        with open("test_split_part2.txt", 'r') as f2:
            self.assertEqual(f2.read(), "---SPLIT---\nPart B: Body")
        
        os.remove("test_split.txt")
        os.remove("test_split_part1.txt")
        os.remove("test_split_part2.txt")

    def test_split_file_not_found(self):
        write_file("test_split_fail.txt", "Hello World")
        from paser.tools.file_tools import split_file
        with self.assertRaises(ToolError) as cm:
            split_file("test_split_fail.txt", "NONEXISTENT")
        self.assertEqual(str(cm.exception), 'Search text not found')
        os.remove("test_split_fail.txt")
if __name__ == '__main__':
    unittest.main()