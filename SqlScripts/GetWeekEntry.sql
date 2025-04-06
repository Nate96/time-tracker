-- CAST((CAST(strftime('%w', 'now') as INT) + 6) % 7 as TEXT)
-- ~ ({current weekday} + 6) % 7
-- ~ DATE('now', "- {({current weekday} + 6) % 7} days")
--
-- Gets all entries where the punch in date is greater that the most recent past
-- monday
SELECT *
FROM entry
WHERE DATE(in_punch) >= DATE('now', '-' || CAST((CAST(strftime('%w', 'now') as INT) + 6) % 7 as TEXT) || " days");
