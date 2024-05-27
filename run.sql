--SELECT * 
--FROM entry
--WHERE entry_date == (SELECT date("now", "localtime"));

SELECT * 
FROM entry
WHERE entry_date > (SELECT date('now', 'localtime', '-1 days'));

--SELECT date("now");
--
--SELECT '2024-05-18 ', date('2024-05-18', 'localtime', 'weekday 1', "-7 days");
--SELECT '2024-05-19 ', date('2024-05-19', 'localtime', 'weekday 1', "-7 days");
--SELECT '2024-05-20 ', date('2024-05-20', 'localtime', 'weekday 1', "-7 days");
--SELECT '2024-05-21 ', date('2024-05-21', 'localtime', 'weekday 1', "-7 days");
--SELECT '2024-05-22 ', date('2024-05-22', 'localtime', 'weekday 1', "-7 days");
--SELECT '2024-05-23 ', date('2024-05-23', 'localtime', 'weekday 1', "-7 days");
--SELECT '2024-05-24 ', date('2024-05-24', 'localtime', 'weekday 1', "-7 days");
--SELECT '2024-05-25 ', date('2024-05-25', 'localtime', 'weekday 1', "-7 days");
--SELECT '2024-05-26 ', date('2024-05-26', 'localtime', 'weekday 1', "-7 days");
--SELECT '2024-05-27 ', date('2024-05-26', 'localtime', 'weekday 1', "-7 days");
--SELECT '2024-05-28 ', date('2024-05-27', 'localtime', 'weekday 1', "-7 days");
--SELECT '2024-05-28 ', date('2024-05-28', 'localtime', 'weekday 1', "-7 days");
--
--SELECT '2024-05-18 just week day 1 ', date('2024-05-18', 'localtime', 'weekday 1');
--SELECT '2024-05-19 just week day 1 ', date('2024-05-19', 'localtime', 'weekday 1');
--SELECT '2024-05-20 just week day 1 ', date('2024-05-20', 'localtime', 'weekday 1');
--SELECT '2024-05-21 just week day 1 ', date('2024-05-21', 'localtime', 'weekday 1');
--SELECT '2024-05-22 just week day 1 ', date('2024-05-22', 'localtime', 'weekday 1');
--SELECT '2024-05-23 just week day 1 ', date('2024-05-23', 'localtime', 'weekday 1');
--SELECT '2024-05-24 just week day 1 ', date('2024-05-24', 'localtime', 'weekday 1');
--SELECT '2024-05-25 just week day 1 ', date('2024-05-25', 'localtime', 'weekday 1');
--SELECT '2024-05-26 just week day 1 ', date('2024-05-26', 'localtime', 'weekday 1');
--SELECT '2024-05-27 just week day 1 ', date('2024-05-27', 'localtime', 'weekday 1');
--SELECT '2024-05-28 just week day 1 ', date('2024-05-28', 'localtime', 'weekday 1');
--SELECT '2024-05-29 just week day 1 ', date('2024-05-29', 'localtime', 'weekday 1');
--
-- sqlite3 log.db < run.sql > results.txt
