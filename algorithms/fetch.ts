
fetch('https://jsonplaceholder.typicode.com/todos/1').then(response => response.json()).catch(error => console.error("rejects", error));