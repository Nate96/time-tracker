import time_tracker 
import os

from config import Res, DATABASE
from repository import Punch

punch_clock = time_tracker


def test_adding_punches():
    # GIVEN the database is Empty
    os.remove(f'{DATABASE}')
    with open(f'{DATABASE}', "w") as file: file.write("")

    # VERIFY punch_out returns a Res of NO_PUNCH
    assert punch_clock.punch_out("test") == Res.NO_PUNCH

    # VERIFY punch_in returns a Res of SEC_PUNCH
    assert punch_clock.punch_in("test") == Res.SEC_PUNCH

    # GIVEN last punch type is "in"
    # VERIFY punch_in returns a Res of INVAIL_IN_PUNCH
    assert time_tracker.punch_in("test") == Res.INVAIL_IN_PUNCH

    # VERIFY punch_out returns a Res of SEC_PUNCH
    res = punch_clock.punch_out("test")
    assert res == Res.SEC_PUNCH

    # GIVEN last punch type is "out"
    # VERIFY punch_out returns a Res of INVAIL_OUT_PUNCH
    res = punch_clock.punch_out("test")
    assert res == Res.INVAIL_OUT_PUNCH

    # VERIFY punch_in returns a Res of SEC_PUNCH
    res = punch_clock.punch_in("test")
    assert res == Res.SEC_PUNCH

