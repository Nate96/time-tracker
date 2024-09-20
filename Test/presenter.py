from datetime import datetime
TOP = "---Entry---\n"
BOTTOM = "\n---End---\n\n"
DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
TIME_FORMAT = "hh:mm tt"


def format_punch(punch):
    """ format punch
    converts a tuple of a punch into a string format

    Parameters:
    punch(id, tye, punch_datetime, comment)

    Returns:
    string - {datetime}, {type} COMMENT: {comment}
    """
    return f"{datetime.strptime(punch[2], DATE_TIME_FORMAT)}, "
    + f"{punch[1]} COMMENT: {punch[3]}"


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
    return f"{TOP}{datetime.strptime(entry[1], DATE_TIME_FORMAT)} -"
    + f" {datetime.strptime(entry[2], TIME_FORMAT)}"
    + f" {round(entry[3], 2)} Hours\n{entry[4]}{entry[5]}{BOTTOM}"


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
        output += f"{TOP}{datetime.strptime(entry[1], DATE_TIME_FORMAT)} -"
        + f"{datetime.strptime(entry[2], TIME_FORMAT)} {round(entry[3], 2)} Hours\n"
        + f"{entry[4]} {entry[5]}{BOTTOM}"

    return output
