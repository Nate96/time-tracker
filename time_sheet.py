# ISSUE: Create Table sql script has two commands and python
#        does not support this.

from pydantic import BaseModel

from config import DATABASE, SQL, PunchType
from datetime import date, timedelta

import sqlite3

INPUT_FORMAT = "%Y-%m-%d %H:%M:%S"

class Punch(BaseModel):
    id:         int
    type:       PunchType
    time_stamp: str
    comment:    str


class Entry(BaseModel):
    id:         int
    in_punch:   str
    out_punch:  str
    total_time: float
    title:      str
    comment:    str


def add_punch(comment: str, punch_type: PunchType) -> Punch: 
    _create_tables()

    con = sqlite3.connect(f'{DATABASE}')
    con.cursor().execute(_sql_script(SQL['INSERT_PUNCH']),
                         (
                              punch_type.value,
                              comment
                          ))
    con.commit()
    con.close()

    return get_last_punch()


def punch_out(comment: str) -> Entry: 
    add_punch(comment, PunchType.OUT)

    con = sqlite3.connect(f'{DATABASE}')
    con.cursor().execute(_sql_script(SQL['INSERT_ENTRY']))
    con.commit()
    con.close()

    return get_last_entry()


def get_last_punch() -> Punch: 
    _create_tables()

    con = sqlite3.connect(f'{DATABASE}')
    res = con.cursor().execute(_sql_script(SQL['LAST_PUNCH'])).fetchone()
    con.close()

    if res is None:
        return Punch(id=-1, type=PunchType.OUT, time_stamp="", comment="")

    return Punch(id=res[0], type=res[1], time_stamp=res[2], comment=res[3])



def get_last_entry() -> Entry:
    _create_tables()

    con = sqlite3.connect(f'{DATABASE}')
    res = con.cursor().execute(_sql_script(SQL['LAST_ENTRY'])).fetchone()

    if res:
        return Entry(
                id=res[0],
                in_punch=res[1],
                out_punch=res[2],
                total_time=res[3],
                title=res[4],
                comment=res[5])
    else:
        return Entry(
                id=-1,
                in_punch="",
                out_punch="",
                total_time=0.0,
                title="",
                comment="")


def get_entries(duration: str) -> list[Entry]:
    _create_tables()

    con = sqlite3.connect(f'{DATABASE}')
    cur = con.cursor()

    if duration == "day":
        res = cur.execute(_sql_script(SQL['TODAY'])).fetchall()
    elif duration == "week":
        today, start_of_week = _get_week_date_range()
        res = cur.execute(_sql_script(SQL['GET_ENTRIES']), 
                          (
                              start_of_week,
                              today)
                          ).fetchall()
    elif duration == "last":
        return [get_last_entry()]
    elif duration == "month":
        res = cur.execute(_sql_script(SQL['MONTH'])).fetchall()
    elif duration == "all":
        res = cur.execute("SELECT * FROM Entry;").fetchall()
    elif duration == "last week":
        today, start_of_week = _get_week_date_range()
        res = cur.execute(_sql_script(SQL['GET_ENTRIES']), 
                          (
                              (str(start_of_week - timedelta(days=7))),
                              str(start_of_week))
                          ).fetchall()
    else:
        res = cur.execute(_sql_script(SQL['GET_BY_TASK_NAME']),
                    (duration,)
                ).fetchall()
        con.close()

    entries: list[Entry] = []

    for item in res:
        entries.append(Entry(
            id=item[0],
            in_punch=item[1],
            out_punch=item[2],
            total_time=item[3],
            title=item[4],
            comment=item[5]))

    con.close()
    return entries



def _sql_script(file_path: str) -> str:
    with open(file_path, 'r') as file:
        script = file.read()
    return script


def _create_tables():
    conn = sqlite3.connect(f'{DATABASE}')
    cur = conn.cursor()

    cur.execute(_sql_script(SQL['create_punch_table']))
    cur.execute(_sql_script(SQL['create_entry_table']))

    conn.commit()
    conn.close()

def _get_week_date_range(today = date.today()) -> tuple[date, date]:
    day_of_week_sunday_0 = (today.weekday() + 1) % 7
    start_of_week = today - timedelta(days=day_of_week_sunday_0)

    return (today, start_of_week)
