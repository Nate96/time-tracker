"""
Examples of mocking SQLite database results for the time-tracker application.
This file demonstrates different mocking strategies.
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, MagicMock, patch

from config import Res, PunchType
from time_sheet import Punch, Entry
from punch_clock import State, punch_out, punch_in, status


# ==============================================================================
# APPROACH 1: Mock the time_sheet module functions
# ==============================================================================

def test_punch_in_with_mocked_get_last_punch(mocker):
    """
    Mock get_last_punch to return a specific punch without database interaction.
    
    This is useful when you want to test punch_in logic without database.
    """
    # GIVEN: Mock get_last_punch to return a punch that's already "out"
    mock_punch = Punch(
        punch_type=PunchType.OUT.value,
        comment="previous punch",
        id=1
    )
    mocker.patch('time_sheet.get_last_punch', return_value=mock_punch)
    
    # Mock add_punch to avoid database write
    mock_add_punch = mocker.patch('time_sheet.add_punch')
    
    # WHEN: We punch in
    result = punch_in("test comment")
    
    # THEN: Should return success and call add_punch
    assert result == Res.SEC_IN
    mock_add_punch.assert_called_once()


def test_punch_in_already_punched_in(mocker):
    """
    Mock get_last_punch to simulate user already punched in.
    """
    # GIVEN: User is already punched in
    mock_punch = Punch(
        punch_type=PunchType.IN.value,
        comment="already in",
        id=1
    )
    mocker.patch('time_sheet.get_last_punch', return_value=mock_punch)
    
    # WHEN: We try to punch in again
    result = punch_in("test comment")
    
    # THEN: Should return IN (already punched in)
    assert result == Res.IN


def test_punch_out_no_previous_punch(mocker):
    """
    Mock get_last_punch to simulate no previous punches.
    """
    # GIVEN: No previous punches (id = -1)
    mock_punch = Punch(
        punch_type="",
        comment="",
        id=-1
    )
    mocker.patch('time_sheet.get_last_punch', return_value=mock_punch)
    
    # WHEN: We try to punch out
    result = punch_out("test comment")
    
    # THEN: Should return NO_PUNCH
    assert result == Res.NO_PUNCH


def test_status_with_mocked_data(mocker):
    """
    Mock multiple functions to test status with complete mocked data.
    """
    # GIVEN: Mock a punch and an entry
    mock_punch = Punch(
        punch_type=PunchType.IN.value,
        comment="working",
        time_stamp="2024-01-15 09:00:00",
        id=1
    )
    mock_entry = Entry(
        id=1,
        total_time=8.5,
        title="Development",
        comment="Working on features",
        in_punch="2024-01-15 09:00:00",
        out_punch="2024-01-15 17:30:00"
    )
    
    mocker.patch('time_sheet.get_last_punch', return_value=mock_punch)
    mocker.patch('time_sheet.get_last_entry', return_value=mock_entry)
    mocker.patch('time_sheet.get_entries', return_value=[mock_entry])
    
    # WHEN: We check status
    state = status()
    
    # THEN: Should show user is punched IN
    assert state.res == Res.IN
    assert state.last_punch.id == 1
    assert state.last_entry.total_time == 8.5


# ==============================================================================
# APPROACH 2: Mock SQLite connection and cursor
# ==============================================================================

def test_get_last_punch_with_mocked_sqlite(mocker):
    """
    Mock the SQLite connection to control database responses.
    
    This gives you fine-grained control over what the database returns.
    """
    # Import here to avoid circular imports in examples
    import time_sheet
    
    # GIVEN: Mock SQLite connection
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    
    # Configure mock to return specific data
    # fetchone() returns a single row: (id, type, timestamp, comment)
    mock_cursor.execute.return_value.fetchone.return_value = (
        1,                          # id
        PunchType.IN.value,         # type
        "2024-01-15 09:00:00",      # timestamp
        "morning punch"             # comment
    )
    mock_connection.cursor.return_value = mock_cursor
    
    # Patch sqlite3.connect to return our mock
    mocker.patch('sqlite3.connect', return_value=mock_connection)
    
    # WHEN: We call get_last_punch
    punch = time_sheet.get_last_punch()
    
    # THEN: Should return a punch with mocked data
    assert punch.id == 1
    assert punch.type == PunchType.IN.value
    assert punch.comment == "morning punch"


def test_get_entries_with_mocked_sqlite(mocker):
    """
    Mock SQLite to return multiple entries.
    """
    import time_sheet
    
    # GIVEN: Mock SQLite connection with multiple entries
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    
    # fetchall() returns multiple rows
    mock_cursor.execute.return_value.fetchall.return_value = [
        (1, "2024-01-15 09:00:00", "2024-01-15 17:00:00", 8.0, "Dev", "Feature A"),
        (2, "2024-01-15 18:00:00", "2024-01-15 20:00:00", 2.0, "Dev", "Feature B"),
    ]
    mock_connection.cursor.return_value = mock_cursor
    mocker.patch('sqlite3.connect', return_value=mock_connection)
    
    # WHEN: We get entries for the day
    entries = time_sheet.get_entries("day")
    
    # THEN: Should return 2 entries with mocked data
    assert len(entries) == 2
    assert entries[0].total_time == 8.0
    assert entries[1].total_time == 2.0
    assert entries[0].title == "Dev"


# ==============================================================================
# APPROACH 3: Use in-memory SQLite database
# ==============================================================================

def test_with_in_memory_database(mocker):
    """
    Use an actual SQLite database in memory instead of mocking.
    
    This is a hybrid approach - real database behavior but no file I/O.
    """
    import time_sheet
    import sqlite3
    
    # GIVEN: Create in-memory database
    in_memory_db = sqlite3.connect(':memory:')
    
    # Patch sqlite3.connect to return in-memory database
    mocker.patch('sqlite3.connect', return_value=in_memory_db)
    
    # WHEN: We add a punch (tables will be created in memory)
    punch = Punch(PunchType.IN.value, "test punch")
    time_sheet.add_punch(punch)
    
    # THEN: We can retrieve it
    last_punch = time_sheet.get_last_punch()
    assert last_punch.type == PunchType.IN.value
    assert last_punch.comment == "test punch"
    
    # Clean up
    in_memory_db.close()


# ==============================================================================
# APPROACH 4: Mock with pytest fixtures for reusable test data
# ==============================================================================

@pytest.fixture
def mock_punched_in_state(mocker):
    """
    Fixture that sets up a 'punched in' state.
    Reusable across multiple tests.
    """
    mock_punch = Punch(
        punch_type=PunchType.IN.value,
        comment="working",
        time_stamp="2024-01-15 09:00:00",
        id=1
    )
    mocker.patch('time_sheet.get_last_punch', return_value=mock_punch)
    return mock_punch


@pytest.fixture
def mock_punched_out_state(mocker):
    """
    Fixture that sets up a 'punched out' state.
    """
    mock_punch = Punch(
        punch_type=PunchType.OUT.value,
        comment="done for the day",
        time_stamp="2024-01-15 17:00:00",
        id=2
    )
    mocker.patch('time_sheet.get_last_punch', return_value=mock_punch)
    return mock_punch


@pytest.fixture
def mock_entries_list(mocker):
    """
    Fixture that provides a list of mock entries.
    """
    entries = [
        Entry(
            id=1,
            total_time=8.0,
            title="Development",
            comment="Feature work",
            in_punch="2024-01-15 09:00:00",
            out_punch="2024-01-15 17:00:00"
        ),
        Entry(
            id=2,
            total_time=2.0,
            title="Meetings",
            comment="Team sync",
            in_punch="2024-01-15 18:00:00",
            out_punch="2024-01-15 20:00:00"
        )
    ]
    mocker.patch('time_sheet.get_entries', return_value=entries)
    return entries


def test_using_punched_in_fixture(mock_punched_in_state):
    """
    Example using the punched_in fixture.
    """
    # GIVEN: State from fixture (already punched in)
    # WHEN: We try to punch in again
    result = punch_in("test")
    
    # THEN: Should return IN (already punched in)
    assert result == Res.IN


def test_using_punched_out_fixture(mock_punched_out_state, mocker):
    """
    Example using the punched_out fixture.
    """
    # GIVEN: State from fixture (already punched out)
    # Mock add_punch to avoid database write
    mocker.patch('time_sheet.add_punch')
    
    # WHEN: We punch in
    result = punch_in("starting work")
    
    # THEN: Should succeed
    assert result == Res.SEC_IN


def test_state_with_entries_fixture(mock_punched_in_state, mock_entries_list, mocker):
    """
    Example combining multiple fixtures.
    """
    # GIVEN: Punched in state + entries
    mock_entry = Entry(
        id=1,
        total_time=8.0,
        title="Dev",
        comment="Work",
        in_punch="2024-01-15 09:00:00",
        out_punch="2024-01-15 17:00:00"
    )
    mocker.patch('time_sheet.get_last_entry', return_value=mock_entry)
    
    # WHEN: We check status
    state = status()
    
    # THEN: Can verify totals
    assert state.res == Res.IN
    day_total = state.get_day_total()
    week_total = state.get_week_total()
    
    # Both should be 10.0 (8.0 + 2.0 from our mocked entries)
    assert day_total == 10.0
    assert week_total == 10.0


# ==============================================================================
# APPROACH 5: Parametrized tests with mocked data
# ==============================================================================

@pytest.mark.parametrize("last_punch_type,expected_result", [
    (PunchType.OUT.value, Res.SEC_IN),   # Can punch in after punch out
    (PunchType.IN.value, Res.IN),        # Cannot punch in when already in
])
def test_punch_in_states(mocker, last_punch_type, expected_result):
    """
    Parametrized test for different punch_in scenarios.
    """
    # GIVEN: Different punch states
    mock_punch = Punch(
        punch_type=last_punch_type,
        comment="test",
        id=1
    )
    mocker.patch('time_sheet.get_last_punch', return_value=mock_punch)
    
    if expected_result == Res.SEC_IN:
        mocker.patch('time_sheet.add_punch')
    
    # WHEN: We punch in
    result = punch_in("test")
    
    # THEN: Should match expected result
    assert result == expected_result


# ==============================================================================
# APPROACH 6: Context manager for temporary mocking
# ==============================================================================

def test_with_context_manager_mocking():
    """
    Using 'with' statement for temporary mocking.
    
    This is useful for isolated mocking within a test.
    """
    from unittest.mock import patch
    
    # GIVEN: Temporarily mock get_last_punch
    with patch('time_sheet.get_last_punch') as mock_get_punch:
        mock_get_punch.return_value = Punch(
            punch_type=PunchType.OUT.value,
            comment="test",
            id=1
        )
        
        with patch('time_sheet.add_punch') as mock_add:
            # WHEN: We punch in
            result = punch_in("work time")
            
            # THEN: Should succeed
            assert result == Res.SEC_IN
            mock_add.assert_called_once()
    
    # After the 'with' block, mocks are automatically cleaned up


if __name__ == "__main__":
    # Run with: pytest test_mocking_examples.py -v
    pytest.main([__file__, "-v"])
