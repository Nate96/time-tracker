from datetime import datetime
import repository
import json
import abacus


TOP = "---Entry---\n"
BOTTOM = "\n---End---\n\n"
DATE_TIME_FORMAT = "%A %Y-%m-%d %I:%M %p"
INPUT_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_FORMAT = "%I:%M %p"

REPO = repository
MESSAGES = json.load(open("../Dialogue/Errors.json"))


def status():
    '''
    Presents the current status of the given databse in the following format

    Status of Database

    Day:  {} hours
    Week: {} hours "-/+"{}
    '''
    last_punch = REPO.get_last_punch()
    week_hours = REPO.get_week_total()

    if last_punch is None:
        return MESSAGES['NO_PUNCHES']

    if last_punch[1] == "in":
        last_punch_time = datetime.fromisoformat(last_punch[2])
        delta_time = datetime.now() - last_punch_time
        delta_time = delta_time.total_seconds() / 3600
        return f'''---------------------
Punched in for: {round(delta_time, 2)} hours
{format_punch(last_punch)}

Day:  {REPO.get_day_total()} Hours
Week: {week_hours} Hours {REPO.over_under(week_hours)}
'''
    elif last_punch[1] == "out":
        return f'''---------------------
currenlty clocked out

Day:  {REPO.get_day_total()} Hours
Week: {week_hours} Hours {abacus.over_under(week_hours)}
'''


def format_punch(punch):
    """ format punch
    converts a tuple of a punch into a string format

    Parameters:
    punch(id, tye, punch_datetime, comment)

    Returns:
    string - {datetime}, {type} COMMENT: {comment}
    """
    in_time = datetime.strptime(punch[2], INPUT_FORMAT)
    format_in_time = in_time.strftime(DATE_TIME_FORMAT)

    return f"{format_in_time}, {punch[1]} COMMENT: {punch[3]}"


def format_entry(entry):
    """format entry
    converts a tuple of a punch into a string

    Parameters:
    Entry(id, in_punch_datatime, out_punch_datetime, total_time, task_name, task_comment)

    Returns:
    ---Entry---
    {in_punch_datetime} - {out_punch_time} {total_time} Hours
    {task_name}
    {task_comment}
    --End--
    """
    in_time = datetime.strptime(entry[1], INPUT_FORMAT)
    format_in_time = in_time.strftime(DATE_TIME_FORMAT)

    out_time = datetime.strptime(entry[2], INPUT_FORMAT)
    format_out_time = out_time.strftime(TIME_FORMAT)

    return f"{TOP}{format_in_time} - {format_out_time}, {round(entry[3], 2)} Hours\n{entry[4]}\n{entry[5]}{BOTTOM}"


def show_entrie(duration):
    '''Show Entires:
    Show Entries for the given Duration in the following format
    Entry{}

    Total Hours: {}
    '''
    return format_entries(REPO.get_entries(duration))


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
Monday:     {week_hours[1]} hours
Tuesday:    {week_hours[1]} hours
Wednesday:  {week_hours[2]} hours
Thursday:   {week_hours[3]} hours
Friday:     {week_hours[4]} hours
Saturday:   {week_hours[5]} hours
Sunday:     {week_hours[6]} hours
---------------------
Total:      {total_hours} hours {abacus.over_under(total_hours)}
'''


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

        output += f"{TOP}{format_in_time} - {format_out_time} {round(entry[3], 2)} Hours\n{entry[4]}\n{entry[5]}{BOTTOM}"

    return output
