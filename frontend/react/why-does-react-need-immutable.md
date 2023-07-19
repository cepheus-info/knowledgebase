# Why does React need immutable?

## What is mutable?

Mutable means that something is changeable. In JavaScript, objects and arrays are mutable, which means that we can change their properties and elements.

```javascript
const obj = { a: 1, b: 2 };
obj.a = 3;
console.log(obj); // { a: 3, b: 2 }
```

So `const` doesn't mean that the value is immutable, it means that the variable can't be reassigned to a new value.

## React setState

In React, we use `setState` to update the state of a component. The `setState` function takes an object as an argument, and merges it with the current state.

```javascript
// state = { a: 1, b: 2 }
this.setState({ a: 3 });
// state = { a: 3, b: 2 }
```

## Why does React need immutable?

React uses a technique called [state reconciliation](https://reactjs.org/docs/reconciliation.html) to update the DOM in an efficient way. It compares the new state with the previous state, and only updates the DOM when necessary.

If we mutate the state directly, React will think that the state hasn't changed, and won't update the DOM.

```javascript
// state = { a: 1, b: 2 }
this.state.a = 3;
// state = { a: 3, b: 2 }
```

This is because the state object is the same before and after the mutation. React doesn't do a deep comparison of the state, it only checks if the state object is the same. It can be done with a simple `===` check.

```javascript
const state = { a: 1, b: 2 };
const state2 = state;
state2.a = 3;
console.log(state === state2); // true
```

From the React docs:

> Never mutate this.state directly, as calling setState() afterwards may replace the mutation you made. Treat this.state as if it were immutable.

## How to make the state immutable?

We can use the [spread operator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax) to create a new object with the same properties as the old object.

```javascript
const state = { a: 1, b: 2 };
const state2 = { ...state };
state2.a = 3;
console.log(state === state2); // false
```

## Thinking in Angular

Q: Does it make sense to use immutable in Angular?

A: No, because Angular uses a different technique to update the DOM. It uses a [zone](https://angular.io/guide/zone) to detect changes in the state, and updates the DOM when necessary. But it's still a good idea to use immutable in Angular, because it makes the code easier to reason about.
