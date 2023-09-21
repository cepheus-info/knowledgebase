# Remove duplicated rows by a key

```sql
-- Remove duplicated rows by a key
-- https://stackoverflow.com/questions/3777633/delete-duplicate-rows-in-mysql
DELETE t1 FROM table_name t1
INNER JOIN table_name t2
WHERE t1.id < t2.id
AND t1.key = t2.key;
```
