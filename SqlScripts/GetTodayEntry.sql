SELECT *
FROM entry
WHERE entry_date == (SELECT date('now', 'localtime'));
