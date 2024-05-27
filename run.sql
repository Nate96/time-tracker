SELECT * 
FROM entry
WHERE entry_date == (SELECT date("now", "localtime"));

-- sqlite3 log.db < run.sql > results.txt
