import unittest
import os

from timeflow import LogFile


class TestLogFile(unittest.TestCase):
    def setUp(self):
        file_name = 'timeflow_test'
        self.test_dir_path = os.path.dirname(os.path.abspath(__file__))
        self.test_file_path = os.path.join(self.test_dir_path, file_name)

    def tearDown(self):
        # remove test file
        os.remove(self.test_file_path)

    def test_file_creates(self):
        log_file = LogFile(path=self.test_file_path)

        # check if test file does not exist before first time opening
        self.assertFalse(os.path.exists(self.test_file_path))
        log_file.open()
        # check if test file is created
        self.assertTrue(os.path.exists(self.test_file_path))

    def test_file_writes(self):
        log_file = LogFile(path=self.test_file_path)

        # check if test file does not exist before first time opening
        self.assertFalse(os.path.exists(self.test_file_path))
        f = log_file.open()

        text = 'message'
        f.write(text)

        f = log_file.read()
        self.assertEqual(f.read(), text)


if __name__ == "__main__":
    unittest.main()
