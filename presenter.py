import time_sheet

from datetime import datetime
from punch_clock import Entry, Punch
from config import TRACKER, Res, DATE_FORMAT, MESSAGES
from rich.console import Console
from rich.table import Table
from rich import box


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
    entries: list[Entry] = time_sheet.get_entries(duration)
    total: float = 0.0

    if not entries:
        print(MESSAGES[Res.NO_PUNCH])
    else:
       table = Table(box=box.MINIMAL_DOUBLE_HEAD)

       table.add_column('In Punch', justify='left', highlight=True)
       table.add_column('Out Punch', justify='left', highlight=True)
       table.add_column('Week Day', justify='left', style='blue')
       table.add_column('Total', justify='right', style='green')
       table.add_column('Title', justify='left', max_width=25, no_wrap=True, style='magenta')
       table.add_column('Comment', justify='left')

       for e in entries:
           temp = datetime.strptime(f'{e.in_punch}', DATE_FORMAT)
           formatted = temp.strftime('%A')

           temp = datetime.strptime(f'{e.in_punch}', DATE_FORMAT)
           in_formatted = temp.strftime(DATE_TIME_FORMAT_2)

           temp = datetime.strptime(f'{e.out_punch}', DATE_FORMAT)
           out_formatted = temp.strftime(DATE_TIME_FORMAT_2)

           total += e.total_time
           table.add_row(in_formatted, out_formatted, formatted, str(e.total_time), e.title, e.comment)


       cons = Console()
       cons.print(table)
       print('Total: ', round(total, 2), 'hours')

def show_last_punch()-> str: return show_punch(time_sheet.get_last_punch())

def show_last_entry()-> str: return show_entry(time_sheet.get_last_entry())

def report() -> None:
    entries = time_sheet.get_entries("week")
    if not entries:
        print(MESSAGES[Res.NO_PUNCH])
    else:
        week_hours: list[float] = [0.0] * 7
        total_hours = 0

        table = Table(box=box.MINIMAL_DOUBLE_HEAD)

        table.add_column('Day', justify='left', style='blue')
        table.add_column('Hours', justify='right', style='green')

        for entry in entries:
            punch: datetime = datetime.strptime(entry.in_punch, DATE_FORMAT)

            week_hours[punch.weekday()] += float(entry.total_time)
            total_hours += float(entry.total_time)

        table.add_row('Monday',    f'{int(week_hours[0])}:{int(round((week_hours[0] - int(week_hours[0])) * 60, 0)):02d}')
        table.add_row('Tuesday',   f'{int(week_hours[1])}:{int(round((week_hours[1] - int(week_hours[1])) * 60, 0)):02d}')
        table.add_row('Wednesday', f'{int(week_hours[2])}:{int(round((week_hours[2] - int(week_hours[2])) * 60, 0)):02d}')
        table.add_row('Thursday',  f'{int(week_hours[3])}:{int(round((week_hours[3] - int(week_hours[3])) * 60, 0)):02d}')
        table.add_row('Friday',    f'{int(week_hours[4])}:{int(round((week_hours[4] - int(week_hours[4])) * 60, 0)):02d}')
        table.add_row('Saturday',  f'{int(week_hours[5])}:{int(round((week_hours[5] - int(week_hours[5])) * 60, 0)):02d}')
        table.add_row('Sunday',    f'{int(week_hours[6])}:{int(round((week_hours[6] - int(week_hours[6])) * 60, 0)):02d}')


        cons = Console()
        cons.print(table)
        print(f'Total: {total_hours} hours {_over_under(total_hours)}')

def _over_under(hours: float) -> float:
    day_of_week: int = (datetime.today().weekday() + 1)

    if day_of_week <= TRACKER["MAX_WORK_WEEK_DAYS"]:
        projected_hours = day_of_week * TRACKER["HOURS_PER_DAY"]
    else:
        projected_hours = TRACKER["MAX_WORK_WEEK_HOURS"]

    return round(hours - projected_hours, 2)

