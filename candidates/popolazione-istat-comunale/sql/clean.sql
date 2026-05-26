-- Clean SQL for popolazione-istat-comunale
SELECT
  comune_id,
  anno,
  popolazione
FROM clean_input
WHERE anno = {{year}};