from datetime import datetime, timedelta, time
from repository import Repository
import os

# TODO: Turn repository into class
# TODO: Implement "cli" class in tt.py file.
# TODO: test
REPO = Repository


def punch_in(comment):
    def _valid_state():
        last_punch = REPO.get_last_punch()[0]
        if last_punch.punch_type == "out":
            return True
        return False

    if _valid_state():
        REPO.add_punch("in", os.time(), comment)


def punch_out(comment):
    def _valid_state():
        last_punch = REPO.get_last_punch()[0]
        if last_punch.punch_type == "in":
            return True
        return False

    if _valid_state():
        REPO.add_punch("out", os.time(), comment)
        REPO.add_entry()


def status():
    last_punch = REPO.get_last_punch()[0]
    day_entries = REPO.get_entries("day")
    week_entries = REPO.get_entries("week")
    punch_in_time = datetime.time('now') - last_punch.punch_time

    if last_punch.punch_type == "in":
        print(f'Punched in for: {round(punch_in_time, 2)} hours\n')
        print(last_punch)
        print(f'Day:  {day_entries} hours')
        print(f'Week: {week_entries} hours')
    elif last_punch.punch_type == "out":
        print(REPO.get_entries("last"))
        print(f'Day:  {day_entries} hours')
        print(f'Week: {week_entries} hours')


def show_entrie(duration):
    '''Show Entires:
    Show Entries for the given Duration in the following format
    Entry{}

    Total Hours: {}
    '''
    entries = REPO.get_entries(duration)

    # print Entry
    # print toal time


def report(duration):
    '''Report
    Show stats of the given week in the following format
    Monday:     {} hours
    Tuesday:    {} hours
    Wednesday:  {} hours
    Thursday:   {} hours
    Friday:     {} hours
    Saturday:   {} hours
    Sunday:     {} hours
    ---------------------
    Total:      {} hours
    '''


def _display_results(hours):
    print(f'Total hours worked today: {round(hours, 2)}')
    print(f'%50: {round(hours / 2, 2)} \n%25: {round(hours/4, 2)}')


def _normal_mode(in_time, out_time):
    """Normal Mode
    Calculates total time (hours) by using a start time and an end time.
    Then, displays the results.
    """
    start_strip = datetime.strptime(in_time, "%H:%M")
    end_strip = datetime.strptime(out_time, "%H:%M")

    delta = end_strip - start_strip

    sec = delta.total_seconds()
    hours = sec / (60 * 60)
    _display_results(hours)

    return hours


def _friday_mode(in_time, total_time):
    """Friday Mode
    Calculates time to leave and hours need to be worked on Friday.
    Then, Displays the results
    """
    remaining_hours = 40.0 - total_time

    delta_time = datetime.strptime(in_time, "%H:%M") + timedelta(hours=remaining_hours)

    delta_hour = delta_time.time().hour % 12

    print(f'You get to work until: {time(delta_hour, delta_time.time().minute)}')
    _display_results(remaining_hours)

    return delta_hour


@click.command()
@click.option('-m', '--mode',
              type=str,
              default='n',
              required=True,
              help='Mode: n = normal, f = friday, q = querying mode, d = today entry(s)')
@click.option('-i', '--in-time',
              type=str,
              required=False,
              help='In Time: HH:MM')
@click.option('-o', '--out-time',
              type=str,
              required=False,
              help='In Time: HH:MM')
@click.option('-hw', '--hours-worked',
              type=float,
              help='In Time: HH:MM')
@click.option('-c', '--comment',
              type=str,
              required=False,
              help='Comment for entry')
@click.option('-q', '--query',
              type=str,
              required=False,
              help='SQLite query')
def time_tracker(mode, in_time, out_time, hours_worked, comment, query):
    if mode == 'n':
        total_time = _normal_mode(in_time, out_time)
        create_entry(in_time, out_time, comment, total_time)
    elif mode == 'f':
        total_time = _friday_mode(in_time, hours_worked)
        create_entry(in_time, out_time, comment, total_time)
    elif mode == 'q':
        execute_query(query)
    elif mode == 'd':
        get_todays_entries()
    elif mode == 'tt':
        get_hours_worked_today()


if __name__ == '__main__':
    time_tracker()
