import datetime
import repository
import json
import logging

REPO = repository
MESSAGES = json.load(open("../Messages/Errors.json"))
logger = logging.getLogger(__name__)


def punch_in(comment):
    """punch in
    punches the user in

    Parameters:
    comment: comment linked to the punch

    Returns:
    str: a messages of the results of the process
    """
    last_punch = REPO.get_last_punch()

    if last_punch is None:
        return MESSAGES['NO_PUNCHES']
    elif last_punch[1] == "in":
        return MESSAGES['PUNCHIN_INVALID']
    elif last_punch[1] == "out":
        REPO.add_punch("in", comment)
        return MESSAGES['PUNCHIN_SUCCESS']
    else:
        return MESSAGES['REFER_LOG']


def punch_out(comment):
    """punch out
    punches the user out

    Parameters:
    comment: comment linked to the punch

    Returns:
    Response of the process
    """
    last_punch = REPO.get_last_punch()

    if last_punch is None:
        return MESSAGES['NO_PUNCHES']
    elif last_punch[1] == "out":
        return MESSAGES['PUNCHOUT_INVALID']
    elif last_punch[1] == "in":
        REPO.add_punch("out", comment)
        REPO.add_entry()
        return MESSAGES['ENTRY_SUCCESS']
    else:
        return MESSAGES['ENTRY_FAIL']


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
