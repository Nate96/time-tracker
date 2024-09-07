# NOTE: typing is not inforced but acts more like a hint
# ISSUE: Create Table sql scirpt has two commands and python
#        does not support this.
from typing import Tuple
import sqlite3
import os
import logging

logger = logging.getLogger(__name__)

scripts = {
        'DATABASE_LOCATION':  "../Test/Log.db",
        'CREATE_TABLE':       "../SqlScripts/CreateTables.sql",
        'LAST_PUNCH       ':  "../SqlScripts/GetLastPunch.sql",
        'INSERT_PUNCH     ':  "../SqlScripts/InsertPunch.sql",
        'INSERT_ENTRY     ':  "../SqlScripts/InsertEntry.sql",
        'TODAY            ':  "../SqlScripts/GetTodayEntry.sql",
        'WEEK             ':  "../SqlScripts/GetWeekEntry.sql",
        'MONTH            ':  "../SqlScripts/GetMonthEntry.sql",
        'LAST_ENTRY       ':  "../SqlScripts/GetLastEntry.sql",
}


def add_punch(punch_type, punch_datetime, comment):
    _connect_to_data_base()

    CUR.execute(os.read(scripts['INSERT_PUNCH']),
                {
                    punch_type,
                    punch_datetime,
                    comment
                 })
    CON.commit()


def add_entry():
    CON = sqlite3.connect(scripts['DATABASE_LOCATION'])
    CUR = CON.cursor()
    CUR.execute(scripts['INSERT_ENTRY']).commit()


def get_entries(self, duration):
    CON = sqlite3.connect(self.scripts['DATABASE_LOCATION'])
    CUR = CON.cursor()

    if duration == "day":
        return CUR.execute(self.scripts['TODAY'])
    elif duration == "week":
        return CUR.execute(self.scripts['WEEK'])
    elif duration == "month":
        return CUR.execute(self.scripts['MONTH'])
    elif duration == "last":
        return CUR.execute(self.scripts['LAST_ENTRY'])


def get_last_punch() -> Tuple[int, str, str, str]:
    """get last punch
    Gets the most recent punch in the database

    Returns:
    Tuple[id, type, punch_datetime, comment]
    """
    cursor = _connect_to_data_base()
    return cursor.execute(scripts['LAST_PUNCH']).fetchone()


def _sql_script(file_path) -> str:
    """sql script
    Reads in the given .sql file

    Parameters:
    file_path: path to the sql script

    Returns:
    str: Content of the .sql file
    """
    with open(file_path, 'r') as file:
        script = file.read()
    return script


def _connect_to_data_base():
    """connect to data base
    connects to database and creates tables for punches and entries.

    Returns:
    the Cursor for the connections
    """
    CON = sqlite3.connect(scripts['DATABASE_LOCATION'])
    CUR = CON.cursor()
    CUR.execute(_sql_script(scripts['CREATE_TABLE']))
    return CON.cursor()
