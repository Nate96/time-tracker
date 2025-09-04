import time_tracker 
import os

from config import Res, DATABASE
from time_tracker import State, punch_in

punch_clock = time_tracker


def test_adding_punches():
    # GIVEN the database is Empty
    with open(f'{DATABASE}', "w") as file: file.write("")

    # VERIFY punch_out returns a Res of NO_PUNCH
    assert punch_clock.punch_out("test") == Res.NO_PUNCH

    # VERIFY punch_in returns a Res of SEC_PUNCH
    assert punch_clock.punch_in("test") == Res.SEC_IN

    # GIVEN last punch type is "in"
    # VERIFY punch_in returns a Res of INVAIL_IN_PUNCH
    assert time_tracker.punch_in("test") == Res.IN

    # VERIFY punch_out returns a Res of SEC_PUNCH_OUT
    res = punch_clock.punch_out("test")
    assert res == Res.SEC_OUT

    # GIVEN last punch type is "out"
    # VERIFY punch_out returns a Res of INVAIL_OUT_PUNCH
    res = punch_clock.punch_out("test")
    assert res == Res.OUT

    # VERIFY punch_in returns a Res of SEC_PUNCH_IN
    res = punch_clock.punch_in("test")
    assert res == Res.SEC_IN

    # Delete Databse
    os.remove(f'{DATABASE}')

def test_status():
    # GIVEN the database is Empty
    with open(f'{DATABASE}', "w") as file: file.write("")

    # VERIFY status return a state with NO_PUNCH
    assert time_tracker.status().res == Res.NO_PUNCH

    # GIVEN the last punch type was in
    _ = time_tracker.punch_in("test")

    # VERIFY status returns a state with IN
    assert time_tracker.status().res == Res.IN

    # GIVEN the last punch type was out
    _ = time_tracker.punch_out("test")

    # VERIFY status returns a state with OUT
    assert time_tracker.status().res == Res.OUT

    # Delete Databse
    os.remove(f'{DATABASE}')
    


