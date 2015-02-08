import datetime
import os

import click


LOG_FILE = os.path.expanduser('~') + "/.timeflow"


class LogFile(object):
    def __init__(self, path=LOG_FILE):
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

def get_log_entry(log_file, message):
    time = get_time_now()
    string = ': '.join((time, message))

    is_another_day = log_file.is_another_day(time)

    # make empty line between different dates in log.
    if is_another_day:
        log_message = '\n' + string + '\n'
    else:
        log_message = string + '\n'
    return log_message


@click.group()
def cli():
    pass


@cli.command()
@click.argument('message')
def log(message):
    """Simple program for registering jobs at points of time"""
    log_file = LogFile()
    file = log_file.open()

    log_entry = get_log_entry(log_file, message)
    file.write(log_entry)

    # echo back full log entry, without the new line char at the end
    click.echo(message=log_entry[:-1])


if __name__ == "__main__":
    message()
