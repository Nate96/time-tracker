SELECT * 
FROM entry
WHERE in_punch >= DATE('now', 'localtime', '-' || strftime('%w', 'now') || ' days');
