from dotenv import load_dotenv
from enum import Enum

import os

load_dotenv() 

DATABASE = os.getenv("DATABASE")

class Res(Enum):
    NO_DB            = 0
    SEC_PUNCH_IN     = 1
    INVAIL_IN_PUNCH  = 2
    INVAIL_OUT_PUNCH = 3
    NO_PUNCH         = 4
    DB_ERROR         = 5
    SEC_PUNCH_OUT    = 6

MESSAGES = {
        # "NO_DB": "No Database Defined, please define DATABASE .env",
        # "PUNCHOUT_SUCCESS": "Seccessfully punched out",
        # "ENTRY_SUCCESS":    "Seccessfully added Entry",
        # "ENTRY_FAIL":       "Entry was NOT added",
        # "INVALID_INPUT":    "In-vaild input. Refer to index.md in the 'How to Use' section",
        # "INVALID_DURATION": "In-valid duration please referr to index.md",
        Res.SEC_PUNCH_IN:     "Seccessfully punched in",
        Res.INVAIL_IN_PUNCH:  "Already Punched in",
        Res.SEC_PUNCH_OUT:    "Seccessfully punched out",
        Res.INVAIL_OUT_PUNCH: "Already Punched out",
        # "NO_ENTRIES":       "There is no entries",
        # "INVALID_STATE":    "Database is NOT in the correct state to perfome action",
        # "NO_PUNCHES":       "There are no punches",
        # "PUNCH_FAIL":       "Punch was not added correctly",
        # "REFER_LOG":        "An Error as accourd, please refer to tt.log",
        # "INVALID_COMMAND":   "Invlaid command, please refer to REAMD.md",
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
    OUT     = "out"
    IN      = "in"

