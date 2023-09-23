import sqlite3
CON = sqlite3.connect('Log.db')
CUR = CON.cursor()


def create_entry(time_in, time_out, comment, total_time):
    '''Create Entry
    Adds an Entry to the entry table
    '''
    _create_entry_table()
    CUR.execute('SELECT Date()')
    todays_date = CUR.fetchone()[0]

    CUR.execute('INSERT INTO entry(date, timeIn, timeOut, TotalTime, comment) values(?, ?, ?, ?, ?)', (todays_date, time_in, time_out, total_time, comment))
    CON.commit()


def execute_query(query):
    '''Execute Query
    Executes the given query
    '''
    print('executing query')
    for row in CUR.execute(query):
        print(row)


def get_todays_entries():
    '''Get Todays Entires
    Prints rows where the date is equal to the current date
    '''
    res = CUR.execute('''
                      SELECT * FROM entry
                      WHERE date = (SELECT Date())
                      ''')
    for row in res:
        print(row)


def get_hours_worked_today():
    CUR.execute('''
                    SELECT SUM(TotalTime) FROM entry
                    WHERE date = (SELECT Date())
                ''')
    print("Total hours worked today:", CUR.fetchone())


def _create_entry_table():
    '''Create Table
    Checks if the entry table has been created.
    If the entry table has not been created, create the table
    NOTE: checks if only 1 table is in the database
    '''
    res = CUR.execute('SELECT name FROM sqlite_master')
    if res.fetchone() is None:
        CUR.execute('CREATE TABLE entry(date, timeIn, timeOut, TotalTime, comment)')
