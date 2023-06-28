# There are m men and w women, choose n person and at least k person are men, implement a function to get the number of all the possible combinations.

- Example:

- Input: m = 2, w = 2, n = 3, k = 1

- Output: 4

The possible combinations are:
(m1, m2, w1), (m1, m2, w2), (m1, w1, w2), (m2, w1, w2)

## Solution

Define a function to get the number of combinations of choosing r from n:
The formula is n! / (r! \* (n - r)!)

```javascript
function nCr(n, r) {
  return factorial(n) / (factorial(r) * factorial(n - r));
}
```

The question can be divided into two parts:

- choose k from m, and choose n - k from w
- choose k + 1 from m, and choose n - k - 1 from w
- ...
- choose n from m, and choose 0 from w

```javascript
function getCombinations(m, w, n, k) {
  let result = 0;
  for (let i = k; i <= n && i <= m; i++) {
    console.log(`result${i}: m: ${nCr(m, i)}, w: ${nCr(w, n - i)}`);
    result += nCr(m, i) * nCr(w, n - i);
  }
  return result;
}

function nCr(n, r) {
  return factorial(n) / (factorial(r) * factorial(n - r));
}

function factorial(n) {
  let result = 1;
  for (let i = 1; i <= n; i++) {
    result *= i;
  }
  return result;
}

// the result of getCombinations(3, 2, 2, 3) is 3
```

## Optimization

The time complexity of the above solution is O(n), however, the nCr function is O(n), so the time complexity of the above solution is O(n^2).

We can optimize the nCr function to O(1) by using the following formula:

nCr = n! / (r! \* (n - r)!) = n \* (n - 1) \* ... \* (n - r + 1) / r!

```javascript
function nCr(n, r) {
  let result = 1;
  for (let i = 1; i <= r; i++) {
    result *= n - i + 1;
    result /= i;
  }
  return result;
}
```

The time complexity of the optimized solution is O(n).
