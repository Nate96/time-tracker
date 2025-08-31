# NOTE: typing is not inforced but acts more like a hint
# ISSUE: Create Table sql scirpt has two commands and python
#        does not support this.

from config import DATABASE, SQL, PunchType

import sqlite3

def add_punch(punch_type: PunchType, comment): 
    con = _connect_to_data_base()
    con.cursor().execute(_sql_script(SQL['INSERT_PUNCH']),
                         (
                              punch_type.value,
                              comment
                          ))
    con.commit()
    con.close()

    return get_last_punch()


def add_entry(): 
    con = _connect_to_data_base()
    con.cursor().execute(_sql_script(SQL['INSERT_ENTRY']))
    con.commit()
    con.close()

    return get_last_entry()


def get_entries(duration):
    con = _connect_to_data_base()
    cur = con.cursor()

    if duration == "day":
        res = cur.execute(_sql_script(SQL['TODAY'])).fetchall()
    elif duration == "week":
        res = cur.execute(_sql_script(SQL['WEEK'])).fetchall()
    elif duration == "month":
        res = cur.execute(_sql_script(SQL['MONTH'])).fetchall()
    else:
        return "invalid duration"

    con.close()

    return res


def get_last_punch(): 
    con = _connect_to_data_base()
    cur = con.cursor()
    res = cur.execute(_sql_script(SQL['LAST_PUNCH'])).fetchone()

    con.close()

    return res


def get_last_entry():
    con = _connect_to_data_base()
    res = con.cursor().execute(_sql_script(SQL['LAST_ENTRY'])).fetchone()

    con.close()

    return res


def _sql_script(file_path: str) -> str:
    """sql script
    Reads in the given .sql file

    Returns: sql_stript string
    """
    with open(file_path, 'r') as file:
        script = file.read()
    return script


def _connect_to_data_base() -> sqlite3.Connection:
    CON = sqlite3.connect(f'{DATABASE}')
    CUR = CON.cursor()
    CUR.execute(_sql_script(SQL['create_punch_table']))
    CUR.execute(_sql_script(SQL['create_entry_table']))

    return CON
