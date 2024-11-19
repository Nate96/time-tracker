from datetime import datetime
import repository
import json
import presenter

REPO = repository
MESSAGES = json.load(open("../Dialogue/Errors.json"))


def punch_in(comment):
    """punch in
    punches the user in

    Parameters:
    comment: comment linked to the punch

    Returns:
    str: a messages of the results of the process
    """
    last_punch = REPO.get_last_punch()

    if last_punch is None or last_punch[1] == "out":
        return presenter.format_punch(REPO.add_punch("in", comment))
    elif last_punch[1] == "in":
        return MESSAGES['PUNCHIN_INVALID']
    else:
        return MESSAGES['REFER_LOG']


def punch_out(comment):
    """punch out
    punches the user out

    Parameters:
    comment: comment linked to the punch

    Returns:
    The most recent punch
    """
    last_punch = REPO.get_last_punch()

    if last_punch is None:
        return MESSAGES['NO_PUNCHES']
    elif last_punch[1] == "out":
        return MESSAGES['PUNCHOUT_INVALID']
    elif last_punch[1] == "in":
        REPO.add_punch("out", comment)
        output = MESSAGES['PUNCHIN_SUCCESS'] + '\n'
        output += presenter.format_entry(REPO.add_entry())
        return output
    else:
        return MESSAGES['ENTRY_FAIL']


def status():
    '''
    Presents the current status of the given databse in the following format

    Status of Database

    Day:  {} hours
    Week: {} hours "-/+"{}
    '''
    last_punch = REPO.get_last_punch()
    week_hours = _get_week_total()

    if last_punch is None:
        return MESSAGES['NO_PUNCHES']

    if last_punch[1] == "in":
        last_punch_time = datetime.fromisoformat(last_punch[2])
        delta_time = datetime.now() - last_punch_time
        delta_time = delta_time.total_seconds() / 3600
        return f'''---------------------
Punched in for: {round(delta_time, 2)} hours
{presenter.format_punch(last_punch)}

Day:  {_get_day_total()} Hours
Week: {week_hours} Hours {_over_under(week_hours)}
'''
    elif last_punch[1] == "out":
        return f'''---------------------
currenlty clocked out

Day:  {_get_day_total()} Hours
Week: {week_hours} Hours {_over_under(week_hours)}
'''


def show_entrie(duration):
    '''Show Entires:
    Show Entries for the given Duration in the following format
    Entry{}

    Total Hours: {}
    '''
    return presenter.format_entries(REPO.get_entries(duration))


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
    if duration == "":
        entries = REPO.get_entries("week")
        presenter.week(entries)
    elif duration == "last":
        entries = REPO.get_entries("lastWeek")
        presenter.week(entries)
    else:
        entries = REPO.get_entries_with_task(duration)
        presenter.format_entries(entries)


def calculate_week(entries):
    day_hours = [0] * 7
    total_hours = 0

    for entry in entries:
        dt = datetime.fromisoformat(entry[2])
        day_of_week = dt.weekday()

        day_hours[day_of_week] += float(entry[3])
        total_hours += float(entry[3])

    return day_hours, total_hours


def _get_day_total():
    day_entries = REPO.get_entries("day")

    total_day_hours = 0
    for entry in day_entries:
        total_day_hours += float(entry[3])

    return round(total_day_hours, 2)


def _get_week_total():
    week_entries = REPO.get_entries("week")

    total_week_hours = 0
    for entry in week_entries:
        total_week_hours += float(entry[3])

    return round(total_week_hours, 2)


def _over_under(hours):
    """over under
    Calculates the hourse the user is head or behead for the current week

    Paramaters:
    hours: hours worked for the current week

    Return:
    int: positive if the user is ahead and negative when the user is behind
    """
    MAX_WORK_WEEK_HOURS = 40
    MAX_WORK_WEEK_DAYS = 5
    HOURS_PER_DAY = 8
    day_of_week = datetime.today().weekday()

    if day_of_week <= MAX_WORK_WEEK_DAYS:
        projected_hours = day_of_week * HOURS_PER_DAY
    else:
        projected_hours = MAX_WORK_WEEK_HOURS

    return hours - projected_hours
