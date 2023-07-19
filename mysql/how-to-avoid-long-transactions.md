# How to avoid long transactions?

Long transactions are bad for database performance. They can cause lock contention, increase the chance of deadlocks, and make the database slow.

## Example

Let's say we have a table `users` with 100,000 rows. We want to update the `name` column of all rows. We can do it in two ways:

1. Update all rows in one transaction

   ```sql
   START TRANSACTION;
   UPDATE users SET name = 'John';
   COMMIT;
   ```

2. Update 1,000 rows in one transaction

   ```sql
   START TRANSACTION;
   UPDATE users SET name = 'John' LIMIT 1000;
   COMMIT;
   ```
