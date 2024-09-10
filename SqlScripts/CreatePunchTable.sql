CREATE TABLE IF NOT EXISTS  punch(
   id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
   , type TEXT NOT NULL CHECK(type IN ('out', 'in'))
   , punch_date DATETIME NOT NULL
   , comment TEXT NOT NULL
);