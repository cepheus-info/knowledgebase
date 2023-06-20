# findLast in es2023

## How to implement findLast in es5?

```ts
function findLast<T>(
  array: T[],
  predicate: (value: T, index: number, obj: T[]) => boolean,
  thisArg?: any
): T | undefined {
  let i = array.length;
  while (i--) {
    if (predicate.call(thisArg, array[i], i, array)) {
      return array[i];
    }
  }
  return undefined;
}
```
