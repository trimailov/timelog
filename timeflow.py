from datetime import datetime
from datetime import timedelta
import os
import subprocess

import click


LOG_FILE = os.path.expanduser('~') + "/.timeflow"
DATETIME_FORMAT = "%Y-%m-%d %H:%M"
DATE_FORMAT = "%Y-%m-%d"

# Constants for stripping log entry strings to get date or datetime strings
DATE_LEN = 10
DATETIME_LEN = 16


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


def get_datetime_now():
    time = datetime.now()
    return time.strftime(DATETIME_FORMAT)


def get_date_now():
    time = datetime.now()
    return time.strftime(DATE_FORMAT)


def get_datetime_obj(string):
    return datetime.strptime(string, DATETIME_FORMAT)


def get_date_obj(string):
    return datetime.strptime(string, DATE_FORMAT)


def get_log_entry(message):
    time = get_datetime_now()
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
    file.close()

    # echo back full log entry, without the new line char at the end
    click.echo(message=log_entry[:-1])


@cli.command()
@click.option('--editor', '-e',
              envvar='EDITOR',
              help='Define editor for timeflow log file editing.')
def edit(editor):
    """Edit timeflow log file"""
    if editor:
        subprocess.call([editor, LOG_FILE])
    else:
        try:
            click.echo("EDITOR environment variable is not set.")
            click.echo("Opening ~/.timeflow with default editor.")
            click.echo("Set EDITOR environment variable, to use preffered editor.")
            open = ['open', LOG_FILE]
            xdg_open = ['xdg-open', LOG_FILE]
            subprocess.call(open) or subprocess.call(xdg_open)
        except:
            click.echo("Default editor not found.")
            click.echo("Set your EDITOR environment variable.")
            click.echo("Add to your .bash_profile, .bashrc, .zshrc or other:")
            click.echo("EDITOR = 'vim'")



def find_date_line(lines, date_to_find, reverse=False):
    "Returns line index of lines, with date_to_find"
    len_lines = len(lines) - 1
    if reverse:
        lines = reversed(lines)
    for i, line in enumerate(lines):
        date_obj = get_date_obj(line[:DATE_LEN])
        date_to_find_obj = get_date_obj(date_to_find)

        if reverse and date_obj <= date_to_find_obj:
            return len_lines - i
        elif date_obj >= date_to_find_obj:
            return i


def date_begins(lines, date_to_find):
    "Returns first line out of lines, with date_to_find"
    return find_date_line(lines, date_to_find)


def date_ends(lines, date_to_find):
    "Returns last line out of lines, with date_to_find"
    return find_date_line(lines, date_to_find, reverse=True)


def is_slack(line):
    "Returns if current log line is slack"
    # slack entries end with '**' and can also have linefeed char
    line = line.replace(' ', '').replace('\n', '')
    if line[-2:] == "**":
        return True
    return False


def is_arrived(line):
    "Returns if log line marks beggining of the day"
    line = line.replace(' ', '').replace('\n', '').replace('.', '')
    if line[DATETIME_LEN:].lower() == 'arrived':
        return True
    return False


def get_lines():
    file = open(LOG_FILE, 'r')
    # exclude empty lines from timeflow file
    lines = [line for line in file.readlines() if line != '\n']
    file.close()
    return lines


def get_time(seconds):
    hours = seconds // 3600
    minutes = seconds % 3600 // 60
    return hours, minutes


def calculate_stats(lines, date_from, date_to):
    work_time = []
    slack_time = []

    line_begins = date_begins(lines, date_from)
    line_ends = date_ends(lines, date_to)

    date_not_found = line_ends < line_begins
    if date_not_found:
        return work_time, slack_time

    for i, line in enumerate(lines[line_begins:line_ends+1]):
        # if we got to the last line - stop
        if line_begins+i+1 > line_ends:
            break

        next_line = lines[line_begins+i+1]

        line_time = get_datetime_obj(line[:DATETIME_LEN])
        if is_arrived(next_line):
            timedelta = 0
        else:
            next_line_time = get_datetime_obj(next_line[:DATETIME_LEN])
            timedelta = (next_line_time - line_time).seconds

        if is_slack(next_line):
            slack_time.append(timedelta)
        else:
            work_time.append(timedelta)

    return work_time, slack_time


def print_stats(work_time, slack_time):
    work_hours, work_minutes = get_time(sum(work_time))
    slack_hours, slack_minutes = get_time(sum(slack_time))

    click.echo('Work: {:02}h {:02}min'.format(work_hours, work_minutes))
    click.echo('Slack: {:02}h {:02}min'.format(slack_hours, slack_minutes))


@cli.command()
@click.option('--today', 'today', is_flag=True)
@click.option('--yesterday', '-y', 'yesterday', is_flag=True)
@click.option('--week', 'week')
@click.option('--last-week', 'last_week', is_flag=True)
@click.option('--month', 'month')
@click.option('--last-month', 'last_month', is_flag=True)
@click.option('--from', '-f', '_from')
@click.option('--to', '-t', 'to')
@click.option('--day', '-d', 'day')
def stats(today, yesterday, week, last_week, month, last_month, _from, to, day):
    "Prints work time statistics"
    date_from = date_to = None
    args = [today, yesterday, week, last_week, month, last_month, _from, to, day]
    if not any(args):
        # if no options are passed, default to today
        today = True

    if today:
        date_from = date_to = get_date_now()
    elif yesterday:
        yesterday_obj = datetime.now() - timedelta(days=1)
        yesterday = yesterday_obj.strftime(DATE_FORMAT)
        date_from = date_to = yesterday
    elif last_week:
        week_ago = datetime.now() - timedelta(weeks=1)
        last_monday = week_ago - timedelta(days=week_ago.isocalendar()[2]-1)
        last_sunday = week_ago + timedelta(days=5+(week_ago.isocalendar()[2]))

        date_from = last_monday.strftime(DATE_FORMAT)
        date_to = last_sunday.strftime(DATE_FORMAT)
    # if no 'to' date is passed, default 'to' to today
    elif _from and not to:
        date_from = _from
        date_to = get_date_now()
    elif _from and to:
        date_from = _from
        date_to = to
    elif day:
        date_from = date_to = day

    work_time, slack_time = calculate_stats(get_lines(), date_from, date_to)

    print_stats(work_time, slack_time)
