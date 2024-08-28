import sqlite3
import os


class Repository:
    scripts = {
            'DATABASE_LOCATION':  "Data Source=../Test/Log.db",
            'CREATE_TABLE     ':  "../SqlScripts/CreateTables.sql",
            'LAST_PUNCH       ':  "../SqlScripts/GetLastPunch.sql",
            'INSERT_PUNCH     ':  "../SqlScripts/InsertPunch.sql",
            'INSERT_ENTRY     ':  "../SqlScripts/InsertEntry.sql",
            'TODAY            ':  "../SqlScripts/GetTodayEntry.sql",
            'WEEK             ':  "../SqlScripts/GetWeekEntry.sql",
            'MONTH            ':  "../SqlScripts/GetMonthEntry.sql",
            'LAST_ENTRY       ':  "../SqlScripts/GetLastEntry.sql",
            }

    def __init__(self):
        CON = sqlite3.connect(self.scripts['DATABASE_LOCATION'])
        CUR = CON.cursor()
        CUR.execute(os.read(self.scripts['CREATE_TABLE']))

    def add_punch(self, punch_type, punch_datetime, comment):
        CON = sqlite3.connect(self.scripts['DATABASE_LOCATION'])
        CUR = CON.cursor()

        CUR.execute(self.scripts['INSERT_PUNCH'],
                    {
                        punch_type,
                        punch_datetime,
                        comment
                     })
        CON.commit()

    def add_entry(self):
        CON = sqlite3.connect(self.scripts['DATABASE_LOCATION'])
        CUR = CON.cursor()
        CUR.execute(self.scripts['INSERT_ENTRY'])
        CON.commit()

    def get_entries(self, duration):
        CON = sqlite3.connect(self.scripts['DATABASE_LOCATION'])
        CUR = CON.cursor()

        if duration == "day":
            return CUR.execute(self.scripts['TODAY'])
        elif duration == "week":
            return CUR.execute(self.scripts['WEEK'])
        elif duration == "month":
            return CUR.execute(self.scripts['MONTH'])
        elif duration == "last":
            return CUR.execute(self.scripts['LAST_ENTRY'])

    def get_last_punch(self):
        CON = sqlite3.connect(self.scripts['DATABASE_LOCATION'])
        CUR = CON.cursor()
        return CUR.execute(self.scripts['LAST_PUNCH'])
