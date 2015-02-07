import datetime
import os

import click


class LogFile(object):
    def __init__(self, path=os.path.expanduser('~') + "/.timeflow"):
        self.path = path

    def open(self):
        return open(self.path, 'a')

    def read(self):
        return open(self.path, 'r')

    def is_another_day(self, date):
        """
        Checks if new message is written in the next day,
        than the last log entry.

        date - message date
        """
        try:
            f = open(self.path, 'rb')
            last_line = f.readlines()[-1]
        except (IOError, IndexError):
            return False

        last_log_date = last_line[:10]

        # if message date is other day than last log entry
        if date[:10] != last_log_date:
            return True
        else:
            return False


def get_time_now():
    time = datetime.datetime.now()
    return time.strftime("%Y-%m-%d %H:%M")


@click.command()
@click.option('--message', '-m',
              prompt="Your log message",
              help="Your work that you've been doing until now")
def message(message):
    """Simple program for registering jobs at points of time"""
    log_file = LogFile()
    file = log_file.open()

    time = get_time_now()
    string = ': '.join((time, message))

    is_another_day = log_file.is_another_day(time)

    # make empty line between different dates in log.
    if is_another_day:
        file.write('\n' + string + '\n')
    else:
        file.write(string + '\n')

    click.echo(message=string)


if __name__ == "__main__":
    message()
