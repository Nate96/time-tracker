-- Gets all entries where the punch in date is greater that the most recent past
-- monday
SELECT *
FROM entry
WHERE in_punch BETWEEN
   STRFTIME('%Y-%m-%d', 'now', '-6 days', 'weekday 0', 'localtime') -- Start of Week (Monday)
   AND STRFTIME('%Y-%m-%d', 'now', 'weekday 0', 'localtime')        -- End of Week (Sunday)
