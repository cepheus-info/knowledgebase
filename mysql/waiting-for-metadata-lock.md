# Waiting for metadata lock

## 1. Symptoms

When altering a table, it stuck in Server Monitor showing `waiting for meta data lock` forever. Could not find any other blocking query executing easily.

## 2. Solution

1. Check Active Transaction

Execute below query to get active transaction

```sql
show engine innodb status;
```

Search for `ACTIVE` keyword in below results and get the Transaction Id.

```text
---TRANSACTION 14568646884, `ACTIVE` 15503 sec
9 lock struct(s), heap size 8400, 6135 row lock(s), undo log entries 3
MySQL thread id 398628, OS thread handle 140178971621120, query id 1744610659 192.168.3.231 root
TABLE LOCK table `yb_smso_attachment_service`.`data_attachment_execute` trx id 14568646884 lock mode IS
TABLE LOCK table `yb_smso_attachment_service`.`data_attachment_execute` trx id 14568646884 lock mode IX
RECORD LOCKS space id 31916 page no 119616 n bits 248 index idx_id of table `yb_smso_attachment_service`.`data_attachment_execute` trx id 14568646884 lock_mode X
Record lock, heap no 178 PHYSICAL RECORD: n_fields 2; compact format; info bits 32
 0: len 30; hex 65613435356134372d623134642d343232632d396239332d336564383938; asc ea455a47-b14d-422c-9b93-3ed898; (total 36 bytes);
 1: len 8; hex 800000000045c10e; asc      E  ;;
```

2. Check the Transaction in `information_schema.INNODB_TRX` table

Use below query to check details and get the INNODB_TRX.trx_mysql_thread_id column as well.

```sql
select * from information_schema.INNODB_TRX where INNODB_TRX.trx_id = '14568646884';
```

3. Kill the long running transaction

```sql
kill your_thread_id
```
