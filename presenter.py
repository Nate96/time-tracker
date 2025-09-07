import time_sheet

from datetime import datetime
from punch_clock import Entry, Punch
from config import TRACKER, Res, DATE_FORMAT, MESSAGES


DATE_TIME_FORMAT = "%A %Y-%m-%d %I:%M %p"
DATE_TIME_FORMAT_2 = "%Y-%m-%d %I:%M %p"
TIME_FORMAT = "%I:%M %p"

HEADER = "==== Entry ====\n"


def show_punch(punch: Punch) -> str:
    """
    Returns
    string - {datetime}, COMMENT: {comment}
    """
    temp = datetime.strptime(f'{punch.time_stamp}', DATE_FORMAT)
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
    temp = datetime.strptime(f'{entry.in_punch}', DATE_FORMAT)
    in_formatted = temp.strftime(DATE_TIME_FORMAT)

    temp = datetime.strptime(f'{entry.in_punch}', DATE_FORMAT)
    out_formatted = temp.strftime(TIME_FORMAT)

    return f"{HEADER}{in_formatted} - {out_formatted}, {round(entry.total_time, 2)} Hours\n{entry.title}\n{entry.comment}"


def show_entries(duration: str) -> None:
    from rich.console import Console
    from rich.table import Table
    from rich import box

    entries: list[Entry] = time_sheet.get_entries(duration)

    if not entries:
        print(MESSAGES[Res.NO_PUNCH])
    else:
       table = Table(box=box.MINIMAL_DOUBLE_HEAD)

       table.add_column('in punch', justify='left', highlight=True)
       table.add_column('out punch', justify='left', highlight=True)
       table.add_column('week day', justify='left', style='blue')
       table.add_column('total', justify='right', style='green')
       table.add_column('title', justify='left', style='magenta')
       table.add_column('comment', justify='left')

       for e in entries:
           temp = datetime.strptime(f'{e.in_punch}', DATE_FORMAT)
           formatted = temp.strftime('%A')

           temp = datetime.strptime(f'{e.in_punch}', DATE_FORMAT)
           in_formatted = temp.strftime(DATE_TIME_FORMAT_2)

           temp = datetime.strptime(f'{e.out_punch}', DATE_FORMAT)
           out_formatted = temp.strftime(DATE_TIME_FORMAT_2)

           table.add_row(in_formatted, out_formatted, formatted, str(e.total_time), e.title, e.comment)

       cons = Console()
       cons.print(table)

def show_last_punch()-> str: return show_punch(time_sheet.get_last_punch())

def show_last_entry()-> str: return show_entry(time_sheet.get_last_entry())

def report():
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
    entries = time_sheet.get_entries("week")
    if not entries:
        print(MESSAGES[Res.NO_PUNCH])
    else:
        week_hours = [0.0] * 7
        total_hours = 0


        for entry in entries:
            punch: datetime = datetime.strptime(entry.in_punch, DATE_FORMAT )

            week_hours[punch.weekday()] += float(entry.total_time)
            total_hours += float(entry.total_time)

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

    if day_of_week <= TRACKER["MAX_WORK_WEEK_DAYS"]:
        projected_hours = day_of_week * TRACKER["HOURS_PER_DAY"]
    else:
        projected_hours = TRACKER["MAX_WORK_WEEK_HOURS"]

    return hours - projected_hours

