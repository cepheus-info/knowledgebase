# What is deadlock?

Deadlock is a situation where two or more transactions are waiting for each other to give up locks. In this situation, the waiting transactions will never finish and the database will be stuck.

## Example

Let's say we have two transactions, `A` and `B`, and two rows, `X` and `Y`. Transaction `A` locks row `X` and transaction `B` locks row `Y`. Then, transaction `A` tries to lock row `Y` and transaction `B` tries to lock row `X`. Now, both transactions are waiting for each other to give up locks. This is a deadlock.

## How to avoid deadlock

### 1. Code level

- Avoid long transactions

- Avoid transactions that lock many rows

- Avoid transactions that lock rows in different order

- Use `SELECT ... FOR UPDATE` to lock rows in advance

### 2. Database level

- Use `innodb_lock_wait_timeout` to set the maximum time a transaction can wait for a lock

- Adjust index to reduce the number of rows locked

- Database deadlock detection and restart

### 3. Application level

- Retry the transaction when deadlock happens
