from datetime import datetime
import os
import subprocess

import click


LOG_FILE = os.path.expanduser('~') + "/.timeflow"
DATE_FORMAT = "%Y-%m-%d %H:%M"

# Constants for stripping log entry strings to get date or datetime strings
DATE_LEN = 10
DATE_TIME_LEN = 16


def is_another_day(date):
    """
    Checks if new message is written in the next day,
    than the last log entry.

    date - message date
    """
    try:
        f = open(LOG_FILE, 'rb')
        last_line = f.readlines()[-1]
    except (IOError, IndexError):
        return False

    last_log_date = last_line[:DATE_LEN]

    # if message date is other day than last log entry
    if date[:DATE_LEN] != last_log_date:
        return True
    else:
        return False


def get_time_now():
    time = datetime.now()
    return time.strftime(DATE_FORMAT)


def get_log_entry(message):
    time = get_time_now()
    string = ': '.join((time, message))

    another_day = is_another_day(time)

    # make empty line between different dates in log.
    if another_day:
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
    """Simple command for registering jobs"""
    file = open(LOG_FILE, 'a')

    log_entry = get_log_entry(message)
    file.write(log_entry)

    # echo back full log entry, without the new line char at the end
    click.echo(message=log_entry[:-1])


@cli.command()
@click.option('--editor', '-e',
              envvar='EDITOR',
              help='Define editor for timeflow log file editing.')
def edit(editor):
    """Edit timeflow log file"""
    subprocess.call([editor, LOG_FILE])


def find_date_line(lines, date_to_find, reverse=False):
    len_lines = len(lines) - 1
    if reverse:
        lines = reversed(lines)
    for i, line in enumerate(lines):
        date = line[:DATE_LEN]
        if date == date_to_find:
            if reverse:
                return len_lines - i
            else:
                return i


def date_begins(lines, date_to_find):
    "Returns first line out of lines, with date_to_find"
    return find_date_line(lines, date_to_find)


def date_ends(lines, date_to_find):
    "Returns last line out of liens, with date_to_find"
    return find_date_line(lines, date_to_find, reverse=True)
