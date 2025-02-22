# Use a Guess offset/timezone policy to format Timestamp

## 1. Overview

In Java, a Date object represents a specific instant in time with millisecond precision. However, when we want to display the date in Frontend, we not only need the `date` but also the `timezone`/`offset` to display the date correctly.

## 2. Walkthrough

### 2.1. Concepts

We can use a `Guess` policy to format the `Timestamp` in Frontend. The `Guess` policy is a heuristic approach to determine the timezone/offset of a given timestamp. It is not 100% accurate but can be useful in many cases.

### 2.2. Steps

1. Use the `Guess` policy to format the `Timestamp` in Frontend using date-fns library.

Basically the main users of current application is from GMT+08:00 timezone, so we can use `Guess` policy to format the `Timestamp` in Frontend.

> Normally we'll have a `UTC` timestamp stored in the database which represent a LocalDate with 00:00:00 as LocalTime. e.g., `2021-10-01T16:00:00Z` represents `2021-10-02 00:00:00` in GMT+08:00 timezone.

```javascript
import { format } from 'date-fns';

const date = new Date('2021-10-01T16:00:00Z'); // UTC timestamp
const formattedDate = format(date, 'yyyy-MM-dd HH:mm:ss', { timeZone: 'Asia/Shanghai' });
console.log(formattedDate); // 2021-10-02 00:00:00
```

However, there are ages the `timezone` was changed, so we can guess the Date using `offset` instead of `timezone` first. e.g., `1900-01-01 00:00:00` in Asia/Shanghai timezone is not `1900-01-01 00:00:00 GMT+08:00`.

```javascript
import { format } from 'date-fns';

const date = new Date('2021-10-01T16:00:00Z'); // UTC timestamp
// we first use an offset instead of a timezone
const formattedDate = format(date, 'yyyy-MM-dd HH:mm:ss', { timeZone: 'GMT+08:00' });
console.log(formattedDate); // 2021-10-02 00:00:00
```




