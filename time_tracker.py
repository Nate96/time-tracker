from os import sendfile
import repository

from datetime import date, datetime
from config import PunchType, Res
from repository import Punch, Entry



REPO = repository
FORMAT_STRING = "%Y-%m-%d %H:%M:%S"

class State():
    def __init__(self, res: Res):
        self.res = res
        self.last_punch: Punch = REPO.get_last_punch()
        self.last_entry: Entry = REPO.get_last_entry()

    def get_punched_in_for(self) -> float:
        in_time: datetime = datetime.strptime(str(self.last_punch.time_stamp), FORMAT_STRING)
        return round((datetime.now() - in_time).total_seconds() / 3600, 2)


    def get_day_total(self) -> float:
        return self._get_total(REPO.get_entries("day"))

    def get_week_total(self) -> float:
        return self._get_total(REPO.get_entries("week"))

    def _get_total(self, entries: list[Entry]):
        total: float = 0

        for ent in entries: 
            total += ent.total_time
        return round(total, 2)


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
    else: 
        REPO.add_punch(Punch(PunchType.OUT.value, comment))
        REPO.add_entry()
        return Res.SEC_OUT


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

