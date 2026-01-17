from config import Res
from punch_clock import punch_out, punch_in, status
from time_sheet import get_entries
from unittest.mock import MagicMock

# NOTE: tc = test case

def test_adding_punches(mocker):
    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.execute.return_value.fetchone.side_effect = [ 
        None, # tc1
        None, # tc2
        (1, "in",  "2024-01-15 09:00:00", "test"), # tc3 Punch
        (1, "in",  "2024-01-15 09:00:00", "test"), # tc4 Punch
        (1, "out",  "2024-01-15 10:00:00", "test comment"), # tc5 Punch
    ]
    mock_connection.cursor.return_value = mock_cursor
    mocker.patch('sqlite3.connect', return_value=mock_connection)

    # [tc1] GIVEN the database is Empty VERIFY punch_out returns a Res of
    # NO_PUNCH
    assert punch_out("test") == Res.NO_PUNCH

    # [tc2] GIVEN the database is Empty VERIFY punch_in returns a Res of
    # SEC_PUNCH
    assert punch_in("test") == Res.SEC_IN

    # [tc3] GIVEN last punch type is "in" VERIFY punch_in returns a Res of
    # INVAIL_IN_PUNCH
    assert punch_in("test") == Res.IN
 
    # [tc4] GIVEN the last punch has a type of "in" VERIFY punch_out returns a
    # Res of SEC_PUNCH_OUT
    assert punch_out("test comment") == Res.SEC_OUT
 
    # [tc5] GIVEN last punch type is "out" VERIFY punch_out returns a Res of
    # INVAIL_OUT_PUNCH
    assert punch_out("another test comment") == Res.OUT
 
def test_status(mocker):
    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    # TODO: Refactor so it doesn't call the database 3 times
    mock_cursor.execute.return_value.fetchone.side_effect = [ 
        None, # tc1
        None, # tc1
        None, # tc1
    ]
    mock_connection.cursor.return_value = mock_cursor
    mocker.patch('sqlite3.connect', return_value=mock_connection)

    # [tc1] VERIFY status return a state with NO_PUNCH
    assert status().res == Res.NO_PUNCH
 
    # GIVEN the last punch type was in
#     _ = punch_in("test")
# 
#     # VERIFY status returns a state with IN
#     assert status().res == Res.IN
# 
#     # GIVEN the last punch type was out
#     _ = punch_out("test")
# 
#     # VERIFY status returns a state with OUT
#     assert status().res == Res.OUT
# 
#     # Delete Databse
#     os.remove(f'{DATABASE}')
# 
def test_entries(mocker):
    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.execute.return_value.fetchall.side_effect = [ 
        [
            ( "1", "2025-01-15 09:00:00", "2025-01-15 10:00:00", "1.0", "Test Entry", "Test Comment"), 
            ( "2", "2025-01-15 10:00:00", "2025-01-15 11:00:00", "1.0", "Another Test Entry", "Another Test Comment")
        ], # tc2
        [
            ( "1", "2025-01-15 09:00:00", "2025-01-15 10:00:00", "1.0", "Test Entry", "Test Comment"), 
            ( "2", "2025-01-15 10:00:00", "2025-01-15 11:00:00", "1.0", "Another Test Entry", "Another Test Comment")
        ], # tc3
        [
            ( "1", "2025-01-15 09:00:00", "2025-01-15 10:00:00", "1.0", "Test Entry", "Test Comment"), 
            ( "2", "2025-01-15 10:00:00", "2025-01-15 11:00:00", "1.0", "Another Test Entry", "Another Test Comment")
        ], # tc4
        [] # tc5
    ]
    mock_connection.cursor.return_value = mock_cursor
    mocker.patch('sqlite3.connect', return_value=mock_connection)

    # [tc1] GIVEN the database is Empty and an invalid duration is inputed
    #       VERIFY get_entires returns an emptry list
    assert get_entries("test") == []

    # [tc2,3,4] GIVEN the database has 2 entries
    #           VERIFY the length of res is 2 for day, week, and month
    assert len(get_entries("day")) == 2
    assert len(get_entries("week")) == 2
    assert len(get_entries("month")) == 2

    # [tc5] GIVEN the database has 2 entries
    #       VERIFY get_entries returns an empty list when INVALID_INTPUT 
    assert get_entries("test") == []


   # VERIFY punch_in_for is 0.01, week_total is 0, day_toal is 0 
#     assert s.get_punched_in_for() > 0
#     assert s.get_day_total() == 0
#     assert s.get_week_total() == 0
# 
#     time.sleep(1)
#     _ = punch_out("Test")
# 
#     # VERIFY week_total is 0.01, day_toal is 0.01 
#     assert s.get_day_total() > 0
#     assert s.get_week_total() > 0
# 
#     # GIVEN an Entry is added to the database
#     punch_in("Test")
#     punch_out("Test")


# def test_presenter():
# 
#     def _test_presenter():
#         try:
#             show_last_punch()
#             show_last_entry()
# 
#             show_entries("day")
#             show_entries("week")
#             show_entries("month")
#             show_entries("all")
# 
#             report()
#         except(Exception): assert False
# 
# 
#     # GIVEN no Database
#     # VERIFY the presenter doesn't error out
#     _test_presenter()
# 
#     # GIVEN the database is Empty
#     with open(f'{DATABASE}', "w") as file: file.write("")
# 
#     # VERIFY the presenter doesn't error out
#     _test_presenter()
# 
#     # GIVEN one punch
#     punch_in("test")
# 
#     # VERIFY the presenter doesn't error out
#     _test_presenter()
# 
#     # GIVEN one Entry
#     punch_out("test")
# 
#     # VERIFY the presenter doesn't error out
#     _test_presenter()
# 
#     # Delete Databse
#     os.remove(f'{DATABASE}')
