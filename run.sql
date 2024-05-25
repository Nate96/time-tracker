SELECT * 
FROM entry
WHERE (SELECT date("now")) > (SELECT date("now", "-7 days"));

-- sqlite3 log.db < run.sql > results.txt
