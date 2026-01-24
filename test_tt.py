from unittest.mock import MagicMock

from config import PunchType
from punch_clock import punch
import punch_clock
from time_sheet import Entry, get_entries, Punch

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
                                type=PunchType.IN.value,
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
                                type=PunchType.IN.value,
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
        None, None,                                                                # [TC1]
        (1, "in",  "2024-01-15 09:00:00", "test"),                                 # [TC2]
        None,                                                                      # [TC2]
        (2, "out",  "2024-01-15 10:00:00", "test"),                                # [TC3]
        (1, "2024-01-15 09:00:00", "2024-01-15 10:00:00", 1.0, "test", "testing"), # [TC3]
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


def test_entries(mocker):
    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.execute.return_value.fetchall.side_effect = [ 
        [
            ( "1", "2025-01-15 09:00:00", "2025-01-15 10:00:00", "1.0", "Test Entry", "Test Comment"), 
            ( "2", "2025-01-15 10:00:00", "2025-01-15 11:00:00", "1.0", "Another Test Entry", "Another Test Comment")
        ], # [TC2]
        [
            ( "1", "2025-01-15 09:00:00", "2025-01-15 10:00:00", "1.0", "Test Entry", "Test Comment"), 
            ( "2", "2025-01-15 10:00:00", "2025-01-15 11:00:00", "1.0", "Another Test Entry", "Another Test Comment")
        ], # [TC3]
        [
            ( "1", "2025-01-15 09:00:00", "2025-01-15 10:00:00", "1.0", "Test Entry", "Test Comment"), 
            ( "2", "2025-01-15 10:00:00", "2025-01-15 11:00:00", "1.0", "Another Test Entry", "Another Test Comment")
        ], # [TC4]
        [] # [TC5]
    ]
    mock_connection.cursor.return_value = mock_cursor
    mocker.patch('sqlite3.connect', return_value=mock_connection)

    # [TC1] GIVEN  The database is Empty and an invalid duration is inputed
    #       VERIFY Get_entires returns an emptry list
    assert get_entries("test") == []

    # [TC2,3,4] GIVEN  The database has 2 entries
    #           VERIFY The length of res is 2 for day, week, and month
    assert len(get_entries("day")) == 2
    assert len(get_entries("week")) == 2
    assert len(get_entries("month")) == 2

    # [tc5] GIVEN the database has 2 entries
    #       VERIFY get_entries returns an empty list when INVALID_INTPUT 
    assert get_entries("test") == []
