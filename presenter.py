from datetime import datetime

from repository import Entry, Punch
from time_tracker import REPO

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


def format_entries(entries):
    """format entry
    converts a tuple of a punch into a string

    Parameters:
    List(Entry(id, in_punch_datatime, out_punch_datetime, total_time, task_name, task_comment))

    Returns:
    ---Entry---
    {in_punch_datetime} - {out_punch_time} {total_time} Hours
    {task_name}
    {task_comment}
    --End--
    """
    output = ''
    for entry in entries:
        in_time = datetime.strptime(entry[1], INPUT_FORMAT)
        format_in_time = in_time.strftime(DATE_TIME_FORMAT)

        out_time = datetime.strptime(entry[2], INPUT_FORMAT)
        format_out_time = out_time.strftime(TIME_FORMAT)

        output += f"{format_in_time} - {format_out_time} {round(entry[3], 2)} Hours\n{entry[4]}\n{entry[5]}"

    return output

def show_entries(): REPO.print_entries()

def show_last_punch(): return show_punch(REPO.get_last_punch())

def show_last_entry(): return show_entry(REPO.get_entries("last")[0])
