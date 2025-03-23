SELECT ROUND(SUM(total_time), 2)
FROM entry
WHERE DATE(in_punch) == DATE('now', 'localtime');
