SELECT *
FROM entry
WHERE in_punch >= DATETIME('2024-08-13', 'weekday 1', '-7 days');
