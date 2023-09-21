# Change Primary Key Field to Another Datatype

## Overview

In this article, we will learn how to change the datatype of a primary key field in MySQL.

## Walkthrough

### Case 1: Changing the datatype of a primary key field to a larger compatible datatype

Let's say we have a table named `users` with the following schema:

```sql
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

We want to change the datatype of the `id` field from `int(11)` to `bigint(20)`.

```sql
-- we will first need to drop the primary key constraint on the `id` field
ALTER TABLE `users` DROP PRIMARY KEY;

-- Then, we can change the datatype of the `id` field:
ALTER TABLE `users` CHANGE `id` `id` BIGINT(20) NOT NULL AUTO_INCREMENT;

-- Finally, we can add the primary key constraint back to the `id` field:
ALTER TABLE `users` ADD PRIMARY KEY (`id`);
```

### Case 2: Changing the datatype of a primary key field to a different datatype

Let's say we have a table named `users` with the following schema:

```sql
CREATE TABLE `users` (
  `id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

We want to change the datatype of the `id` field from `varchar(255)` to `int(11) AUTO_INCREMENT`.

To do this, we will need to patch the data in the `id` field to be compatible with the new datatype. This can be done by creating a new field as a temporary placeholder for the data in the `id` field, patching the data in the new field, dropping the `id` field, and then renaming the new field to `id`.

```sql
-- First, we will drop the primary key constraint on the `id` field:
ALTER TABLE `users` DROP PRIMARY KEY;

-- Then, we will create a new field named `id_new`:
ALTER TABLE `users` ADD `id_new` INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;

-- Next, we will drop the `id` field:
ALTER TABLE `users` DROP `id`;

-- Finally, we will rename the `id_new` field to `id`:
ALTER TABLE `users` CHANGE `id_new` `id` INT(11) NOT NULL AUTO_INCREMENT;
```

### Case 3: Changing the primary key field to AUTO_INCREMENT

Let's say we have a table named `users` with the following schema:

```sql
CREATE TABLE `users` (
  `id` bigint NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

We want to change the `id` field to be an `AUTO_INCREMENT` field.

```sql
-- If the `id` field is already an `AUTO_INCREMENT` field, but with some natural id values, we will need another field to store the natural id values. Let's call this field `id_old`, and we will remove the `AUTO_INCREMENT` property from the `id` field first:
ALTER TABLE `users` MODIFY `id` BIGINT NOT NULL;
-- First, we will drop the primary key constraint on the `id` field:
ALTER TABLE `users` DROP PRIMARY KEY;
-- Then, we will add a new field named `id_new` as an `AUTO_INCREMENT` PRIMARY KEY field:
ALTER TABLE `users` ADD `id_new` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
-- Next, we will rename the `id` field to `id_old`:
ALTER TABLE `users` CHANGE `id` `id_old` BIGINT NOT NULL;
-- Finally, we will rename the `id_new` field to `id`:
ALTER TABLE `users` CHANGE `id_new` `id` BIGINT NOT NULL;
```

## Performance Tuning Case use AUTO_INCREMENT key

Let's say we have several tables using naturalIds as primary key, in a high concurrency environment, the insertion order is not the same as the naturalIds order, so the insertion will be blocked by the gap lock, and the performance will be very bad.

After considering the performance, we decide to use AUTO_INCREMENT key as primary key, but we have to keep the naturalIds for the business logic and reference the naturalIds as foreign key in other tables.

```sql
-- Patch uid_container
-- First, we will drop the primary key constraint on the `id` field:
ALTER TABLE `uid_container` DROP PRIMARY KEY;
-- Then, we will add a new field named `id_new` as an `AUTO_INCREMENT` PRIMARY KEY field:
ALTER TABLE `uid_container` ADD `id_new` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
-- Next, we will rename the `id` field to `id_old`:
ALTER TABLE `uid_container` CHANGE `id` `id_old` VARCHAR(255);
-- Finally, we will rename the `id_new` field to `id`:
ALTER TABLE `uid_container` CHANGE `id_new` `id` BIGINT NOT NULL;

-- Clear all the foreign keys in person_snapshot, person_snapshot_subsidy_record_item, person_snapshot_performance_detail_record_item

-- Patch person_snapshot
ALTER TABLE `person_snapshot` DROP PRIMARY KEY;
-- Then, we will add a new field named `id_new` as an `AUTO_INCREMENT` field:
ALTER TABLE person_snapshot ADD `id` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;

-- Patch person_snapshot_personnel_info
ALTER TABLE `person_snapshot_personnel_info` MODIFY `id` BIGINT NOT NULL;
-- First, we will drop the primary key constraint on the `id` field:
ALTER TABLE person_snapshot_personnel_info DROP PRIMARY KEY;
-- Then, we will add a new field named `id_new` as an `AUTO_INCREMENT` field:
ALTER TABLE person_snapshot_personnel_info ADD `id_new` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
-- Next, we will rename the `id` field to `id_old`:
ALTER TABLE `person_snapshot_personnel_info` CHANGE `id` `change_record_id` BIGINT NOT NULL;
-- Finally, we will rename the `id_new` field to `id`:
ALTER TABLE `person_snapshot_personnel_info` CHANGE `id_new` `id` BIGINT NOT NULL;

-- Patch person_snapshot_person_wages_info
ALTER TABLE `person_snapshot_person_wages_info` MODIFY `id` BIGINT NOT NULL;
-- First, we will drop the primary key constraint on the `id` field:
ALTER TABLE person_snapshot_person_wages_info DROP PRIMARY KEY;
-- Then, we will add a new field named `id_new` as an `AUTO_INCREMENT` field:
ALTER TABLE person_snapshot_person_wages_info ADD `id_new` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
-- Next, we will rename the `id` field to `id_old`:
ALTER TABLE `person_snapshot_person_wages_info` CHANGE `id` `change_record_id` BIGINT NOT NULL;
-- Finally, we will rename the `id_new` field to `id`:
ALTER TABLE `person_snapshot_person_wages_info` CHANGE `id_new` `id` BIGINT NOT NULL;

-- Patch person_snapshot_person_subsidy_record
ALTER TABLE `person_snapshot_person_subsidy_record` MODIFY `id` BIGINT NOT NULL;
-- First, we will drop the primary key constraint on the `id` field:
ALTER TABLE person_snapshot_person_subsidy_record DROP PRIMARY KEY;
-- Then, we will add a new field named `id_new` as an `AUTO_INCREMENT` field:
ALTER TABLE person_snapshot_person_subsidy_record ADD `id_new` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
-- Next, we will rename the `id` field to `id_old`:
ALTER TABLE `person_snapshot_person_subsidy_record` CHANGE `id` `change_record_id` BIGINT NOT NULL;
-- Finally, we will rename the `id_new` field to `id`:
ALTER TABLE `person_snapshot_person_subsidy_record` CHANGE `id_new` `id` BIGINT NOT NULL;

-- Patch person_snapshot_person_performance_detail_record
ALTER TABLE `person_snapshot_person_performance_detail_record` MODIFY `id` BIGINT NOT NULL;
-- First, we will drop the primary key constraint on the `id` field:
ALTER TABLE person_snapshot_person_performance_detail_record DROP PRIMARY KEY;
-- Then, we will add a new field named `id_new` as an `AUTO_INCREMENT` field:
ALTER TABLE person_snapshot_person_performance_detail_record ADD `id_new` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
-- Next, we will rename the `id` field to `id_old`:
ALTER TABLE `person_snapshot_person_performance_detail_record` CHANGE `id` `change_record_id` BIGINT NOT NULL;
-- Finally, we will rename the `id_new` field to `id`:
ALTER TABLE `person_snapshot_person_performance_detail_record` CHANGE `id_new` `id` BIGINT NOT NULL;

```

## Conclusion

In this article, we learned how to change the datatype of a primary key field in MySQL.
