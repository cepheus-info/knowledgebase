# Mongodb pull duplicated data in nested array

## Problem

There are some duplicated data in nested array, and we want to remove them.

## Solution

Use `$pull` operator to remove the duplicated data.

```js
db.collection.update(
  { _id: ObjectId("5f0b9b3b9b9b9b9b9b9b9b9b") },
  { $pull: { "array": { $in: [ "a", "b" ] } } }
)
```

Above code will not remove any duplicated data, because `$pull` operator will only remove the first matched element in the array.

To distinct the duplicated data, we can use `$elemMatch` operator to find the first matched element in the array.

```js
db.collection.update(
  { _id: ObjectId("5f0b9b3b9b9b9b9b9b9b9b9b") },
  { $pull: { "array": { $elemMatch: { $in: [ "a", "b" ] } } } }
)
```

## Example

```js
> db.test.insert({ _id: ObjectId("5f0b9b3b9b9b9b9b9b9b9b9b"), array: [ "a", "b", "c", "d", "e", "f", "g", "h", "i", "j" ] })
WriteResult({ "nInserted" : 1 })
> db.test.find()
{ "_id" : ObjectId("5f0b9b3b9b9b9b9b9b9b9b9b"), "array" : [ "a", "b", "c", "d", "e", "f", "g", "h", "i", "j" ] }
> db.test.update(
...   { _id: ObjectId("5f0b9b3b9b9b9b9b9b9b9b9b") },
...   { $pull: { "array": { $in: [ "a", "b" ] } } }
... )
WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
> db.test.find()
{ "_id" : ObjectId("5f0b9b3b9b9b9b9b9b9b9b9b"), "array" : [ "c", "d", "e", "f", "g", "h", "i", "j" ] }
```
