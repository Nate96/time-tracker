INSERT INTO entry (in_punch, out_punch, total_time, task_name, task_comment)
VALUES (
      DATETIME('now', 'localtime'),
      DATETIME('now', 'localtime'),
      $duration,
      'Lunch',
      'Lunch break'
);
