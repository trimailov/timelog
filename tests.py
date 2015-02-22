import unittest
import os

from click.testing import CliRunner

import timeflow


class TestCommands(unittest.TestCase):
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


class TestTimeflowHelpers(unittest.TestCase):
    def test_find_date_lines(self):
        lines = ['2015-01-01 12:00', '2015-01-01 14:00',
                 '2015-01-02 12:00', '2015-01-02 13:00', '2015-01-02 15:00']
        date_to_find = '2015-01-02'

        line = timeflow.find_date_line(lines, date_to_find, reverse=False)
        self.assertEqual(line, 2)

        line = timeflow.find_date_line(lines, date_to_find, reverse=True)
        self.assertEqual(line, 4)

    def test_date_begins(self):
        lines = ['2015-01-01 12:00', '2015-01-01 14:00',
                 '2015-01-02 12:00', '2015-01-02 13:00', '2015-01-02 15:00']
        date_to_find = '2015-01-01'

        line = timeflow.date_begins(lines, date_to_find)
        self.assertEqual(line, 0)

    def test_date_ends(self):
        lines = ['2015-01-01 12:00', '2015-01-01 14:00',
                 '2015-01-02 12:00', '2015-01-02 13:00', '2015-01-02 15:00']
        date_to_find = '2015-01-02'

        line = timeflow.date_ends(lines, date_to_find)
        self.assertEqual(line, 4)


if __name__ == "__main__":
    unittest.main()
