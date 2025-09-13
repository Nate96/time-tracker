import time_sheet

from datetime import datetime
from punch_clock import Entry, Punch
from config import TRACKER, Res, DATE_FORMAT, MESSAGES

DATE_TIME_FORMAT   = "%Y-%m-%d %I:%M %p"
DATE_TIME_FORMAT_2 = "%Y-%m-%d %I:%M %p"
TIME_FORMAT        = "%I:%M %p"

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

       headers = ["In punch", "Out Punch", "Day", "Total", "Title", "Comment"]

       print(f'{headers[0]:<20} {headers[1]:<10} {headers[2]:<10} {headers[3]:<6} {headers[4]:<30} {headers[5]:<30}')
       print('-' * 90)

       for e in entries:
           temp = datetime.strptime(f'{e.in_punch}', DATE_FORMAT)
           in_formatted = temp.strftime(DATE_TIME_FORMAT)

           temp = datetime.strptime(f'{e.out_punch}', DATE_FORMAT)
           out_formatted = temp.strftime(TIME_FORMAT)

           temp = datetime.strptime(f'{e.in_punch}', DATE_FORMAT)
           day = temp.strftime("%A")

           e.title = e.title.replace("\n", "")
           e.comment = e.comment.replace("\n", "")

           print(f'{in_formatted:<20} {out_formatted:<10} {day:<10} {e.total_time:<6} {e.title:<30} : {e.comment:<30}')
           total =+ e.total_time
    
       print('Total: ', round(total, 2), 'hours')

def show_last_punch( )-> str: return show_punch(time_sheet.get_last_punch())

def show_last_entry() -> str: return show_entry(time_sheet.get_last_entry())

def report() -> None:
    entries = time_sheet.get_entries("week")

    if not entries:
        print(MESSAGES[Res.NO_PUNCH])
    else:
        week_hours: list[float] = [0.0] * 7
        total_hours = 0

        for entry in entries:
            punch: datetime = datetime.strptime(entry.in_punch, DATE_FORMAT)

            week_hours[punch.weekday()] += float(entry.total_time)
            total_hours += float(entry.total_time)

        print("\n==== Report =====")
        print(f'Monday:    {int(week_hours[0])}:{int(round((week_hours[0] - int(week_hours[0])) * 60, 0)):02d}')
        print(f'Tuesday:   {int(week_hours[1])}:{int(round((week_hours[1] - int(week_hours[1])) * 60, 0)):02d}')
        print(f'Wednesday: {int(week_hours[2])}:{int(round((week_hours[2] - int(week_hours[2])) * 60, 0)):02d}')
        print(f'Thursday:  {int(week_hours[3])}:{int(round((week_hours[3] - int(week_hours[3])) * 60, 0)):02d}')
        print(f'Friday:    {int(week_hours[4])}:{int(round((week_hours[4] - int(week_hours[4])) * 60, 0)):02d}')
        print(f'Saturday:  {int(week_hours[5])}:{int(round((week_hours[5] - int(week_hours[5])) * 60, 0)):02d}')
        print(f'Sunday:    {int(week_hours[6])}:{int(round((week_hours[6] - int(week_hours[6])) * 60, 0)):02d}\n')

        print(f'Total:     {total_hours} hours {_over_under(total_hours)}')


def _over_under(hours: float) -> float:
    day_of_week: int = (datetime.today().weekday() + 1)

    if day_of_week <= TRACKER["MAX_WORK_WEEK_DAYS"]:
        projected_hours = day_of_week * TRACKER["HOURS_PER_DAY"]
    else:
        projected_hours = TRACKER["MAX_WORK_WEEK_HOURS"]

    return round((hours - projected_hours), 2)

