from datetime import date, datetime, timedelta

from unittest.mock import MagicMock

from config import PunchType
from punch_clock import punch
from time_sheet import Entry, get_entries, Punch

import punch_clock
import time_sheet

# NOTE: tc = test case

def test_punching(mocker: MagicMock):
    # Punch: defined in time_sheet.py
    # Entry: define in time_sheet.py

    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.execute.return_value.fetchone.side_effect = [ 
        None,                                                                      # [TC1]
        (1, "in",  "2024-01-15 09:00:00", "test"),                                 # [TC1]
        (1, "in",  "2024-01-15 09:00:00", "test"),                                 # [TC2]
        (2, "out", "2024-01-15 10:00:00", "testing"),                              # [TC2]
        (1, "2024-01-15 09:00:00", "2024-01-15 10:00:00", 1.0, "test", "testing"), # [TC2]
        (2, "out", "2024-01-15 10:00:00", "testing"),                              # [TC3]
        (1, "in",  "2024-01-15 10:01:00", "test"),                                 # [TC3]

    ]

    mock_connection.cursor.return_value = mock_cursor
    mocker.patch('sqlite3.connect', return_value=mock_connection)

    # [TC1] GIVEN  an empty database 
    #       VERIFY The system returns a [Punch]
    assert punch("test") == Punch(
                                id=1,
                                type=PunchType.IN,
                                time_stamp="2024-01-15 09:00:00",
                                comment="test")

    # [TC2] GIVEN  A Punch with a type of "in" is in the database
    #       VERIFY The system returns a [Entry]
    assert punch("testing") == Entry(
                                id=1,
                                in_punch="2024-01-15 09:00:00",
                                out_punch="2024-01-15 10:00:00",
                                total_time=1.0,
                                title="test",
                                comment="testing")

    # [TC3] GIVEN  A the last Punch type of out
    #       VERIFY The system returns a [Punch]
    assert punch("test") == Punch(
                                id=1,
                                type=PunchType.IN,
                                time_stamp="2024-01-15 10:01:00",
                                comment="test")


def test_punch_clock_state(mocker: MagicMock):
    # Punch: defined in time_sheet.py
    # Entry: define in time_sheet.py

    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_connection.cursor.return_value = mock_cursor
    mocker.patch('sqlite3.connect', return_value=mock_connection)

    mock_cursor.execute.return_value.fetchone.side_effect = [ 
        None, None,                                                                                # [TC1]
        (1, "in",  "2024-01-15 09:00:00", "test"),                                                 # [TC2]
        None,                                                                                      # [TC2]
        (2, "out",  "2024-01-15 10:00:00", "test"),                                                # [TC3]
        (1, "2024-01-15 09:00:00", "2024-01-15 10:00:00", 1.0, "test", "testing"),                 # [TC3]
        ( "1", "2025-01-15 09:00:00", "2025-01-15 10:00:00", "1.0", "Test Entry", "Test Comment"), # [TC7]  
    ]

    mock_cursor.execute.return_value.fetchall.side_effect = [ 
        [
            (2, "2024-01-14 09:00:00", "2024-01-14 10:00:00", 1.0, "test", "testing"), # [TC3]
            (2, "2024-01-15 09:00:00", "2024-01-15 10:00:00", 1.0, "test", "testing"), # [TC3]
        ],
        [
            (2, "2024-01-14 09:00:00", "2024-01-14 10:00:00", 1.0, "test", "testing"), # [TC3]
            (2, "2024-01-15 09:00:00", "2024-01-15 10:00:00", 1.0, "test", "testing"), # [TC3]
        ]
    ]

    # [TC1] GIVEN  No database
    #       VERIFY last_punch.id and last_entry.id is -1   
    state = punch_clock.State()
    assert state.last_punch.id == -1
    assert state.last_entry.id == -1

    # [TC2] GIVEN  ONLY one punch in the database
    #       VERIFY last_punch.id is 1 and last_entry.id = -1
    state = punch_clock.State()
    assert state.last_punch.id == 1
    assert state.last_entry.id == -1

    # [TC3] GIVEN  An Entry
    #       VERIFY last_punch.id is 2 and last_entry.id = 1
    #              week and day total is 2.0
    #              punch_in_for > 0
    state = punch_clock.State()
    assert state.last_punch.id == 2
    assert state.last_entry.id == 1

    assert state.get_day_total() == 2.0
    assert state.get_week_total() == 2.0

    assert state.get_punched_in_for() > 0

    # [TC7] GIVEN the database has 1 entries
    #       VERIFY get_entries returns 1 when duration = "last"
    assert len(get_entries("last")) == 1


def test_entries(mocker):
    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.execute.return_value.fetchall.side_effect = [ 
        [ # [TC2]
            ( "1", "2025-01-15 09:00:00", "2025-01-15 10:00:00", "1.0", "Test Entry", "Test Comment"), 
            ( "2", "2025-01-15 10:00:00", "2025-01-15 11:00:00", "1.0", "Another Test Entry", "Another Test Comment")
        ], 
        [ # [TC3]
            ( "1", "2025-01-15 09:00:00", "2025-01-15 10:00:00", "1.0", "Test Entry", "Test Comment"), 
            ( "2", "2025-01-15 10:00:00", "2025-01-15 11:00:00", "1.0", "Another Test Entry", "Another Test Comment")
        ], 
        [ # [TC4]
            ( "1", "2025-01-15 09:00:00", "2025-01-15 10:00:00", "1.0", "Test Entry", "Test Comment"), 
            ( "2", "2025-01-15 10:00:00", "2025-01-15 11:00:00", "1.0", "Another Test Entry", "Another Test Comment")
        ], 
        [ # [TC5]
            ( "1", "2025-01-15 09:00:00", "2025-01-15 10:00:00", "1.0", "Test Entry", "Test Comment"), 
            ( "2", "2025-01-15 10:00:00", "2025-01-15 11:00:00", "1.0", "Another Test Entry", "Another Test Comment")
        ], 
        [ # [TC6]
            ( "1", "2025-01-15 09:00:00", "2025-01-15 10:00:00", "1.0", "Test Entry", "Test Comment"), 
        ], 
        [] # [TC7]
    ]
    mock_connection.cursor.return_value = mock_cursor
    mocker.patch('sqlite3.connect', return_value=mock_connection)

    # [TC1] GIVEN  The database is Empty and an invalid duration is inputed
    #       VERIFY Get_entires returns an empty list
    assert get_entries("test") == []

    # [TC2,3,4, 5]
    #  GIVEN  mocked database response of 2 entries
    #  VERIFY The length of res is 2 for day, week, and month
    assert len(get_entries("day")) == 2
    assert len(get_entries("week")) == 2
    assert len(get_entries("month")) == 2
    assert len(get_entries("all")) == 2

    # [TC6] GIVEN mocked database response of 1 entry,
    #       VERIFY get_entries returns 1 entry when duration = "last week"
    assert len(get_entries("last week")) == 1



    # [tc8] GIVEN the database has 2 entries
    #       VERIFY get_entries returns an empty list when INVALID_INTPUT 
    assert get_entries("test") == []


def test_get_date_range():
    test_cases = [
        (date(2026,2,19), (date(2026, 2, 19), date(2026, 2, 15))), # [TC1]
        (date(2026,2,12), (date(2026, 2, 12), date(2026, 2,  8))), # [TC2]
        (date(2026,2,7), (date(2026, 2, 7), date(2026, 2, 1))),    # [TC3]
        (date(2026,2,1), (date(2026, 2, 1), date(2026, 2, 1))),    # [TC3]
    ]

    for current_date, expected in test_cases:
        assert time_sheet._get_week_date_range(current_date) == expected
