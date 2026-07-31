import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

ROOT:     str | None = os.getenv("ROOT")
DATABASE: str | None = os.getenv("DATABASE")

class Res(Enum):
    NO_DB           = 0
    SEC_IN          = 1
    IN              = 2
    OUT             = 3
    NO_PUNCH        = 4
    DB_ERROR        = 5
    SEC_OUT         = 6
    INVALID_COMMAND = 7

MESSAGES = {
        Res.SEC_IN:          "Seccessfully punched in",
        Res.IN:              "Already Punched in",
        Res.SEC_OUT:         "Seccessfully punched out",
        Res.OUT:             "Already Punched out",
        Res.NO_PUNCH:        "No punches",
        Res.INVALID_COMMAND: "Invlaid command, please refer to the REAMD.md",
        Res.NO_DB:           "No Database, please define DATABASE in .env",
        # "PUNCHOUT_SUCCESS": "Seccessfully punched out",
        # "ENTRY_SUCCESS":    "Seccessfully added Entry",
        # "ENTRY_FAIL":       "Entry was NOT added",
        # "INVALID_INPUT":    "In-vaild input. Refer to index.md in the 'How to Use' section",
        # "INVALID_DURATION": "In-valid duration please referr to index.md",
        # "NO_ENTRIES":       "There is no entries",
        # "INVALID_STATE":    "Database is NOT in the correct state to perfome action",
        # "NO_PUNCHES":       "There are no punches",
        # "PUNCH_FAIL":       "Punch was not added correctly",
        # "REFER_LOG":        "An Error as accourd, please refer to tt.log",
        }

TRACKER = {
        "ACTIVE":              True,
        "MAX_WORK_WEEK_HOURS": 40,
        "MAX_WORK_WEEK_DAYS":  5,
        "HOURS_PER_DAY":       8
        }

SQL = {
        'create_punch_table': ROOT + "/SqlScripts/CreatePunchTable.sql",
        'create_entry_table': ROOT + "/SqlScripts/CreateEntryTable.sql",
        'LAST_PUNCH':         ROOT + "/SqlScripts/GetLastPunch.sql",
        'INSERT_PUNCH':       ROOT + "/SqlScripts/InsertPunch.sql",
        'INSERT_ENTRY':       ROOT + "/SqlScripts/InsertEntry.sql",
        'TODAY':              ROOT + "/SqlScripts/GetTodayEntry.sql",
        'WEEK':               ROOT + "/SqlScripts/GetWeekEntry.sql",
        'MONTH':              ROOT + "/SqlScripts/GetMonthEntry.sql",
        'LAST_ENTRY':         ROOT + "/SqlScripts/GetLastEntry.sql",
        'SHOW_ENTRIES':       ROOT + "/SqlScripts/ShowEntries.sql",
        'GET_ENTRIES':        ROOT + "/SqlScripts/get_entries_with_range.sql",
        'GET_BY_TASK_NAME':   ROOT + "/SqlScripts/GetEntriesByTaskName.sql"

}


class PunchType(Enum):
    OUT = "out"
    IN  = "in"

