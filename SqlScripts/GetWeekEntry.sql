SELECT *
FROM entry
WHERE in_punch >= DATETIME(DATE('now'), 'weekday 1', '-7 days');
