import unittest
import os

from click.testing import CliRunner

import timeflow


class TestLogging(unittest.TestCase):
    def tearDown(self):
        os.remove(self.test_file)

    def test_log(self):
        test_dir_path = os.path.dirname(os.path.abspath(__file__))
        self.test_file = os.path.join(test_dir_path, 'timeflow_test')
        timeflow.LOG_FILE = self.test_file

        message = 'Arrived.'
        time = timeflow.get_time_now()

        runner = CliRunner()
        result = runner.invoke(timeflow.log, [message])
        assert result.exit_code == 0

        log = time + ': ' + message + '\n'
        assert result.output == log


if __name__ == "__main__":
    unittest.main()
