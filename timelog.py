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


@click.command()
@click.option('--message',
              prompt="Your log message",
              help="Your work that you've been doing until now")
def hello(message):
    """Simple program for registering jobs at points of time"""
    log_file = LogFile()
    file_path = os.path.expanduser('~') + "/.timelog/timelog"
    log_file.path = file_path
    file = log_file.open(create=True)

    time = datetime.datetime.now()
    time = time.strftime("%Y-%m-%d %H:%M")
    string = ': '.join((time, message))

    log_file.write(file, (string + '\n'))
    click.echo(message=string)


if __name__ == "__main__":
    hello()
