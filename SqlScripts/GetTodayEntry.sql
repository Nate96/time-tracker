SELECT *
FROM entry
WHERE DATE(in_punch) == DATE('now', 'localtime');
