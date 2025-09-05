from datetime import datetime
from config import PunchType, Res
from repository import Punch 

import repository
import config


REPO = repository

class State():
    def __init__(self, res: Res):
        self.res = res
        self.last_punch = REPO.get_last_punch()
        self.last_entry = REPO.get_last_entry()

    def get_punched_in_for(self) -> float:
        # last_punch_time = datetime.fromisoformat()
        # delta_time = datetime.now() - last_punch_time

        return 0.0 # delta_time.total_seconds() / 3600
    
    def get_day_total(self) -> float:
        return 0.0

    def get_week_total(self) -> float:
        week_entries = REPO.get_entries("week")

        total_week_hours = 0
        for entry in week_entries:
            total_week_hours += float()

        return round(total_week_hours, 2)




def punch_in(comment: str) -> Res:
    '''
    Returns SEC_PUNCH OR INVAILID_IN_PUNCH
    '''
    # NOTE: does not have id
    last_punch: Punch = REPO.get_last_punch()

    if last_punch.id == -1 or last_punch.type == PunchType.OUT.value:
        REPO.add_punch(Punch(PunchType.IN.value, comment))
        return Res.SEC_IN
    return Res.IN


def punch_out(comment: str) -> Res:
    '''
    Returns NO_PUNCH, INVAID_OUT, SEC_PUNCH, DB.ERROR
    '''
    last_punch: Punch = REPO.get_last_punch()

    if last_punch.id == -1:
        return Res.NO_PUNCH 
    elif last_punch.type == "out":
        return Res.OUT
    elif last_punch.type == "in":
        REPO.add_punch(Punch(PunchType.OUT.value, comment))
        REPO.add_entry()
        return Res.SEC_OUT
    else:
        return Res.DB_ERROR 


def status() -> State:
    '''
    Returns NO_PUNCH, OUT, IN 
    '''
    last_punch: Punch = REPO.get_last_punch()

    if last_punch.id == -1:
        return State(Res.NO_PUNCH)
    elif last_punch.type == PunchType.OUT.value: 
        return State(Res.OUT)
    return State(Res.IN)

# def show_entries() -> None:


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

    if day_of_week <= config.TRACKER["MAX_WORK_WEEK_DAYS"]:
        projected_hours = day_of_week * config.TRACKER["HOURS_PER_DAY"]
    else:
        projected_hours = config.TRACKER["MAX_WORK_WEEK_HOURS"]

    return hours - projected_hours
