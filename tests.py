from datetime import datetime
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
        time = timeflow.get_datetime_now()

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

    def test_is_slack(self):
        non_slack_entry = '2015-01-01 12:00 Timeflow: testing'
        self.assertFalse(timeflow.is_slack(non_slack_entry))

        non_slack_entry_lf = '2015-01-01 12:00 Timeflow: testing\n'
        self.assertFalse(timeflow.is_slack(non_slack_entry_lf))

        slack_entry = '2015-01-01 12:00 Slack: testing**'
        self.assertTrue(timeflow.is_slack(slack_entry))

        slack_entry2 = '2015-01-01 12:00 Slack: testing**   '
        self.assertTrue(timeflow.is_slack(slack_entry2))

        slack_entry3 = '2015-01-01 12:00 Slack: testing  **   '
        self.assertTrue(timeflow.is_slack(slack_entry3))

        slack_entry_lf = '2015-01-01 12:00 Slack: testing**\n'
        self.assertTrue(timeflow.is_slack(slack_entry_lf))

        slack_entry_lf2 = '2015-01-01 12:00 Slack: testing**     \n'
        self.assertTrue(timeflow.is_slack(slack_entry_lf2))

        slack_entry_lf3 = '2015-01-01 12:00 Slack: testing   **     \n'
        self.assertTrue(timeflow.is_slack(slack_entry_lf3))

    def test_get_datetime_obj(self):
        date_time_obj = timeflow.get_datetime_obj('2015-03-15 15:14')
        self.assertEqual(date_time_obj, datetime(2015, 3, 15, 15, 14))

    def test_get_date_obj(self):
        date_obj = timeflow.get_date_obj('2015-03-15')
        self.assertEqual(date_obj, datetime(2015, 3, 15))

    def test_is_arrived(self):
        line = '2015-03-14 15:28: Arrived.'
        self.assertTrue(timeflow.is_arrived(line))

        line = '2015-03-14 15:28: Arrived'
        self.assertTrue(timeflow.is_arrived(line))

        line = '2015-03-14 15:28: Arrived\n'
        self.assertTrue(timeflow.is_arrived(line))

        line = '2015-03-14 15:28: Arrived.\n'
        self.assertTrue(timeflow.is_arrived(line))

        line = '2015-03-14 15:28: Timeflow: some task.\n'
        self.assertFalse(timeflow.is_arrived(line))

    def test_get_time(self):
        self.assertEqual(timeflow.get_time(35), (0, 0))
        self.assertEqual(timeflow.get_time(65), (0, 1))
        self.assertEqual(timeflow.get_time(1860), (0, 31))
        self.assertEqual(timeflow.get_time(3600), (1, 0))
        self.assertEqual(timeflow.get_time(3720), (1, 2))

    def test_calculate_stats_day(self):
        lines = [
            '2015-03-14 15:00: Arrived.\n',
            '2015-03-14 15:28: Timeflow: testing\n',
            '2015-03-14 15:40: Slack: chat**\n',
        ]
        wt, st = timeflow.calculate_stats(lines, '2015-03-14', '2015-03-14')
        self.assertEqual((wt, st), ([1680], [720]))

        wt, st = timeflow.calculate_stats(lines, '2015-03-13', '2015-03-13')
        self.assertEqual((wt, st), ([], []))

    def test_calculate_stats_range(self):
        lines = [
            '2015-03-12 15:00: Arrived.\n',
            '2015-03-12 15:28: Timeflow: testing\n',
            '2015-03-12 15:40: Slack: chat**\n',
            '2015-03-14 15:00: Arrived.\n',
            '2015-03-14 15:28: Timeflow: testing\n',
            '2015-03-14 15:40: Slack: chat**\n',
        ]
        wt, st = timeflow.calculate_stats(lines, '2015-03-12', '2015-03-14')
        self.assertEqual((wt, st), ([1680, 1680], [720, 720]))

        wt, st = timeflow.calculate_stats(lines, '2015-03-13', '2015-03-13')
        self.assertEqual((wt, st), ([], []))


if __name__ == "__main__":
    unittest.main()
