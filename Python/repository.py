# NOTE: typing is not inforced but acts more like a hint
# ISSUE: Create Table sql scirpt has two commands and python
#        does not support this.

from typing import Tuple, List
import sqlite3
import datetime


scripts = {
        'DATABASE_LOCATION':  "../Test/Log.db",
        'create_punch_table': "../SqlScripts/CreatePunchTable.sql",
        'create_entry_table': "../SqlScripts/CreateEntryTable.sql",
        'LAST_PUNCH':         "../SqlScripts/GetLastPunch.sql",
        'INSERT_PUNCH':  "../SqlScripts/InsertPunch.sql",
        'INSERT_ENTRY':  "../SqlScripts/InsertEntry.sql",
        'TODAY':  "../SqlScripts/GetTodayEntry.sql",
        'WEEK':  "../SqlScripts/GetWeekEntry.sql",
        'MONTH':  "../SqlScripts/GetMonthEntry.sql",
        'LAST_ENTRY':  "../SqlScripts/GetLastEntry.sql",
}


def add_punch(punch_type, comment) -> Tuple[str, str, str, str]:
    """add punch
    Inserts a new punch into the table.

    Parameters:
    punch_type: "in" or "out"
    comment: comment for the punch

    Returns:
    Boolean
    """
    datetime.datetime.now()
    con = _connect_to_data_base()
    con.cursor().execute(_sql_script(scripts['INSERT_PUNCH']),
                         (
                              punch_type,
                              comment
                          ))
    con.commit()
    con.close()

    return get_last_punch()


def add_entry() -> Tuple[int, str, str, float, str, str]:
    """
    Inserts a new entry into table

    Returns:
    Tuple[id, in_punch, out_punch, total_time, task_name, task_comment]
    """
    con = _connect_to_data_base()
    con.cursor().execute(_sql_script(scripts['INSERT_ENTRY']))
    con.commit()
    con.close()

    return get_last_entry()


def get_entries(duration) -> List[Tuple[str, str, str, str, str, str]]:
    """get entries
    Get entries from the data base for the given duration

    Parameters:
    duration: the range of entry of entries

    Returns:
    list[Tuple[id, in_punch, out_punch, total_time, task_name, task_comment]]
    """
    con = _connect_to_data_base()
    cur = con.cursor()

    if duration == "day":
        res = cur.execute(_sql_script(scripts['TODAY'])).fetchall()
    elif duration == "week":
        res = cur.execute(_sql_script(scripts['WEEK'])).fetchall()
    elif duration == "month":
        res = cur.execute(_sql_script(scripts['MONTH'])).fetchall()
    else:
        return "invalid duration"

    con.close()

    return res


def get_last_punch() -> Tuple[int, str, str, str]:
    """get last punch
    Gets the most recent punch in the database

    Returns:
    Tuple[id, type, punch_datetime, comment]
    """
    con = _connect_to_data_base()
    cur = con.cursor()
    res = cur.execute(_sql_script(scripts['LAST_PUNCH'])).fetchone()

    con.close()

    return res


def get_last_entry() -> Tuple[str, str, str, str, str, str]:
    """get last entry
    Gets the most recent entry in the database

    Returns:
    Tuple[id, in_punch, out_punch, total_time, task_name, task_comment]
    """
    con = _connect_to_data_base()
    res = con.cursor().execute(_sql_script(scripts['LAST_ENTRY'])).fetchone()

    con.close()

    return res


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
    the connection for the datbase
    """
    CON = sqlite3.connect(scripts['DATABASE_LOCATION'])
    CUR = CON.cursor()
    CUR.execute(_sql_script(scripts['create_punch_table']))
    CUR.execute(_sql_script(scripts['create_entry_table']))

    return CON
