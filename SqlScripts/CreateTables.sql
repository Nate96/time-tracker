CREATE TABLE IF NOT EXISTS  punch(
   id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
   , type TEXT NOT NULL CHECK(type IN ('out', 'in'))
   , punch_date DATETIME NOT NULL
   , comment TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS entry(
   id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
   , in_punch DATETIME NOT NULL
   , out_punch DATETIME NOT NULL
   , total_time FLOAT NOT NULL
   , task_name TEXT NOT NULL
   , task_comment TEXT NOT NULL
);
