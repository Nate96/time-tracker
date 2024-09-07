from datetime import datetime, timedelta, time
import repository
import json
import os
import logging

# TODO: Turn repository into class
# TODO: Implement "cli" class in tt.py file.
# TODO: test
REPO = repository
MESSAGES = json.load(open("../Messages/CommandErrors.json"))
logger = logging.getLogger(__name__)


def punch_in(comment):
    def _valid_state():
        last_punch = REPO.get_last_punch()
        if last_punch is None:
            logger.error(MESSAGES['NO_PUNCHES'])
            return False
        elif last_punch[1] == "out":
            return True
        elif last_punch:
            logger.error(MESSAGES['PUNCHIN_INVALID'])
            return False

    if _valid_state():
        timestamp = os.time()
        REPO.add_punch("in", timestamp, comment)

        if timestamp == REPO.get_last_punch()[2]:
            return MESSAGES['PUNCHIN_SUCCESS']
        else:
            logger.error(MESSAGES['PUNCH_FAIL'])
            return MESSAGES['REFER_LOG']


def punch_out(comment):
    def _valid_state():
        last_punch = REPO.get_last_punch()
        if last_punch is None:
            logger.error(MESSAGES['NO_PUNCHES'])
            return False
        elif last_punch[1] == "in":
            return True
        elif last_punch:
            logger.error(MESSAGES['PUNCHOUT_INVALID'])
            return False

    if _valid_state():
        timestamp = os.time()
        REPO.add_punch("out", timestamp, comment)

        if timestamp == REPO.get_last_punch()[2]:
            logger.info(MESSAGES['PUNCHOUT_SUCCESS'])
            REPO.add_entry()
            logger.info(MESSAGES['PUNCHOUT_SUCCESS'])

        else:
            logger.error(MESSAGES['PUNCH_FAIL'])
            return MESSAGES['REFER_LOG']

    if _valid_state():
        REPO.add_punch("out", os.time(), comment)
        REPO.add_entry()


def status():
    last_punch = REPO.get_last_punch()[0]
    day_entries = REPO.get_entries("day")
    week_entries = REPO.get_entries("week")
    punch_in_time = datetime.time('now') - last_punch.punch_time

    if last_punch.punch_type == "in":
        print(f'Punched in for: {round(punch_in_time, 2)} hours\n')
        print(last_punch)
        print(f'Day:  {day_entries} hours')
        print(f'Week: {week_entries} hours')
    elif last_punch.punch_type == "out":
        print(REPO.get_entries("last"))
        print(f'Day:  {day_entries} hours')
        print(f'Week: {week_entries} hours')


def show_entrie(duration):
    '''Show Entires:
    Show Entries for the given Duration in the following format
    Entry{}

    Total Hours: {}
    '''
    entries = REPO.get_entries(duration)

    # print Entry
    # print toal time


def report(duration):
    '''Report
    Show stats of the given week in the following format
    Monday:     {} hours
    Tuesday:    {} hours
    Wednesday:  {} hours
    Thursday:   {} hours
    Friday:     {} hours
    Saturday:   {} hours
    Sunday:     {} hours
    ---------------------
    Total:      {} hours
    '''
