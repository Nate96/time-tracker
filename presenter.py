from datetime import datetime

import time_sheet
import punch_clock

from config import PunchType, Res, DATE_FORMAT, MESSAGES


DATE_TIME_FORMAT   = "%Y-%m-%d %I:%M %p"
DATE_TIME_FORMAT_2 = "%Y-%m-%d %I:%M %p"
TIME_FORMAT        = "%I:%M %p"

REPORT  = "==== Report ===="
DIVIDER = "================"


def show_punch(punch: punch_clock.Punch):
    """
    comment, date
    """
    temp = datetime.strptime(f'{punch.time_stamp}', DATE_FORMAT)
    formatted = temp.strftime(DATE_TIME_FORMAT)

    print(f"{punch.comment}, {formatted}")


def show_entry(entry: punch_clock.Entry):
    """
    {total}  (in out)
    title
    comment
    """
    temp = datetime.strptime(f'{entry.in_punch}', DATE_FORMAT)
    in_formatted = temp.strftime(DATE_TIME_FORMAT)

    temp = datetime.strptime(f'{entry.out_punch}', DATE_FORMAT)
    out_formatted = temp.strftime(TIME_FORMAT)

    print(f"{round(entry.total_time, 2)}  {in_formatted} - {out_formatted}")
    print(f"*{entry.title}*")
    print(entry.comment)


def show_entries(duration: str):
    entries: list[punch_clock.Entry] = time_sheet.get_entries(duration)
    total: float = 0.0

    if not entries:
        print(MESSAGES[Res.NO_PUNCH])
    else:

       headers = ["In punch", "Out Punch", "Day", "Total", "Title", "Comment"]

       title_len = max(len(str(e.title)) for e in entries)

       print(f'{headers[0]:<20} {headers[1]:<10} {headers[2]:<10} {headers[3]:<6} {headers[4]:<{title_len}} {headers[5]:<30}')
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

           print(f'{in_formatted:<20} {out_formatted:<10} {day:<10} {e.total_time:<6} {e.title:<{title_len}}: {e.comment:<30}')
           total += e.total_time
    
       print(f'\nTotal: {_convert_float_to_time(total)}')


def show_last_punch(): show_punch(time_sheet.get_last_punch())


def show_last_entry(): show_entry(time_sheet.get_last_entry())


def report(duration: str) -> None:
    # Just doing weeks for now
    if not duration: duration = "week"

    entries = time_sheet.get_entries(duration)
    
    if not entries:
        print(MESSAGES[Res.NO_PUNCH])
    else:
        week_hours: list[float] = [0.0] * 7
        total_hours = 0

        for entry in entries:
            punch: datetime = datetime.strptime(entry.in_punch, DATE_FORMAT)

            week_hours[punch.weekday()] += float(entry.total_time)
            total_hours += float(entry.total_time)

        print(f"\n{REPORT}")
        print(f'Sunday:    {_convert_float_to_time(week_hours[6])}')
        show_day_breakdown([e for e in entries if datetime.strptime(e.in_punch, DATE_FORMAT).weekday() == 6])

        print(f'Monday:    {_convert_float_to_time(week_hours[0])}')
        show_day_breakdown([e for e in entries if datetime.strptime(e.in_punch, DATE_FORMAT).weekday() == 0])

        print(f'Tuesday:   {_convert_float_to_time(week_hours[1])}')
        show_day_breakdown([e for e in entries if datetime.strptime(e.in_punch, DATE_FORMAT).weekday() == 1])

        print(f'Wednesday: {_convert_float_to_time(week_hours[2])}')
        show_day_breakdown([e for e in entries if datetime.strptime(e.in_punch, DATE_FORMAT).weekday() == 2])

        print(f'Thursday:  {_convert_float_to_time(week_hours[3])}')
        show_day_breakdown([e for e in entries if datetime.strptime(e.in_punch, DATE_FORMAT).weekday() == 3])

        print(f'Friday:    {_convert_float_to_time(week_hours[4])}')
        show_day_breakdown([e for e in entries if datetime.strptime(e.in_punch, DATE_FORMAT).weekday() == 4])

        print(f'Saturday:  {_convert_float_to_time(week_hours[5])}')
        show_day_breakdown([e for e in entries if datetime.strptime(e.in_punch, DATE_FORMAT).weekday() == 5])
        print(DIVIDER)
        print(f'Total:     {_convert_float_to_time(total_hours)}')
        print(f'{show_total_breakdown(entries)}')


def show_total_breakdown(entries: list[punch_clock.Entry]) -> str:
    output = ""
    task_dict: dict[str, float] = {}

    for ent in entries:
        task_dict[ent.title] = task_dict.get(ent.title, 0.0) + ent.total_time

    for name, amount in task_dict.items():
        output += f"* {name:<8} {_convert_float_to_time(amount)}\n"

    return output


def show_state():
    state = punch_clock.State()
    session_total: float = 0.0

    if state.last_punch.id != -1:
        print("**STATE**:", state.last_punch.type.value)

        if  state.last_punch.type == PunchType.IN:
            session_total: float = state.get_punched_in_for()

            show_punch(state.last_punch)
            print('')
            print(f'Session: {_convert_float_to_time(session_total)}')
        else:
            show_entry(state.last_entry)
            print('')

        print(f'Day:     {_convert_float_to_time(session_total + state.get_day_total())}')
        print(f'Week:    {_convert_float_to_time(session_total + state.get_week_total())}')
    else:
        print(Res.NO_DB.value)


def show_day_breakdown(entries: list[punch_clock.Entry]) -> None:
    if entries:
        tasks = {}
        for entry in entries:
            tasks[entry.title] = tasks.get(entry.title, 0.0) + entry.total_time

        output = ""
        for name, amount in tasks.items():
            output += f"* {name:<8} {_convert_float_to_time(amount)}\n"

        print(output)  # Remove last newline

def _convert_float_to_time(hours: float) -> str:
    h = int(abs(hours))
    m = int(round((abs(hours) - h) * 60, 0))

    return f"{h:02d}:{m:02d}"
