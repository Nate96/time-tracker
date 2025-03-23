SELECT ROUND(SUM(total_time), 2)
FROM entry
WHERE DATE(in_punch) >= DATE('now', '-' || CAST((CAST(strftime('%w', 'now') as INT) + 6) % 7 as TEXT) || " days");
