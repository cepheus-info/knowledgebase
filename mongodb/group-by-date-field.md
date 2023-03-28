# Group by date field

## Overview

We need to use $dateToString to format a date field to specified one.

## Process

There's a chance we could encounter an error that Cannot convert BSON type String to Date when we use $dateToString operator. This might due to some records' field type mismatch.

We can use below $match operator to exclude those records' $type is not DateTime.

```js
db.users.aggregate([
  { $match: { "others.registerTime": { $type: 9 } } },
  //{ $unwind: "$others" },
  {
    $group: {
      _id: {
        $dateToString: { format: "%Y-%m-%d", date: "$others.registerTime" },
      },
      //				_id: "$others.registerTime",
      count: {
        $sum: 1,
      },
    },
  },
  { $sort: { _id: 1 } },
]);
```

## How to calculate maxValue - minValue?

```js
db.logs.aggregate([
  {
    $match: {
      date: { $gte: new Date("2022-12-01"), $lte: new Date("2023-01-01") },
    },
  },
  { $sort: { date: 1 } },
  {
    $group: {
      _id: {
        date: { $dateToString: { format: "%Y-%m-%d", date: "$date" } },
        userId: "$userId",
      },
      maxDate: {
        $max: "$date",
      },
      minDate: {
        $min: "$date",
      },
      operationCount: {
        $sum: 1,
      },
    },
  },
  { $addFields: { aliveMS: { $subtract: ["$maxDate", "$minDate"] } } },
  {
    $project: {
      date: "$_id.date",
      userId: "$_id.userId",
      earliest: "$minDate",
      latest: "$maxDate",
      aliveMS: "$aliveMS",
      aliveMinutes: { $ceil: { $divide: ["$aliveMS", 1000 * 60] } },
      operationCount: "$operationCount",
    },
  },
  //{ $sort: { date: 1 } },
]);
```
