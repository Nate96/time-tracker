import os
import time

from config import Res, DATABASE
from time_sheet import Entry
from punch_clock import State, punch_out, punch_in, status
from time_sheet import get_entries
from presenter import show_last_punch, show_last_entry, show_entries, report



def test_adding_punches():
    # GIVEN the database is Empty
    with open(f'{DATABASE}', "w") as file: file.write("")

    # VERIFY punch_out returns a Res of NO_PUNCH
    assert punch_out("test") == Res.NO_PUNCH

    # VERIFY punch_in returns a Res of SEC_PUNCH
    assert punch_in("test") == Res.SEC_IN

    # GIVEN last punch type is "in"
    # VERIFY punch_in returns a Res of INVAIL_IN_PUNCH
    assert punch_in("test") == Res.IN

    # VERIFY punch_out returns a Res of SEC_PUNCH_OUT
    res = punch_out("test")
    assert res == Res.SEC_OUT

    # GIVEN last punch type is "out"
    # VERIFY punch_out returns a Res of INVAIL_OUT_PUNCH
    res = punch_out("test")
    assert res == Res.OUT

    # VERIFY punch_in returns a Res of SEC_PUNCH_IN
    res = punch_in("test")
    assert res == Res.SEC_IN

    # Delete Databse
    os.remove(f'{DATABASE}')

def test_status():
    # GIVEN the database is Empty
    with open(f'{DATABASE}', "w") as file: file.write("")

    # VERIFY status return a state with NO_PUNCH
    assert status().res == Res.NO_PUNCH

    # GIVEN the last punch type was in
    _ = punch_in("test")

    # VERIFY status returns a state with IN
    assert status().res == Res.IN

    # GIVEN the last punch type was out
    _ = punch_out("test")

    # VERIFY status returns a state with OUT
    assert status().res == Res.OUT

    # Delete Databse
    os.remove(f'{DATABASE}')

def test_entries():
    # GIVEN the database is Empty
    with open(f'{DATABASE}', "w") as file: file.write("")

    # WHEN invalid duration is inputed
    res: list[Entry] = get_entries("test")

    # VERIFY the first entry's id is -1
    assert res == []


    # WHEN there are 2 entries in the DataBase 
    _ = punch_in("Test")

    # GIVEN 45 seconds 
    time.sleep(45)
    s: State = status()
    s = status()

    # VERIFY punch_in_for is 0.01, week_total is 0, day_toal is 0 
    assert s.get_punched_in_for() > 0
    assert s.get_day_total() == 0
    assert s.get_week_total() == 0

    time.sleep(1)
    _ = punch_out("Test")

    # VERIFY week_total is 0.01, day_toal is 0.01 
    assert s.get_day_total() > 0
    assert s.get_week_total() > 0

    # GIVEN an Entry is added to the database
    punch_in("Test")
    punch_out("Test")

    # VERIFY the length of res is 2 for day
    res = get_entries("day")
    assert len(res) == 2

    # VERIFY the length of res is 2 for week
    res = get_entries("week")
    assert len(res) == 2

    # VERIFY the length of res is 2 for month
    res = get_entries("month")
    assert len(res) == 2

    # VERIFY get_entries returns an empty list when INVALID_INTPUT 
    assert get_entries("test") == []

    # Delete Databse
    os.remove(f'{DATABASE}')

def test_presenter():

    def _test_presenter():
        try:
            show_last_punch()
            show_last_entry()

            show_entries("day")
            show_entries("week")
            show_entries("month")
            show_entries("all")

            report()
        except:
            assert False


    # GIVEN no Database
    # VERIFY the presenter doesn't error out
    _test_presenter()

    # GIVEN the database is Empty
    with open(f'{DATABASE}', "w") as file: file.write("")

    # VERIFY the presenter doesn't error out
    _test_presenter()

    # GIVEN one punch
    punch_in("test")

    # VERIFY the presenter doesn't error out
    _test_presenter()

    # GIVEN one Entry
    punch_out("test")

    # VERIFY the presenter doesn't error out
    _test_presenter()

    # Delete Databse
    os.remove(f'{DATABASE}')



