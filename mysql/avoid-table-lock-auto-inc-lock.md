# Avoid table lock auto inc lock

## Overview

When using auto increment key, the insert operation will lock the table, and the lock will be released after the statement is executed. If the table is frequently inserted, the table will be locked frequently, and the performance will be very bad.

## Solution

We have a global variable named `innodb_autoinc_lock_mode` to control the auto increment lock mode.

```sql
-- The auto increment lock mode needs to be 2, which will not lock the table when inserting
show global VARIABLES like 'innodb_autoinc_lock_mode';
```

It helps when the number of rows inserting couldnot be determined in advance. Such as `INSERT INTO ... SELECT ... FROM ... statement`.

> Note: The `innodb_autoinc_lock_mode=2` is recommended only if `BINLOG_FORMAT` is set to `ROW`.

## Steps

1. Set `innodb_autoinc_lock_mode=2` in `my.cnf` file.

   ```ini
   [mysqld]
   innodb_autoinc_lock_mode=2
   ```

2. Restart MySQL service.

   ```bash
   systemctl restart mysqld
   ```

3. Check the variable value.

   ```sql
   show global VARIABLES like 'innodb_autoinc_lock_mode';
   ```

## Reference
