# Update Join

## update a fields with a lookup table

```js
db.fundAuditRecordDto.aggregate([
  {
    $lookup: {
      from: "approvalListDto",
      let: { fundMonth: "$fundMonth", organizationId: "$organizationId" },
      pipeline: [
        {
          $match: {
            $expr: {
              $and: [
                { $eq: ["$fundMonth", "$$fundMonth"] },
                { $eq: ["$organizationId", "$$organizationId"] },
              ],
            },
          },
        },
        { $project: { reportTime: "$fundAuditDto.declaraeTime", _id: 0 } },
      ],
      as: "approvalListDto",
    },
  },
  {
    $addFields: {
      reportTime: {
        $first: "$approvalListDto.reportTime",
      },
    },
  },
  {
    $project: {
      approvalListDto: 0,
    },
  },
  {
    $merge: {
      into: "fundAuditRecordDto",
      whenMatched: "replace",
      whenNotMatched: "discard",
    },
  },
]);
```
