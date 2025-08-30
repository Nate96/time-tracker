from dotenv import load_dotenv
import os

load_dotenv() # This loads the variables from .env into os.environ

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
