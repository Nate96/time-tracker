from datetime import datetime, timedelta

NORMAL_MODE = 1
FRIDAY_MODE = 2

def _display_results(hours):
    print("Total hours worked today: {}".format(round(hours, 2)))
    print("%50: {} \n%25: {}".format(round(hours / 2, 2), round(hours/4, 2)))


def _normal_mode():
    """Normal Mode
    Calculates total time (hours) by using a start time and an end time. 
    Then, displays the results.
    """
    start_time = str(input('Enter in Start time: ') + ":00")
    end_time = str(input('Enter in End time: ') + ":00")

    start_strip = datetime.strptime(start_time, "%H:%M:%S")
    end_strip = datetime.strptime(end_time, "%H:%M:%S")

    delta = end_strip - start_strip

    sec = delta.total_seconds()
    hours = sec / (60 * 60)
    
    _display_results(hours)   


def _friday_mode():
    """Friday Mode
    Calculates time to leave and hours need to be worked on Friday. 
    Then, Displays the results
    """
    total_time = float(input("Enter in total time worked for the week: "))
    start_time = str(input("Enter in time started: ") + ":00")

    remaining_hours = 40.0 - total_time

    time_out = datetime.strptime(start_time, "%H:%M:%S") + timedelta(hours=remaining_hours)

    print("You get to work until: {}".format(time_out.time()))
    _display_results(remaining_hours)


if __name__ == '__main__':
    print("----------------------")
    print("---- Time Tracker ----")
    print("----------------------")

    print("1 = Normal Mode")
    print("2 = Friday Mode")
    mode = int(input("Enter in Mode: "))

    if mode > FRIDAY_MODE or mode < NORMAL_MODE:
        print("Invalid Mode")
    elif mode == NORMAL_MODE:
        _normal_mode()
    elif mode == FRIDAY_MODE:
        _friday_mode()