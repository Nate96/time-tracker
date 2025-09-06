import repository
import time_tracker 
import os
import time

from config import Res, DATABASE
from repository import Entry
from time_tracker import State


punch_clock = time_tracker
REPO = repository


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

def test_entries():
    # GIVEN the database is Empty
    with open(f'{DATABASE}', "w") as file: file.write("")

    # WHEN invalid duration is inputed
    res: list[Entry] = REPO.get_entries("test")

    # VERIFY the first entry's id is -1
    assert res[0].id == -1


    # WHEN there are 2 entries in the DataBase 
    punch_clock.punch_in("Test")

    # GIVEN 45 seconds 
    time.sleep(45)
    s: State = time_tracker.status()
    s = time_tracker.status()

    # VERIFY punch_in_for is 0.01, week_total is 0, day_toal is 0 
    assert s.get_punched_in_for() == 0.01
    assert s.get_day_total() == 0
    assert s.get_week_total() == 0

    time.sleep(1)
    punch_clock.punch_out("Test")

    # VERIFY week_total is 0.01, day_toal is 0.01 
    assert s.get_day_total() == 0.01
    assert s.get_week_total() == 0.01

    # GIVEN an Entry is added to the database
    punch_clock.punch_in("Test")
    punch_clock.punch_out("Test")

    # VERIFY the length of res is 2 for day
    res = punch_clock.get_entries("day")
    assert len(res) == 2

    # VERIFY the length of res is 2 for week
    res = punch_clock.get_entries("week")
    assert len(res) == 2

    # VERIFY the length of res is 2 for month
    res = punch_clock.get_entries("month")
    assert len(res) == 2

    # VERIFY get_entries returns an empty list when INVALID_INTPUT 
    assert punch_clock.get_entries("test") == []
