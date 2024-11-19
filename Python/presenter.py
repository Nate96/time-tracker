from datetime import datetime

TOP = "---Entry---\n"
BOTTOM = "\n---End---\n\n"
DATE_TIME_FORMAT = "%A %Y-%m-%d %I:%M %p"
input_format = "%Y-%m-%d %H:%M:%S"
TIME_FORMAT = "%I:%M %p"


def format_punch(punch):
    """ format punch
    converts a tuple of a punch into a string format

    Parameters:
    punch(id, tye, punch_datetime, comment)

    Returns:
    string - {datetime}, {type} COMMENT: {comment}
    """
    in_time = datetime.strptime(punch[2], input_format)
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
    in_time = datetime.strptime(entry[1], input_format)
    format_in_time = in_time.strftime(DATE_TIME_FORMAT)

    out_time = datetime.strptime(entry[2], input_format)
    format_out_time = out_time.strftime(TIME_FORMAT)

    return f"{TOP}{format_in_time} - {format_out_time}, {round(entry[3], 2)} Hours\n{entry[4]}\n{entry[5]}{BOTTOM}"


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
        in_time = datetime.strptime(entry[1], input_format)
        format_in_time = in_time.strftime(DATE_TIME_FORMAT)

        out_time = datetime.strptime(entry[2], input_format)
        format_out_time = out_time.strftime(TIME_FORMAT)

        output += f"{TOP}{format_in_time} - {format_out_time} {round(entry[3], 2)} Hours\n{entry[4]}\n{entry[5]}{BOTTOM}"

    return output


def format_week(week_hours, total_hours, overUnder):
    return f'''---------------------
Monday:     {week_hours[1]} hours
Tuesday:    {week_hours[1]} hours
Wednesday:  {week_hours[2]} hours
Thursday:   {week_hours[3]} hours
Friday:     {week_hours[4]} hours
Saturday:   {week_hours[5]} hours
Sunday:     {week_hours[6]} hours
---------------------
Total:      {total_hours} hours {overUnder}
'''
