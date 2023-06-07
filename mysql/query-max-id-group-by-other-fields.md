# Query max id group by other fields

```sql
SELECT MAX(id) FROM table GROUP BY field1, field2, field3;
```

## Example

We can use subquery to get the max id of each group.

```sql
SELECT * FROM table WHERE id IN (
    SELECT MAX(id) FROM table GROUP BY field1, field2, field3
);
```

Use in clause is not efficient, we can use join to get the same result.

```sql
SELECT t1.* FROM table t1
JOIN (
    SELECT MAX(id) AS id FROM table GROUP BY field1, field2, field3
) t2 ON t1.id = t2.id;
```

We can use `HAVING` to get the same result in mysql with only one query.

```sql
SELECT * FROM table GROUP BY field1, field2, field3 HAVING id = MAX(id);
```

Above query is not standard sql, it will not work in other database like postgresql.

We can use `EXISTS` to get the same result in standard sql.

```sql
SELECT * FROM table t1 WHERE NOT EXISTS (
    SELECT 1 FROM table t2
    WHERE t1.field1 = t2.field1 AND t1.field2 = t2.field2 AND t1.field3 = t2.field3 AND t1.id < t2.id
);
```