# Lookup field using mongodb

## Process

```js
db.users.aggregate([
  {
    $lookup: {
      from: "others",
      localField: "_id",
      foreignField: "userId",
      as: "others",
    },
  },
  { $unwind: "$others" },
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
