SELECT * 
FROM entry
WHERE DATE(in_punch) >= DATE('now', 'localtime', '-' || strftime('%d', 'now') || ' days');
