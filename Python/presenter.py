TOP = "---Entry---\n"
BOTTOM = "\n---End---\n\n"
DATE_TIME_FORMAT = "dddd dd-MM-yyyy hh:mm tt"
TIME_FORMAT = "hh:mm tt"


def present_punch(punch):
    print(f"{punch["DateTime"]}, {punch["type"]}, COMMENT: {punch["comment"]}")


def present_punches(punches):
    for punch in punches:
        print(f"{punch["DateTime"]}, {punch["type"]}, COMMENT: {punch["comment"]}")


def present_entry(entry):
    print(f"{TOP}{entry["inDateTime"]} - {entry["outDateTime"]} {round(entry["totalTime"], 2)} Hours\n{entry["title"]} {entry["comment"]}{BOTTUM}")
