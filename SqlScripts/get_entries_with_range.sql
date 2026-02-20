SELECT *
FROM Entry
WHERE DATE(in_punch) BETWEEN DATE($start) AND DATE($end);
