from datetime import datetime
from repository import Entry, Punch
from time_tracker import REPO
from config import DATABASE

import os

DATE_TIME_FORMAT = "%A %Y-%m-%d %I:%M %p"
INPUT_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_FORMAT = "%I:%M %p"

HEADER = "==== Entry ====\n"


def show_punch(punch: Punch) -> str:
    """
    Returns
    string - {datetime}, COMMENT: {comment}
    """
    temp = datetime.strptime(f'{punch.time_stamp}', INPUT_FORMAT)
    formatted = temp.strftime(DATE_TIME_FORMAT)

    return f"{formatted}, COMMENT: {punch.comment}"


def show_entry(entry: Entry) -> str:
    """
    Returns:
    ==== Entry ====
    {in_punch_datetime} - {out_punch_time} {total_time} Hours
    {task_name}
    {task_comment}
    """
    temp = datetime.strptime(f'{entry.in_punch}', INPUT_FORMAT)
    in_formatted = temp.strftime(DATE_TIME_FORMAT)

    temp = datetime.strptime(f'{entry.in_punch}', INPUT_FORMAT)
    out_formatted = temp.strftime(TIME_FORMAT)

    return f"{HEADER}{in_formatted} - {out_formatted}, {round(entry.total_time, 2)} Hours\n{entry.title}\n{entry.comment}"


def show_entries(entries: list[Entry]):
    for entry in entries:
        print(entry.id, entry.in_punch, entry.out_punch, entry.total_time, entry.title, entry.comment)

def show_last_punch()-> str: return show_punch(REPO.get_last_punch())

def show_last_entry()-> str: return show_entry(REPO.get_entries("last")[0])

def print_entries():
    os.system(f'sqlite3 {DATABASE} -cmd \".mode column\" \" SELECT * FROM entry;\"')

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
    entries = REPO.get_entries("week")
    week_hours = [0] * 7
    total_hours = 0

    for entry in entries:
        dt = datetime.fromisoformat(entry[2])
        day_of_week = dt.weekday()
        week_hours[day_of_week] += float(entry[3])
        total_hours += float(entry[3])

    return f'''---------------------
Monday:     {week_hours[0]} hours
Tuesday:    {week_hours[1]} hours
Wednesday:  {week_hours[2]} hours
Thursday:   {week_hours[3]} hours
Friday:     {week_hours[4]} hours
Saturday:   {week_hours[5]} hours
Sunday:     {week_hours[6]} hours
---------------------
Total:      {total_hours} hours {_over_under(total_hours)}
'''

def _over_under(hours):
    """over under
    Calculates the hourse the user is head or behead for the current week

    Paramaters:
    hours: hours worked for the current week

    Return:
    int: positive if the user is ahead and negative when the user is behind
    """
    day_of_week: int = (datetime.today().weekday() + 1)

    if day_of_week <= config.TRACKER["MAX_WORK_WEEK_DAYS"]:
        projected_hours = day_of_week * config.TRACKER["HOURS_PER_DAY"]
    else:
        projected_hours = config.TRACKER["MAX_WORK_WEEK_HOURS"]

    return hours - projected_hours

