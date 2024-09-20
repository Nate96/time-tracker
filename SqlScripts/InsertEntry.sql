WITH last_two_punches AS (
   SELECT punch_date, comment
   FROM punch
   ORDER BY punch_date DESC 
   LIMIT 2
)
INSERT INTO  entry (in_punch, out_punch, total_time, task_name, task_comment)
SELECT 
   MIN(punch_date)
   , MAX(punch_date)
   , ROUND(((julianday(MAX(punch_date)) - julianday(MIN(punch_date))) * 24), 2)
   , (SELECT comment FROM last_two_punches ORDER BY punch_date ASC LIMIT 1)
   , (SELECT comment FROM last_two_punches LIMIT 1)
FROM last_two_punches;
