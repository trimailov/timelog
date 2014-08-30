import click
import datetime
import os


class LogFile(object):
    def __init__(self, path=None):
        self.path = path

    def open(self, create=False):
        try:
            return open(self.path, 'a')
        except IOError:
            if create:
                return open(self.path, 'w+')

    def write(self, file, message):
        try:
            file.write(message)
        except IOError:
            file = self.open(create=True)
            file.write(message)

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


@click.command()
@click.option('--message',
              prompt="Your log message",
              help="Your work that you've been doing until now")
def message(message):
    """Simple program for registering jobs at points of time"""
    log_file = LogFile()
    file_path = os.path.expanduser('~') + "/.timelog/timelog"
    log_file.path = file_path
    file = log_file.open(create=True)

    time = datetime.datetime.now()
    time = time.strftime("%Y-%m-%d %H:%M")
    string = ': '.join((time, message))

    is_another_day = log_file.is_another_day(time)

    # make empty line between different dates in log.
    if is_another_day:
        log_file.write(file, ('\n' + string + '\n'))
    else:
        log_file.write(file, (string + '\n'))

    click.echo(message=string)


if __name__ == "__main__":
    message()
