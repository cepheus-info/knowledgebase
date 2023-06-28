# filterRanges

```js
function countSignals(frequencies, filterRanges) {
  // Write your code here
  return frequencies.map((f) => isInRange(f, filterRanges)).filter((f) => f)
    .length;
}

function isInRange(f, filterRanges) {
  for (let i = 0; i < filterRanges.length; ++i) {
    if (f < filterRanges[i][0] || f > filterRanges[i][1]) {
      return false;
    }
  }
  return true;
}
```

# a query to identify the root and leaf node in a table in sql

```sql
SELECT
  ID,
  CASE
    WHEN P_ID IS NULL THEN 'Root'
    WHEN ID IN (SELECT P_ID FROM TREE) THEN 'Inner'
    ELSE 'Leaf'
  END AS TYPE
FROM TREE
ORDER BY ID;
```
