from datetime import datetime
TOP = "---Entry---\n"
BOTTOM = "\n---End---\n\n"
DATE_TIME_FORMAT = "dddd dd-MM-yyyy hh:mm tt"
TIME_FORMAT = "hh:mm tt"


def format_punch(punch):
    print(f"{datetime.strptime(punch[2], DATE_TIME_FORMAT)}, COMMENT: {punch[3]}")


def format_entry(entry):
    return f"{TOP}{datetime.strptime(entry[1], DATE_TIME_FORMAT)} -"
    + f" {datetime.strptime(entry[2], TIME_FORMAT)}"
    + f" {round(entry[3], 2)} Hours\n{entry[4]}{entry[5]}{BOTTOM}"


def format_entries(entries):
    output = ''
    for entry in entries:
        output += f"{TOP}{datetime.strptime(entry[1], DATE_TIME_FORMAT)} -"
        + f"{datetime.strptime(entry[2], TIME_FORMAT)} {round(entry[3], 2)} Hours\n"
        + f"{entry[4]} {entry[5]}{BOTTOM}"

    return output
