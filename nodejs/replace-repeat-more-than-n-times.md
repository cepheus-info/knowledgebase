# Replace repeat more than n times
```js
const str = 'aabbccdd';
const result = str.replace(/(.)\1{2,}/g, '$1$1');
console.log(result); // 'aabbccdd'
```

```js
// regex: (.*",\n)\1{1,}
// regex: (.*"),\n\1
```