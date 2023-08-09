# Performance Issue

## 1. Backlog Item

| No. | Title                                                     | Type              | Dignostics                                          |
| --- | --------------------------------------------------------- | ----------------- | --------------------------------------------------- |
| 1   | data_attachment_execute deadlock                          | deadlock          | [dignostics](#21-data_attachment_execute-deadlock)  |
| 2   | update change_record status block                         | block             | [dignostics](#22-update-change_record-status-block) |
| 3   | concurrent requests to `put` change_record client aborted | api threads block | [dignostics](##23-)                                 |

## 2. Dignostics

### 2.1. data_attachment_execute deadlock

Refer to [DataAttachementExecute Deadlock](./dignostics/01.data_attachement_execute.deadlock.md) for details.

### 2.2. update change_record status block

Refer to [ChangeRecord Updating block](./dignostics/02.update_change_record.block.md) for details.

### 2.3. concurrent requests

[API threads block](./dignostics/03.concurrent_requests_to_long_transaction.md) for details.
