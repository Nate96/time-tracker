from dotenv import load_dotenv
from enum import Enum

import os

load_dotenv() 

DATABASE = os.getenv("DATABASE")

MESSAGES = {
        "ENTRY_SUCCESS":    "Seccessfully added Entry",
        "ENTRY_FAIL":       "Entry was NOT added",
        "INVALID_INPUT":    "In-vaild input. Refer to index.md in the 'How to Use' section",
        "INVALID_DURATION": "In-valid duration please referr to index.md",
        "PUNCHIN_SUCCESS":  "Seccessfully punched in",
        "PUNCHOUT_SUCCESS": "Seccessfully punched out",
        "PUNCHIN_INVALID":  "Already Punched in",
        "PUNCHOUT_INVALID": "Already Punched out",
        "NO_ENTRIES":       "There is no entries",
        "INVALID_STATE":    "Database is NOT in the correct state to perfome action",
        "NO_PUNCHES":       "There are no punches",
        "PUNCH_FAIL":       "Punch was not added correctly",
        "REFER_LOG":        "An Error as accourd, please refer to tt.log",
        "INVALID_COMMAND":   "Invlaid command, please refer to REAMD.md",
        }

TRACKER = {
        "ACTIVE":               False,
        "MAX_WORK_WEEK_HOURS":  0,
        "MAX_WORK_WEEK_DAYS":   0,
        "HOURS_PER_DAY":        0
        }

SQL = {
        'create_punch_table': "./SqlScripts/CreatePunchTable.sql",
        'create_entry_table': "./SqlScripts/CreateEntryTable.sql",
        'LAST_PUNCH':         "./SqlScripts/GetLastPunch.sql",
        'INSERT_PUNCH':  "./SqlScripts/InsertPunch.sql",
        'INSERT_ENTRY':  "./SqlScripts/InsertEntry.sql",
        'TODAY':  "./SqlScripts/GetTodayEntry.sql",
        'WEEK':  "./SqlScripts/GetWeekEntry.sql",
        'MONTH':  "./SqlScripts/GetMonthEntry.sql",
        'LAST_ENTRY':  "./SqlScripts/GetLastEntry.sql",
}

class PunchType(Enum):
    OUT = "out"
    IN  = "in"
