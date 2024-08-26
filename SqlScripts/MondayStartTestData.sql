.mode column
DROP TABLE entry;

CREATE TABLE IF NOT EXISTS entry(
   id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
   , in_punch DATETIME NOT NULL
   , out_punch DATETIME NOT NULL
   , total_time FLOAT NOT NULL
   , task_name TEXT NOT NULL
   , task_comment TEXT NOT NULL
);

INSERT INTO entry(in_punch, out_punch, total_time, task_name, task_comment) VALUES("2024-08-13 21:46:32", "2024-08-13 21:46:32", 1.23, "Pickles", "oh yeah parona gun");
INSERT INTO entry(in_punch, out_punch, total_time, task_name, task_comment) VALUES("2024-08-12 21:46:32", "2024-08-13 21:46:32", 1.23, "Pickles", "oh yeah parona gun");
INSERT INTO entry(in_punch, out_punch, total_time, task_name, task_comment) VALUES("2024-08-11 21:46:32", "2024-08-13 21:46:32", 1.23, "Pickles", "oh yeah parona gun");
INSERT INTO entry(in_punch, out_punch, total_time, task_name, task_comment) VALUES("2024-08-10 21:46:32", "2024-08-13 21:46:32", 1.23, "Pickles", "oh yeah parona gun");

SELECT *
FROM entry
WHERE Date(in_punch) >= DATE('2024-08-13', 'weekday 1', '-7 days');
