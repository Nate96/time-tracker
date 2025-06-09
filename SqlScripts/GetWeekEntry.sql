-- Gets all entries where the punch in date is greater that the most recent past
-- monday
SELECT *
FROM entry
WHERE DATE(in_punch) >= DATE('%Y-%m-%d', 'now', '-7 days', 'weekday 1');
