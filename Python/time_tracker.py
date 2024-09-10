from datetime import datetime
import repository
import json
import logging
import presenter

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
    last_punch = REPO.get_last_punch()
    day_entries = REPO.get_entries("day")
    week_entries = REPO.get_entries("week")
    punch_in_time = datetime.strptime(last_punch[1])
    last_entry = REPO.get_last_entry()

    if last_punch[1] == "in":
        delta_time = datetime.now() - punch_in_time
        output = f'Punched in for: {round(delta_time.total_hours(), 2)} hours\n '
        output += presenter.format_punch(last_punch)
    elif last_punch[1] == "out":
        output = presenter.format_entry(last_entry)

    total_week_hours = 0
    for entry in week_entries:
        total_week_hours += float(entry[3])

    output += f'Week: {total_week_hours} hours'

    total_day_hours = 0
    for enty in day_entries:
        total_day_hours += float(entry[3])

    output += f'Day: {total_day_hours} hours'

    return output


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
