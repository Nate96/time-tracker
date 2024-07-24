INSERT INTO punch(type, punch_date, comment)
VALUES($type, DATETIME('now', 'localtime'), $comment);
