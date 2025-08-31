# NOTE: typing is not inforced but acts more like a hint
# ISSUE: Create Table sql scirpt has two commands and python
#        does not support this.

from sqlite3.dbapi2 import Connection
from config import DATABASE, SQL, PunchType
from datetime import datetime

import sqlite3

class Punch():
    def __init__(self, punch_type: str, comment: str, time_stamp=None, id=0):
        self.id         = id
        self.type       = punch_type
        self.time_stamp = time_stamp
        self.comment    = comment


class Entry():
    def __init__(self, id: int, in_punch: datetime, out_punch: datetime,
             total_time: float, title: str, comment: str):
        self.id         = id
        self.in_punch   = in_punch
        self.out_punch  = out_punch
        self.total_time = total_time
        self.title      = title
        self.comment    = comment


def add_punch(punch: Punch) -> None: 
    con = sqlite3.connect(f'{DATABASE}')
    con.cursor().execute(_sql_script(SQL['INSERT_PUNCH']),
                         (
                              punch.type,
                              punch.comment
                          ))
    con.commit()
    con.close()

    punch.time_stamp = datetime.now()



def add_entry() -> Entry: 
    con = sqlite3.connect(f'{DATABASE}')
    con.cursor().execute(_sql_script(SQL['INSERT_ENTRY']))

    res = con.cursor().execute(_sql_script(SQL['LAST_ENTRY'])).fetchone()

    con.commit()
    con.close()

    return Entry(res[0], res[1], res[2], res[3], res[4], res[5])
            


def get_entries(duration) -> list[Entry]:
    con = sqlite3.connect(f'{DATABASE}')
    cur = con.cursor()

    if duration == "day":
        res = cur.execute(_sql_script(SQL['TODAY'])).fetchall()
    elif duration == "week":
        res = cur.execute(_sql_script(SQL['WEEK'])).fetchall()
    elif duration == "month":
        res = cur.execute(_sql_script(SQL['MONTH'])).fetchall()
    else:
        return [Entry(-1, datetime.now(), datetime.now(), 0.0, "", "")]

    con.close()

    return res


def get_last_punch() -> Punch: 
    con = sqlite3.connect(f'{DATABASE}')
    res = con.cursor().execute(_sql_script(SQL['LAST_PUNCH'])).fetchone()
    con.close()

    if res is None:
        return Punch("", "", id=-1 )

    return Punch(res[1], res[3], time_stamp=res[2], id=res[0])



def _sql_script(file_path: str) -> str:
    """sql script
    Reads in the given .sql file

    Returns: sql_stript string
    """
    with open(file_path, 'r') as file:
        script = file.read()
    return script


def create_tables():
    conn = sqlite3.connect(f'{DATABASE}')
    cur = conn.cursor()

    cur.execute(_sql_script(SQL['create_punch_table']))
    cur.execute(_sql_script(SQL['create_entry_table']))

