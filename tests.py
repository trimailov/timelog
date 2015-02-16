import unittest
import os

from click.testing import CliRunner

import timeflow


class TestLogging(unittest.TestCase):
    def test_log(self):
        message = 'Arrived.'
        time = timeflow.get_time_now()

        runner = CliRunner()
        result = runner.invoke(timeflow.log, [message])
        assert result.exit_code == 0

        log = time + ': ' + message + '\n'
        assert result.output == log


if __name__ == "__main__":
    unittest.main()
