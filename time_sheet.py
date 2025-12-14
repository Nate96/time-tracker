# ISSUE: Create Table sql script has two commands and python
#        does not support this.

from config import DATABASE, SQL
from datetime import datetime, date, timedelta

import sqlite3

INPUT_FORMAT = "%Y-%m-%d %H:%M:%S"

class Punch():
    def __init__(self, 
                 punch_type: str,
                 comment: str,
                 time_stamp=datetime.now().strftime(INPUT_FORMAT),
                 id=0):
        self.id         = id
        self.type       = punch_type
        self.time_stamp = time_stamp
        self.comment    = comment


class Entry():
    def __init__(self,
                 id: int,
                 total_time: float,
                 title: str,
                 comment: str,
                 in_punch=datetime.now().strftime(INPUT_FORMAT),
                 out_punch=datetime.now().strftime(INPUT_FORMAT)):
        self.id         = id
        self.total_time = total_time
        self.title      = title
        self.comment    = comment
        self.in_punch   = in_punch
        self.out_punch  = out_punch


def add_punch(punch: Punch) -> None: 
    create_tables()

    con = sqlite3.connect(f'{DATABASE}')
    con.cursor().execute(_sql_script(SQL['INSERT_PUNCH']),
                         (
                              punch.type,
                              punch.comment
                          ))
    con.commit()
    con.close()


def add_entry() -> Entry: 
    create_tables()

    con = sqlite3.connect(f'{DATABASE}')
    con.cursor().execute(_sql_script(SQL['INSERT_ENTRY']))

    res = con.cursor().execute(_sql_script(SQL['LAST_ENTRY'])).fetchone()

    con.commit()
    con.close()

    return Entry(res[0], res[1], res[2], res[3], res[4], res[5])


def get_last_entry() -> Entry:
    create_tables()
    con = sqlite3.connect(f'{DATABASE}')
    res = con.cursor().execute(_sql_script(SQL['LAST_ENTRY'])).fetchone()

    if res:
        return Entry(res[0], res[3], res[4], res[5], res[1], res[2])
    else:
        return Entry(-1, 0.0, "", "")
            

def get_entries(duration: str) -> list[Entry]:
    create_tables()

    con = sqlite3.connect(f'{DATABASE}')
    cur = con.cursor()

    if duration == "day":
        res = cur.execute(_sql_script(SQL['TODAY'])).fetchall()
    elif duration == "week":
        start, end = _get_current_week_date_range()
        res = cur.execute(f"""
                          SELECT *
                          FROM Entry
                          WHERE DATE(in_punch) BETWEEN DATE('{end}') AND DATE('{start}');
                          """
                ).fetchall()
    elif duration == "last":
        start, end = _get_last_week_date_range()
        print(start, end)
        res = cur.execute(f"""
                          SELECT *
                          FROM Entry
                          WHERE DATE(in_punch) BETWEEN DATE('{start}') AND DATE('{end}');
                          """
                ).fetchall()
    elif duration == "month":
        res = cur.execute(_sql_script(SQL['MONTH'])).fetchall()
    elif duration == "all":
        res = cur.execute("SELECT * FROM Entry;").fetchall()
    else:
        con.close()
        return []

    entries: list[Entry] = []

    for item in res:
        entries.append(Entry(
            id = item[0],
            in_punch=item[1],
            out_punch=item[2],
            total_time=item[3],
            title=item[4],
            comment=item[5]))

    con.close()
    return entries


def get_last_punch() -> Punch: 
    create_tables()

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

    conn.commit()
    conn.close()

def _get_current_week_date_range() -> tuple[date, date]:
    today = date.today()
    day_of_week_sunday_0 = (today.weekday() + 1) % 7
    start_of_week = today - timedelta(days=day_of_week_sunday_0)

    return (today, start_of_week)

def _get_last_week_date_range() -> tuple[date, date]:
    today = date.today()
    day_of_week_sunday_0 = (today.weekday() + 1) % 7
    start_of_this_week = today - timedelta(days=day_of_week_sunday_0)
    start_of_last_week = start_of_this_week - timedelta(days=7)
    end_of_last_week = start_of_this_week - timedelta(days=1)

    return (start_of_last_week, end_of_last_week)
