import os
import unittest
import shutil
from paser.tools.web_tools import download_file

class TestDownloadFile(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_downloads"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
        self.test_file = os.path.join(self.test_dir, "test_image.png")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_successful_download(self):
        url = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
        result = download_file(url, self.test_file)
        self.assertEqual(result, "OK")
        self.assertTrue(os.path.exists(self.test_file))
        self.assertGreater(os.path.getsize(self.test_file), 0)

    def test_invalid_url(self):
        url = "not-a-url"
        result = download_file(url, self.test_file)
        self.assertTrue(result.startswith("ERR:"))

    def test_unsafe_url(self):
        url = "http://127.0.0.1/test.txt"
        result = download_file(url, self.test_file)
        self.assertEqual(result, "ERR: Unsafe or invalid URL: http://127.0.0.1/test.txt")

    def test_create_directory(self):
        nested_dir = os.path.join(self.test_dir, "nested", "dir")
        nested_file = os.path.join(nested_dir, "test.txt")
        url = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
        result = download_file(url, nested_file)
        self.assertEqual(result, "OK")
        self.assertTrue(os.path.exists(nested_file))

    def test_http_error(self):
        # Using a known 404 URL
        url = "https://www.google.com/nonexistent_file_12345.png"
        result = download_file(url, self.test_file)
        self.assertTrue(result.startswith("ERR: HTTP Error 404"))

if __name__ == '__main__':
    unittest.main()
